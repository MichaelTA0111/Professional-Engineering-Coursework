//
// Created by drlim on 30/01/2021.
//

#include "NetworkHandler.h"

#include <string>
#include <utility>
#include <sstream>

NetworkHandler::NetworkHandler(bool staticIpEnabled, int port, int timeout, std::string staticIp) : staticIpEnabled(
        staticIpEnabled), port(port), timeout(timeout), staticIp(std::move(staticIp)) {
    connectToNetwork();
}

void NetworkHandler::connectToNetwork() {
    if (ethernet.get_connection_status() == NSAPI_STATUS_DISCONNECTED) {
        if (this->staticIpEnabled) {
            setIpAddress();
        }

        ethernet.connect();

        socket->open(&ethernet);
        socket->bind(this->port);
        socket->listen();
    }
}

bool NetworkHandler::setIpAddress() {
    SocketAddress gateway;
    SocketAddress netmask;
    bool error = false;

    if (ethernet.get_connection_status() == NSAPI_STATUS_DISCONNECTED) {
        ethernet.connect();

        if (ethernet.get_connection_status() == NSAPI_STATUS_LOCAL_UP) {
            if (ethernet.get_gateway(&gateway) != NSAPI_ERROR_OK) {
                error = true;
            }

            if (ethernet.get_netmask(&netmask) != NSAPI_ERROR_OK) {
                error = true;
            }
        }

        ethernet.disconnect();
            
        if (!error) {
            if (ethernet.set_network(SocketAddress(staticIp.c_str()), netmask, gateway) != NSAPI_ERROR_OK) {
                error = true;
            }
        }

    } else {
        error = true;
    }
    
    return !error;
}

void NetworkHandler::connectToHost() {
    nsapi_error_t error;
    TCPSocket *newSocket = socket->accept(&error);
    if (error == NSAPI_ERROR_WOULD_BLOCK) {
        newSocket->close();
        delete newSocket;
        hostConnectionEstablished = false;
    } else {
        socket->close();
        delete socket;
        socket = newSocket;
        hostConnectionEstablished = true;
    }
}

void NetworkHandler::send(DataPackage dataPackage, std::chrono::microseconds runtime) {
    buffer.push_back(dataPackage);
    std::string json = jsonParser(buffer, runtime);
    nsapi_size_t dataSent;
    dataSent = socket->send(json.c_str(), json.size() + 1);
    if (dataSent >= 0) {
        connectionActive = true;
        buffer.clear();
    } else {
        connectionActive = false;
    }
}

std::string NetworkHandler::jsonParser(const std::vector<DataPackage> &packages, std::chrono::microseconds runtime) {
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
        oss << "\"timeAlive\": " << std::to_string(timeAlive) << ", ";
        oss << "\"temperature\": " << std::to_string(package.getTemperature()) << ", ";
        oss << "\"humidity\": " << std::to_string(package.getHumidity()) << ", ";
        oss << "\"pressure\": " << std::to_string(package.getPressure()) << ", ";
        oss << "\"voc\": " << std::to_string(package.getVoc());
        oss << "}";

        // Append to the string of data packets
        text += oss.str();
    }

    // End the string with a closing square bracket
    text += "]";

    return text;
}

void NetworkHandler::disconnect() {
    socket->close();
    delete socket;
    ethernet.disconnect();
}

void NetworkHandler::setStaticIpEnabled(bool staticIpEnabled) {
    if (ethernet.get_connection_status() == NSAPI_STATUS_DISCONNECTED) {
        if (staticIpEnabled != this->staticIpEnabled) {
            if (staticIpEnabled) {
                setIpAddress();
            } else {
                ethernet.set_dhcp(true);
            }
        }
        NetworkHandler::staticIpEnabled = staticIpEnabled;
    }
}

bool NetworkHandler::isHostConnectionEstablished() const {
    return hostConnectionEstablished;
}

bool NetworkHandler::isConnectionActive() const {
    return connectionActive;
}

std::string NetworkHandler::getIpAddress() {
    if (ethernet.get_connection_status() == NSAPI_STATUS_DISCONNECTED) {
        return std::string("No IP");
    }

    SocketAddress ipAddress;
    ethernet.get_ip_address(&ipAddress);

    if(ipAddress.get_ip_address()[0] == '\0') {
        return std::string("No IP");
    }
    
    return std::string(ipAddress.get_ip_address());
}

int NetworkHandler::getBufferSize() const {
    return buffer.size();
}
