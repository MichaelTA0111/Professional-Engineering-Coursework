#include "mbed.h"
#include "mbed_bme680.h"
#include "Adafruit_SSD1306.h"
#include "Menu.h"

using namespace std::chrono;

// Used inside the BME680 Mbed Lib.
SPI spi(p11, p12, p13);
DigitalOut cs(p14);

BME680 bme680;

// an I2C sub-class that provides a constructed default
class I2CPreInit : public I2C
{
public:
    I2CPreInit(PinName sda, PinName scl) : I2C(sda, scl)
    {
        frequency(400000);
        start();
    };
};
 
I2CPreInit gI2C(p28,p27);

int main()
{
    // Initialise analogue inputs for the joystick x and y positions
    AnalogIn joyX = AnalogIn(p15);
    AnalogIn joyY = AnalogIn(p16);
    
    // Initialise the timer
    Timer runtime;
    runtime.start();
    
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
    int ip[4] = {192, 168, 1, 254};
    int unsent = 3;
    int nextSend = 2;
    double temp = 19.32;
    int hum = 67;
    double conc1 = 2.34;
    double conc2 = 1.72;
    
    while (true)
    {
        if (bme680.performReading()) {
            temp = bme680.getTemperature();
            hum = bme680.getHumidity();
            conc1 = bme680.getPressure() / 100.0;
            conc2 = bme680.getGasResistance() / 1000.0;
        }

        // Find the direction held
        Direction dir = js1.directionPressed(joyX.read(), joyY.read(),
                                             duration_cast<milliseconds>(
                                             runtime.elapsed_time()).count());
        
        // Operate the menu
        menu.use(dir, duration_cast<milliseconds>(runtime.elapsed_time()),
                 connected, ip, unsent, nextSend, temp, hum, conc1, conc2);
    }
}


