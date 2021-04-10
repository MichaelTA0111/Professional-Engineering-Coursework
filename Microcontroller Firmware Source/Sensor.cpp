//
// Created by MichaelTA on 09/02/2021.
//

#include "Sensor.h"

Sensor::Sensor() {
    medianReading = -300;
}

double Sensor::read() {
    calculateMedian();
    return medianReading;
}

void Sensor::newReading(double reading) {
    readings.push_back(reading);
}

void Sensor::calculateMedian() {
    if (!readings.empty()) {
        int length = (int) readings.size();
        if (readings.size() % 2 == 0) {
            // Median of an even number of total readings
            medianReading = (readings[length / 2 - 1] + readings[length / 2]) / 2;
        } else {
            // Median of an odd number of total readings
            medianReading = readings[length / 2];
        }
    } else {
        // Default value of -300 is out of range for all sensors, signifies no reading was taken
        medianReading = -300;
    }
    resetReadings();
}

void Sensor::resetReadings() {
    readings.clear();
}
