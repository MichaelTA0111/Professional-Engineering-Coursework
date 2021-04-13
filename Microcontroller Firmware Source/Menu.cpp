#include "Menu.h"
#include <string>


Menu::Menu(I2C &i2c, PinName resetPin) {
    oled = new Adafruit_SSD1306_I2c(i2c, resetPin);

    state = MAIN;
    option = FIRST;
    updateScreen = true;
    prevUpdateTime = 0ms;
}

void Menu::use(Direction dir, std::chrono::milliseconds runtime, bool connected,
               std::string ip, int unsentPackages, int timeUntilSend, double temp,
               int hum, double conc1, double conc2) {
    if (state == MAIN) {
        Option prevOption = option;
        updateOption(dir);

        // Define the message to be displayed
        char msg[4][22] = {"*********************",
                           "   Network status    ",
                           "   Current readings  ",
                           "*********************"};

        if (option != prevOption || updateScreen) {
            if (option == FIRST) {
                msg[1][1] = '>';
            } else if (option == SECOND) {
                msg[2][1] = '>';
            }

            updateScreen = false;
            displayMessage(msg);
        }

        if (dir == RIGHT) {
            if (option == FIRST) {
                state = STATUS;
                updateScreen = true;
                char newMsg[4][22] = {"Connected:",
                                      "IP:",
                                      "",
                                      ""};
                createBigMsg(msg, newMsg);
                state = TRANSITION_RIGHT;
                counter = 0;
            } else if (option == SECOND) {
                state = READINGS;
                updateScreen = true;
                char newMsg[4][22] = {"Temperature:",
                                      "Humidity:",
                                      "Pressure:",
                                      "NO2:"};
                createBigMsg(msg, newMsg);
                state = TRANSITION_RIGHT;
                counter = 0;
            }
        }
    } else if (state == STATUS) {
        if (runtime - prevUpdateTime > 500ms) {
            prevUpdateTime = runtime;
            updateScreen = true;
        }

        if (updateScreen) {
            displayStatus(connected, ip, unsentPackages, timeUntilSend);
            updateScreen = false;
        }

        if (dir == LEFT) {
            updateScreen = true;
            char leftMsg[4][22] = {"*********************",
                                   "   Network status    ",
                                   "   Current readings  ",
                                   "*********************"};
            char rightMsg[4][22] = {"Connected:",
                                    "IP:",
                                    "",
                                    ""};
            createBigMsg(leftMsg, rightMsg);
            state = TRANSITION_LEFT;
            counter = 0;
        }
    } else if (state == READINGS) {
        if (runtime - prevUpdateTime > 500ms) {
            prevUpdateTime = runtime;
            updateScreen = true;
        }

        if (updateScreen) {
            displayReadings(temp, hum, conc1, conc2);
            updateScreen = false;
        }

        if (dir == LEFT) {
            updateScreen = true;
            char leftMsg[4][22] = {"*********************",
                                   "   Network status    ",
                                   "   Current readings  ",
                                   "*********************"};
            char rightMsg[4][22] = {"Temperature:",
                                    "Humidity:",
                                    "Pressure:",
                                    "NO2:"};
            createBigMsg(leftMsg, rightMsg);
            state = TRANSITION_LEFT;
            counter = 0;
        }
    } else if (state == TRANSITION_LEFT) {
        if (runtime - prevUpdateTime > 50ms) {
            prevUpdateTime = runtime;
            if (counter < 22) {
                transitionScreenRev();
            } else {
                state = MAIN;
            }
        }
    } else if (state == TRANSITION_RIGHT) {
        if (runtime - prevUpdateTime > 50ms) {
            prevUpdateTime = runtime;
            if (counter < 22) {
                transitionScreen();
            } else {
                if (option == FIRST) {
                    state = STATUS;
                } else if (option == SECOND) {
                    state = READINGS;
                }
            }
        }
    }
}

void Menu::updateOption(Direction dir) {
    if (dir == DOWN) {
        if (option == FIRST) {
            option = SECOND;
        } else if (option == SECOND) {
            option = FIRST;
        }
    }
    if (dir == UP) {
        if (option == FIRST) {
            option = SECOND;
        } else if (option == SECOND) {
            option = FIRST;
        }
    }
}

void Menu::displayMessage(char msg[4][22]) {
    oled->setTextCursor(1, 0);
    oled->printf("%s", msg[0]);
    oled->setTextCursor(1, 8);
    oled->printf("%s", msg[1]);
    oled->setTextCursor(1, 16);
    oled->printf("%s", msg[2]);
    oled->setTextCursor(1, 24);
    oled->printf("%s", msg[3]);
    oled->display();
    oled->display();
}

void Menu::displayStatus(bool connected, std::string ip, int unsentPackages,
                         int timeUntilNextSend) {
    oled->setTextCursor(1, 0);
    if (connected) {
        oled->printf("Connected: Yes");
    } else {
        oled->printf("Connected: No");
    }
    oled->setTextCursor(1, 8);
    oled->printf("IP: %s", ip.c_str());
    if (!connected) {
        oled->setTextCursor(1, 16);
        if (unsentPackages < 1000) {
            oled->printf("Unsent Packages: %d", unsentPackages);
        } else {
            oled->printf("Unsent Packages: >999");
        }
        oled->setTextCursor(1, 24);
        if (timeUntilNextSend < 1000) {
            oled->printf("Next Send: %d s", timeUntilNextSend);
        } else {
            oled->printf("Next Send: >999 s");
        }
    }
    oled->display();
    oled->display();
}

void Menu::displayReadings(double temperature, int humidity, double pressure, double no2) {
    oled->setTextCursor(1, 0);
    oled->printf("Temperature: %.2f C", temperature);
    oled->setTextCursor(1, 8);
    oled->printf("Humidity: %d %%", humidity);
    oled->setTextCursor(1, 16);
    oled->printf("Pressure: %.2f hPa", pressure);
    oled->setTextCursor(1, 24);
    oled->printf("NO2: %.2f ug/m^3", no2);
    oled->display();
    oled->display();
}

void Menu::createBigMsg(char leftMsg[4][22], char rightMsg[4][22]) {
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 21; ++j) {
            bigMsg[i][j] = leftMsg[i][j];
            bigMsg[i][j + 22] = rightMsg[i][j];
        }
        bigMsg[i][21] = ' ';
        bigMsg[i][42] = '\0';
    }
}

void Menu::transitionScreen() {
    char currentMsg[4][22];

    for (int j = 0; j < 4; ++j) {
        for (int k = 0; k < 22; ++k) {
            currentMsg[j][k] = bigMsg[j][counter + k];
        }
        currentMsg[j][21] = '\0';
    }

    ++counter;
    displayMessage(currentMsg);
}

void Menu::transitionScreenRev() {
    char currentMsg[4][22];

    for (int j = 0; j < 4; ++j) {
        for (int k = 0; k < 22; ++k) {
            currentMsg[j][k] = bigMsg[j][21 - counter + k];
        }
        currentMsg[j][21] = '\0';
    }

    ++counter;
    displayMessage(currentMsg);
}
