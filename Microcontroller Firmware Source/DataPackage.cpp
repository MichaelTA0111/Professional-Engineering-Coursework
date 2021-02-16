//
// Created by drlim on 12/02/2021.
//

#include "DataPackage.h"


using namespace std::chrono_literals;

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

std::string DataPackage::jsonParser(const std::vector<DataPackage>& packages, std::chrono::microseconds runtime) {
    // Start the string with an opening square bracket
    std::string text = "[";

    bool flag = false;

    // Add each data package to the string
    for (auto package : packages) {
        if (flag) {
            // Separate each data package with a comma and space
            text += ", ";
        } else {
            flag = true;
        }

        long long timeAlive = std::chrono::duration_cast<std::chrono::milliseconds>(package.getTimeAlive(runtime)).count();

        // Create a stringstream to parse each data package into a JSON object
        std::ostringstream oss;
        oss << "{";
        oss << "\"timeAlive\": " << timeAlive << ", ";
        oss << "\"temperature\": " << package.getTemperature() << ", ";
        oss << "\"carbonMonoxide\": " << package.getCarbonMonoxide() << ", ";
        oss << "\"nitricOxide\": " << package.getNitricOxide() << ", ";
        oss << "\"nitrogenDioxide\": " << package.getNitrogenDioxide() << ", ";
        oss << "\"sulphurDioxide\": " << package.getSulphurDioxide();
        oss << "}";

        // Append to the string of data packets
        text += oss.str();
    }

    // End the string with a closing square bracket
    text += "]";

    return text;
}
