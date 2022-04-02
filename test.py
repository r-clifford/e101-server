import data
from datetime import datetime

d = data.Data(Command="Open", Time=datetime.now().isoformat(), T1="", T2="")
print(d.Serialize())

d = data.Data(Command="Sched", T1=datetime.now().isoformat(), T2="TIME")
print(d.Serialize())
