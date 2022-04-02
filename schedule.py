import datetime
import logging
from threading import Thread
from time import sleep
import motor


class Scheduler:
    openTime: datetime.datetime = datetime.datetime.now()
    closeTime: datetime.datetime = openTime
    isClosed: bool = True
    motorController: motor.MotorController

    def __init__(
        self, motorController, date, openTime, closeTime, currentState
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

    def start(self):
        return Thread(target=self.actuate)

    def actuate(self):
        waitTime = 0  # time before actuation in seconds
        actuator = None
        if self.isClosed:
            waitTime = (self.openTime - datetime.datetime.now()).total_seconds()
            logging.info(f"Opening in {waitTime} seconds")
            actuator = self.motorController.open
        else:
            waitTime = (self.closeTime - datetime.datetime.now()).total_seconds()
            logging.info(f"Closing in {waitTime} seconds")
            actuator = self.motorController.close
        sleep(waitTime)
        logging.info("Opening/Closing")
        actuator()


# Non standard date time format given as strings
def DateParser(date: str) -> datetime.datetime:
    parts = date.split("-")
    year = int(parts[0].strip())
    month = int(parts[1].strip())
    day = int(parts[2].strip())
    return datetime.datetime(year, month, day)


def TimeParser(time: str, date: datetime.datetime) -> datetime.datetime:
    parts = time.split(":")
    hour = int(parts[0].strip())
    minute = int(parts[1].strip())
    computed_time = datetime.time(hour, minute, 0)
    return datetime.datetime.combine(date.date(), computed_time)
