import data
from datetime import datetime
import time
d = data.Data("Open")
print(d.Serialize())

d = data.Data("Sched", Args=[datetime.now().isoformat(), "TIME" ])
print(d.Serialize())