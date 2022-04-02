# Author: Ryan Clifford
# 2022-03-26
import json
import datetime


class Data:
    def __init__(
        self, Command, Time=datetime.datetime.now().isoformat(), T1="", T2=""
    ) -> None:
        self.Command = Command
        self.Time = Time
        self.T1 = T1
        self.T2 = T2
        self.object = {
            "Command": self.Command,
            "Time": self.Time,
            "T1": self.T1,
            "T2": self.T2,
        }

    def Serialize(self):
        return json.dumps(self.object)


if __name__ == "__main__":
    print("Try server.py")
