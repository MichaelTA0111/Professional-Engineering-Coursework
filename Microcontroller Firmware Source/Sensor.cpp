//
// Created by MichaelTA on 09/02/2021.
//

#include "Sensor.h"

/**
 * Constructor to create a sensor object with a negative median reading.
 */
Sensor::Sensor() {
    medianReading = -300;
}

/**
 * Getter for the median reading
 * @return - The median reading
 */
double Sensor::getMedianReading() const {
    return medianReading;
}

/**
 * Method to add a new reading to the vector of readings
 * @param reading - The reading to be appended to the vector
 */
void Sensor::newReading(double reading) {
    readings.push_back(reading);
}

/**
 * Method to calculate the median value from the vector of readings
 */
void Sensor::calculateMedian() {
    if (!readings.empty()) {
        int length = (int) readings.size();
        if (readings.size() % 2 == 0) {
            medianReading = (readings[length / 2 - 1] + readings[length / 2]) / 2;
        } else {
            medianReading = readings[length / 2];
        }
    } else {
        medianReading = -300;
    }
    resetReadings();
}

/**
 * Private method to remove all readings from the vector of previous readings
 */
void Sensor::resetReadings() {
    readings.clear();
}
