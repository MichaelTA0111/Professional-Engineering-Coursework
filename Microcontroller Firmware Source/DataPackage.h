//
// Created by drlim on 12/02/2021.
//

#ifndef PROFESSIONAL_ENGINEERING_COURSEWORK_DATAPACKAGE_H
#define PROFESSIONAL_ENGINEERING_COURSEWORK_DATAPACKAGE_H


#include <chrono>

/**
 * A collection of data recorded by the sensor to be sent over the network.
 * @author - David Lim
 */
class DataPackage {
public:
    /**
     * Constructor for the data package.
     * @param runtime - The time the program has been running for as a std::chrono::duration
     * @param temperature - The temperature read by the sensor in celsius as a double
     * @param humidity - The concentration of carbon monoxide read by the sensor as a double
     * @param pressure  - The concentration of nitric oxide read by the sensor as a double
     * @param voc - The concentration of nitrogen dioxide read by the sensor as a double
     * @param sulphurDioxide - The concentration of sulphur dioxide read by the sensor as a double
     */
    DataPackage(std::chrono::microseconds runtime, double temperature, double humidity, double pressure, double voc);

    /**
     * Default constructor for the data package.
     */
    DataPackage();

    /**
     * Calculate and return the time since the data package was created.
     * @param runtime - The time the program has been running for as a std::chrono::duration
     * @return - The time since the data package was created as a std::chrono::duration
     */
    std::chrono::microseconds getTimeAlive(std::chrono::microseconds runtime) const;

    /**
     * Getter for temperature.
     * @return - The temperature read by the sensor in celsius as a double
     */
    double getTemperature() const;

    /**
     * Getter for humidity.
     * @return - The concentration of humidity read by the sensor as a double
     */
    double getHumidity() const;

    /**
     * Getter for pressure.
     * @return - The concentration of pressure read by the sensor as a double
     */
    double getPressure() const;

    /**
     * Getter for voc.
     * @return - The concentration of voc read by the sensor as a double
     */
    double getVoc() const;

private:
    std::chrono::microseconds creationTime;
    double temperature;
    double humidity;
    double pressure;
    double voc;
};


#endif //PROFESSIONAL_ENGINEERING_COURSEWORK_DATAPACKAGE_H
