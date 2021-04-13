//
// Created by drlim on 13/04/2021.
//

#ifndef PROFESSIONAL_ENGINEERING_COURSEWORK_JOYSTICK_H
#define PROFESSIONAL_ENGINEERING_COURSEWORK_JOYSTICK_H

#include "mbed.h"
#include "Button.h"
#include <chrono>

enum Direction {
    none = 0, left = 1, right = 2, up = 3, down = 4
};

class Joystick {
public:
    Joystick(std::chrono::milliseconds debounce_delay, const PinName& x_pin, const PinName& y_pin, float low_limit_x,
            float high_limit_x, float low_limit_y, float high_limit_y);

    Direction direction_pressed(std::chrono::milliseconds runtime);

private:
    AnalogIn x_pin;
    AnalogIn y_pin;

    Button left_button;
    Button right_button;
    Button up_button;
    Button down_button;

    float low_limit_x;
    float high_limit_x;
    float low_limit_y;
    float high_limit_y;
};

#endif //PROFESSIONAL_ENGINEERING_COURSEWORK_JOYSTICK_H
