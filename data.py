# Author: Ryan Clifford
# 2022-03-26
import json
from typing import AnyStr
import datetime
class Data:
    def __init__(self, Command, Time=datetime.datetime.now().isoformat(), Args=None) -> None:
        self.Command = Command
        if Command.lower() == "sched" and len(Args) < 2:
            raise TypeError
        self.Time = Time
        self.Args = Args
        self.object = {"Command": self.Command,
                        "Time": self.Time,
                        "Args": self.Args}
    
    def Serialize(self):
        return json.dumps(self.object)

if __name__ == '__main__':
    print("Try server.py")        