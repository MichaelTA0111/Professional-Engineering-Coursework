//
// Created by drlim on 22/01/2021.
//

#include "EventIntervalTrigger.h"

using namespace std::literals;

EventIntervalTrigger::EventIntervalTrigger(std::chrono::microseconds interval) : interval(interval) {
    EventIntervalTrigger::startTime = 0ms;
    running = false;
    eventCounter = 0;
}

void EventIntervalTrigger::start(std::chrono::microseconds currentTime) {
    startTime = currentTime;
    running = true;
}

void EventIntervalTrigger::pause() {
    running = false;
    eventCounter = 0;
}

bool EventIntervalTrigger::hasElapsed(std::chrono::microseconds currentTime) {
    if (running) {
        std::chrono::microseconds nextTrigger = startTime + interval * (eventCounter + 1);
        if ((eventCounter == 0) || (currentTime >= nextTrigger)) {
            eventCounter++;
            return true;
        }
    }
    return false;
}

void EventIntervalTrigger::setInterval(const std::chrono::microseconds interval) {
    EventIntervalTrigger::interval = interval;
}
