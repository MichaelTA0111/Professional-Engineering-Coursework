//
// Created by MichaelTA on 09/02/2021.
//

#ifndef MBED_SENSOR_H
#define MBED_SENSOR_H


#include <vector>

/**
 * Stores sensor data and then calculates a mean of that data
 * @author - MichaelTA
 */
class Sensor {
    public:
        /**
        * Constructor to create a sensor object with a negative median reading.
        */
        Sensor();

        /**
         * Getter for the median reading
         * @return - The median reading
         */
        [[nodiscard]] double read();

        /**
         * Method to add a new reading to the vector of readings
         * @param reading - The reading to be appended to the vector
         */
        void newReading(double reading);

    private:
        /**
         * Private ethod to calculate the median value from the vector of readings
         */
        void calculateMedian();

        /**
         * Private method to remove all readings from the vector of previous readings
         */
        void resetReadings();

        double medianReading;
        std::vector<double> readings;
};

#endif //MBED_SENSOR_H
