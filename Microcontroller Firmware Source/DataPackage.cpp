//
// Created by drlim on 12/02/2021.
//

#include "DataPackage.h"


using namespace std::chrono_literals;

DataPackage::DataPackage(std::chrono::microseconds runtime, double temperature, double humidity, double pressure,
                         double voc) : creationTime(runtime), temperature(temperature), humidity(humidity),
                                       pressure(pressure), voc(voc) {}

DataPackage::DataPackage() : creationTime(0s), temperature(-300), humidity(-300), pressure(-300), voc(-300) {}

std::chrono::microseconds DataPackage::getTimeAlive(std::chrono::microseconds runtime) const {
    return runtime - creationTime;
}

double DataPackage::getTemperature() const {
    return temperature;
}

double DataPackage::getHumidity() const {
    return humidity;
}

double DataPackage::getPressure() const {
    return pressure;
}

double DataPackage::getVoc() const {
    return voc;
}
