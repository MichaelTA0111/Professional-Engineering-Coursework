//
// Created by drlim on 13/04/2021.
//

#include "NewJoystick.h"

Joystick::Joystick(const PinName& x_pin, const PinName& y_pin, std::chrono::milliseconds debounce_delay,
        float low_limit_x, float high_limit_x, float low_limit_y, float high_limit_y)
        :x_pin(x_pin), y_pin(y_pin), left_button(debounce_delay), right_button(debounce_delay),
         up_button(debounce_delay), down_button(debounce_delay), low_limit_x(low_limit_x), high_limit_x(high_limit_x),
         low_limit_y(low_limit_y), high_limit_y(high_limit_y) { }

Direction Joystick::direction_pressed(std::chrono::milliseconds runtime)
{
    if (left_button.isPressed(x_pin.read()<low_limit_x, runtime)) {
        return left;
    }
    if (right_button.isPressed(x_pin.read()>high_limit_x, runtime)) {
        return right;
    }
    if (up_button.isPressed(y_pin.read()<low_limit_y, runtime)) {
        return up;
    }
    if (down_button.isPressed(y_pin.read()>high_limit_y, runtime)) {
        return down;
    }
}
