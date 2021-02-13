//
// Created by drlim on 12/02/2021.
//

#include "DataPackage.h"

DataPackage::DataPackage(std::chrono::microseconds runtime, double temperature, double carbonMonoxide,
                         double nitricOxide, double nitrogenDioxide, double sulphurDioxide) : creationTime(runtime),
                                                                                              temperature(temperature),
                                                                                              carbonMonoxide(
                                                                                                      carbonMonoxide),
                                                                                              nitricOxide(nitricOxide),
                                                                                              nitrogenDioxide(
                                                                                                      nitrogenDioxide),
                                                                                              sulphurDioxide(
                                                                                                      sulphurDioxide) {}

DataPackage::DataPackage() : creationTime(0s), temperature(-300), carbonMonoxide(-300), nitricOxide(-300),
                             nitrogenDioxide(-300), sulphurDioxide(-300) {}

std::chrono::microseconds DataPackage::getTimeAlive(std::chrono::microseconds runtime) const {
    return runtime - creationTime;
}

double DataPackage::getTemperature() const {
    return temperature;
}

double DataPackage::getCarbonMonoxide() const {
    return carbonMonoxide;
}

double DataPackage::getNitricOxide() const {
    return nitricOxide;
}

double DataPackage::getNitrogenDioxide() const {
    return nitrogenDioxide;
}

double DataPackage::getSulphurDioxide() const {
    return sulphurDioxide;
}
