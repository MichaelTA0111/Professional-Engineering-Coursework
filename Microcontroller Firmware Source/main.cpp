#include "mbed.h"
#include "mbed_bme680.h"
#include "Adafruit_SSD1306.h"
#include "EventIntervalTrigger.h"
#include "Menu.h"
#include "Sensor.h"
#include "DataPackage.h"
#include "NetworkHandler.h"
#include <cstdio>

using namespace std::chrono;

// Used inside the BME680 Mbed Lib.
SPI spi(p11, p12, p13);
DigitalOut cs(p14);

// Second thread for networking
Thread thread;

// BME680 sensor to interface with the physical sensor
BME680 bme680;

// Senosr objects to be used to calculate median readings
Sensor temperatureSesnor;
Sensor humiditySensor;
Sensor pressureSensor;
Sensor vocSensor;

// Vector to store packages to be sent over the network
std::vector<DataPackage> dataPackages;


// an I2C sub-class that provides a constructed default
class I2CPreInit : public I2C {
public:
    I2CPreInit(PinName sda, PinName scl) : I2C(sda, scl) {
        frequency(400000);
        start();
    };
};

I2CPreInit gI2C(p28, p27);

NetworkHandler network(false);

void networkThread() {
    // Initialise the timers
    Timer runtime;
    runtime.start();

    while (true) {
        if (!network.isHostConnectionEstablished()) {
            network.connectToHost();
        }
        
        if (dataPackages.size() != 0) {
            for (auto package : dataPackages) {
                network.send(package, runtime.elapsed_time());
            }
            dataPackages.clear();
        }
    }
}

int main() {
    thread.start(networkThread);

    // Initialise analogue inputs for the joystick x and y positions
    AnalogIn joyX = AnalogIn(p15);
    AnalogIn joyY = AnalogIn(p16);

    // Initialise the timers
    Timer runtime;
    runtime.start();

    EventIntervalTrigger sensorReadTimer(1s);
    sensorReadTimer.start(runtime.elapsed_time());

    EventIntervalTrigger sensorAverageTimer(1min);
    sensorAverageTimer.startNext(runtime.elapsed_time());

    // Initialise the joystick
    Joystick js1 = Joystick();

    // Initialise the menu
    Menu menu = Menu(gI2C, p26);

    if (!bme680.begin()) {
        printf("BME680 Begin failed \r\n");
        return 1;
    }

    // Declare variables
    bool connected = true;
    int unsent = 3;
    int nextSend = 2;
    double temperature = 19.32;
    int humidity = 67;
    double pressure = 2.34;
    double vocs = 1.72;

    while (true) {
        // If a second has passed since the last sensor reading
        if (sensorReadTimer.hasElapsed(runtime.elapsed_time())) {
            // Read and store the new sensor readinge
            if (bme680.performReading()) {
              temperature = bme680.getTemperature();
              humidity = bme680.getHumidity();
              pressure = bme680.getPressure() / 100.0;
              vocs = bme680.getGasResistance() / 1000.0;

              temperatureSesnor.newReading(temperature);
              humiditySensor.newReading(humidity);
              pressureSensor.newReading(pressure);
              vocSensor.newReading(vocs);
            }
        }

        if (sensorAverageTimer.hasElapsed(runtime.elapsed_time())) {
            dataPackages.push_back(DataPackage(runtime.elapsed_time(), temperatureSesnor.read(), humiditySensor.read(),
                                               pressureSensor.read(), vocSensor.read()));
        }

        // Find the direction held
        Direction dir = js1.directionPressed(joyX.read(), joyY.read(),
                                             duration_cast<milliseconds>(runtime.elapsed_time()).count());


        printf("Ip address: %s\r\n", network.getIpAddress().c_str());


        // Operate the menu
        menu.use(dir, duration_cast<milliseconds>(runtime.elapsed_time()), network.isConnectionActive(),
                 network.getIpAddress(), dataPackages.size(), nextSend, temperature, humidity, pressure, vocs);
    }
}
