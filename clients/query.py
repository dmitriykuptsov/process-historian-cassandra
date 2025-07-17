import requests
from json import loads
from time import time
import random
class PHClient():
    def __init__(self, url, tag):
        self.url = url
        self.tag = tag
    def open(self):
        self.session = requests.session()
        result = self.session.post(self.url + "/auth/signin/", 
                                   json={"username": "admin", 
                                         "password": "password"}, 
                                    headers={"Accept": "application/json"})
        self.token = loads(result.text)["token"]
        
    def run_query(self, start, end):
        s = time()
        result = self.session.post(self.url + "/api/get_data_raw/",
                    json={"tag": self.tag, "start": start, "end": end},
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        e = time()
        #print(result.text)
        d = loads(result.text)
        print(len(d["result"]))
        print("Fetching 1 day of data took " + str(e-s) + " seconds, tag " + self.tag + " start " + str(s) + " end " + str(e) + " number " + str(len(d["result"])))


from threading import Thread

def run_thread(tag):
	c = PHClient("http://process-historian.strangebit.io:5006", tag)
	c.open()
	for i in range(0, 10):
		c.run_query("2025-07-17 00:00:00", "2025-07-18 00:00:00")

from sys import argv

for i in range(0, int(argv[1])):
	t = Thread(target=run_thread, args=("sensor_" + str(i), ))
	t.start()

