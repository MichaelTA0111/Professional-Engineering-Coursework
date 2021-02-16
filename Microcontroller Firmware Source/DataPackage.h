//
// Created by drlim on 12/02/2021.
//

#ifndef PROFESIONAL_ENGINEERING_COURSEWORK_DATAPACKAGE_H
#define PROFESIONAL_ENGINEERING_COURSEWORK_DATAPACKAGE_H


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
     * @param carbonMonoxide - The concentration of carbon monoxide read by the sensor as a double
     * @param nitricOxide  - The concentration of nitric oxide read by the sensor as a double
     * @param nitrogenDioxide - The concentration of nitrogen dioxide read by the sensor as a double
     * @param sulphurDioxide - The concentration of sulphur dioxide read by the sensor as a double
     */
    DataPackage(std::chrono::microseconds runtime, double temperature, double carbonMonoxide, double nitricOxide,
                double nitrogenDioxide, double sulphurDioxide);

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
     * Getter for carbon monoxide.
     * @return - The concentration of carbon monoxide read by the sensor as a double
     */
    double getCarbonMonoxide() const;

    /**
     * Getter for nitric oxide.
     * @return - The concentration of nitric oxide read by the sensor as a double
     */
    double getNitricOxide() const;

    /**
     * Getter for nitrogen dioxide.
     * @return - The concentration of nitrogen dioxide read by the sensor as a double
     */
    double getNitrogenDioxide() const;

    /**
     * Getter for sulphur dioxide.
     * @return - The concentration of sulphur dioxide read by the sensor as a double
     */
    double getSulphurDioxide() const;

private:
    std::chrono::microseconds creationTime;
    double temperature;
    double carbonMonoxide;
    double nitricOxide;
    double nitrogenDioxide;
    double sulphurDioxide;
};


#endif //PROFESIONAL_ENGINEERING_COURSEWORK_DATAPACKAGE_H
