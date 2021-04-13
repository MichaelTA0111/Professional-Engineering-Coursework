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
    MAIN = 0, STATUS = 1, READINGS = 2, TRANSITION_RIGHT = 3, TRANSITION_LEFT = 4
};


/**
 * An enum for the possible options of the menu
 */
enum Option {
    FIRST = 1, SECOND = 2
};


/**
 * A menu class for use in an air pollution monitoring system
 * @author - MichaelTA
 */
class Menu {
public:
    /**
     * Constructor for the Menu object
     * @param i2c -
     * @param resetPin - The pin number of the reset pin
     */
    Menu(I2C &i2c, PinName resetPin);

    /**
     * Method to interact with the menu system
     * @param dir - The direction pressed on a joystick
     * @param runtime - The time that the program has been running for (ms)
     * @param connected - Whether the device is connected through ethernet
     * @param ip - The IPv4 address of the network
     * @param unsentPackages - The number of unsent packages to the database
     * @param timeUntilNextSend - The time until the next attempt to send data (s)
     * @param temp - The temperature reading (C)
     * @param hum - The humidity reading (%)
     * @param pres - The pressure reading (hPa)
     * @param voc - The resistance in the sensor based on the concectration of VOCs (kOhm)
     */
    void use(Direction dir, std::chrono::milliseconds runtime, bool connected,
             std::string ip, int unsentPackages, int timeUntilNextSend, double temp,
             int hum, double pres, double voc);

private:

    /**
     * Method to update the option on the main menu screen
     * @param dir - The direction pressed on a joystick
     */
    void updateOption(Direction dir);

    /**
     * Method to display a message across 4 lines on the OLED
     * @param msg - A message to be displayed on the OLED, taking a maximmum of 4 lines of 21 displayable characters
     */
    void displayMessage(char msg[4][22]);

    /**
     * Method to display the network status screen on the OLED
     * @param connected - Whether the device is connected through ethernet
     * @param ip - The IPv4 address of the network
     * @param unsentPackages - The number of unsent packages to the database
     * @param timeUntilNextSend - The time until the next attempt to send data (s)
     */
    void displayStatus(bool connected, std::string ip, int unsentPackages, int timeUntilNextSend);

    /**
     * Method to display the current readings screen on the OLED
     * @param timeUntilNextSend - The time until the next attempt to send data (s)
     * @param temp - The temperature reading (C)
     * @param hum - The humidity reading (%)
     * @param pres - The pressure reading (hPa)
     * @param voc - The resistance in the sensor based on the concectration of VOCs (kOhm)
     */
    void displayReadings(double temp, int hum, double pres, double voc);

    /**
     * Helper method to create a large message for the transition screen
     * @param leftMsg - The message for display on the left hand side of the transition screen
     */
    void createBigMsg(char leftMsg[4][22], char rightMsg[4][22]);

    /**
     * Method to transition the screen displayed on the OLED from left to right
     */
    void transitionScreen();

    /**
     * Method to transition the screen displayed on the OLED from right to left
     */
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
