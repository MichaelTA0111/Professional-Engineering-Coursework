#ifndef MENU_H
#define MENU_H


#include <string>
#include "mbed.h"
#include "Adafruit_SSD1306.h"
#include "Joystick.h"


using namespace std::chrono_literals;


/**
 * An enum for the possible states of the menu
 */
enum State {
    MAIN = 0, STATUS = 1, READINGS = 2,
    TRANSITION_RIGHT = 3, TRANSITION_LEFT = 4
};


/**
 * An enum for the possible options of the menu
 */
enum Option {
    FIRST = 1, SECOND = 2
};


/**
 * A menu class
 * @author - MichaelTA
 */
class Menu {
public:
    /**
     * Constructor for the Menu object
     * @param debounceDelay - The debounce delay (ms) as a long long
     */
    Menu(I2C &i2c, PinName resetPin);

    void use(Direction dir, std::chrono::milliseconds runtime, bool connected,
             std::string ip, int unsentPackages, int timeUntilNextSend, double temp,
             int hum, double conc1, double conc2);

private:

    void updateOption(Direction dir);

    void displayMessage(char msg[4][22]);

    void displayStatus(bool connected, std::string ip, int unsentPackages,
                       int timeUntilNextSend);

    void displayReadings(double temp, int hum, double conc1, double conc2);

    void createBigMsg(char leftMsg[4][22], char rightMsg[4][22]);

    void transitionScreen();

    void transitionScreenRev();

    Adafruit_SSD1306_I2c *oled;
    State state;
    Option option;
    bool updateScreen;
    std::chrono::milliseconds prevUpdateTime;
    char bigMsg[4][43];
    int counter;
};


#endif
