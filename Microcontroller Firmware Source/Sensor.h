#ifndef MBED_SENSOR_H
#define MBED_SENSOR_H

#include <vector>

/**
 * Abstract class for sensors to inherit from
 */
class Sensor {
    public:
        Sensor();
        [[nodiscard]] double getMedianReading() const;
        virtual void newReading(double reading);
        void calculateMedian();

    private:
        double medianReading;
        std::vector<double> readings;
        void resetReadings();
};

#endif //MBED_SENSOR_H
