import datetime
import logging
from multiprocessing import Lock
from threading import Thread
from time import sleep
import motor


class Scheduler:
    openTime: datetime.datetime = datetime.datetime.now()
    closeTime: datetime.datetime = openTime
    motorController: motor.MotorController

    def __init__(
        self, motorController, motorLock, date, openTime, closeTime, currentState
    ) -> None:
        try:
            date = DateParser(date)
        except:
            logging.critical("Could not parse date")
        try:
            self.openTime = TimeParser(openTime, date)
            self.closeTime = TimeParser(closeTime, date)
        except:
            logging.critical("Could not parse time")
        self.currentState = currentState
        self.motorController = motorController
        self.motorLock = motorLock

    def start(self):
        return Thread(target=self.actuate)

    def actuate(self):
        waitTime = 0  # time before actuation in seconds
        nextWait = 0
        actuator = None
        logging.info(f"Open: {self.openTime}")
        logging.info(f"Close: {self.closeTime}")
        openWait = (self.openTime - datetime.datetime.now()).total_seconds()
        closeWait = (self.closeTime - datetime.datetime.now()).total_seconds()
        if openWait < closeWait:
            waitTime = openWait
            nextWait = closeWait - waitTime
            logging.info(f"Opening in {waitTime} seconds")
            actuator = self.motorController.open
            nextActuator = self.motorController.close
        else:
            waitTime = closeWait
            nextWait = openWait - waitTime
            logging.info(f"Closing in {waitTime} seconds")
            actuator = self.motorController.close
            nextActuator = self.motorController.open
        sleep(waitTime)
        with self.motorLock:
            logging.info("Opening/Closing")
            actuator()
        logging.info(f"Sleeping {nextWait} for next actuation")
        sleep(nextWait)
        with self.motorLock:
            logging.info("Opening/Closing")
            nextActuator()


# Non standard date time format given as strings
def DateParser(date: str) -> datetime.datetime:
    logging.debug(f"DateParser: {date}")
    parts = date.split("-")
    year = int(parts[0].strip())
    month = int(parts[1].strip())
    day = int(parts[2].strip())
    return datetime.datetime(year, month, day)


def TimeParser(time: str, date: datetime.datetime) -> datetime.datetime:
    logging.debug(f"TimeParser: {time}")
    parts = time.split(":")
    hour = int(parts[0].strip())
    minute = int(parts[1].strip())
    computed_time = datetime.time(hour, minute, 0)
    return datetime.datetime.combine(date.date(), computed_time)
