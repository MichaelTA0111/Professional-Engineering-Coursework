//
// Created by drlim on 30/01/2021.
//

#ifndef PROFESSIONAL_ENGINEERING_COURSEWORK_NETWORKHANDLER_H
#define PROFESSIONAL_ENGINEERING_COURSEWORK_NETWORKHANDLER_H


#include "mbed.h"
#include "EthernetInterface.h"
#include <vector>
#include <string>
#include "DataPackage.h"

/**
 * Handles networking from the Mbed controller to the remote host.
 * @author - David Lim
 */
class NetworkHandler {
public:
    /**
     * Constructor for the NetworkHandler.
     * @param staticIpEnabled - Whether or not the Mbed is running in static IP mode as a boolean
     * @param port - The network port for the Mbed to use as an integer
     * @param timeout - The timeout time in milliseconds for the network socket as an integer
     * @param staticIp - The static IP address to use as a std::string
     */
    NetworkHandler(bool staticIpEnabled, int port = 1028, int timeout, std::string staticIp = "192.168.1.255");

    /**
     * Connect to the local network.
     */
    void connectToNetwork();

    /**
     * Check for and connect to any incoming connections.
     */
    void connectToHost();

    /**
     * Send a package of sensor data to the remote host.
     * @param dataPackage - An DataPackage of sensor data
     * @param runtime - The time the program has been running for as a std::chrono::duration
     */
    void send(DataPackage dataPackage, std::chrono::microseconds runtime);

    /**
     * Disconnect from the local network.
     */
    void disconnect();

    /**
     * Setter for staticIpEnabled. Network interface must be disconnected otherwise does nothing.
     * @param staticIpEnabled - The new value for staticIpEnabled as a boolean
     */
    void setStaticIpEnabled(bool staticIpEnabled);

    /**
     * Getter for connectionEstablished.
     * @return - Whether a connection has been made with the remote host as a boolean
     */
    bool isHostConnectionEstablished() const;

    /**
     * Getter for connectionActive.
     * @return - Whether the last package was successfully sent as a boolean.
     */
    bool isConnectionActive() const;

    /**
     * Calculate and return how many packages are to be sent.
     * @return - How many packages are to be sent as an integer.
     */
    int getBufferSize() const;

private:
    bool staticIpEnabled;
    bool hostConnectionEstablished = false;
    bool connectionActive = false;
    const int port;
    const int timeout;
    std::string staticIp;
    EthernetInterface ethernet;
    TCPSocket *socket = new TCPSocket();
    std::vector<DataPackage> buffer;

    /**
     * Helper method to set the IP address of the network interface. Network interface must be disconnected.
     * @return - Whether the IP address was successfully set as a boolean
     */
    bool setIpAddress();

    /**
     * Static method to parse a vector of data packages into a JSON object
     * @author - MichaelTA
     * @param packages - A vector of data packages
     * @param runtime - The time the program has been running for as a std::chrono::duration
     * @return - A JSON object as a string
     */
     static std::string jsonParser(const std::vector<DataPackage>& packages, std::chrono::microseconds runtime);
};


#endif //PROFESSIONAL_ENGINEERING_COURSEWORK_NETWORKHANDLER_H
