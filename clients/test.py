from client import PHClient
from time import time
from datetime import datetime, timezone
from random import uniform
from time import sleep;

c=PHClient("http://localhost:5006/")
c.open("admin", "password")
#print(c.get_data_public("demo_temperature_tag", "2026-04-15 23:50:00", "2026-04-16 00:00:00"))
#print(c.get_data_with_aggregation(tag = "demo_temperature_tag", start="2026-04-15 23:50:00", end="2026-04-16 00:00:00", aggr="avg", interval=1))
print(time())
print(uniform(20, 25))
for i in range(0, 100):
	now = datetime.now(timezone.utc)
	print(now)
	print(now.timestamp())
	c.add_data("demo_temperature_tag", now.timestamp()*1000, uniform(20, 25), "test");
	sleep(1)
