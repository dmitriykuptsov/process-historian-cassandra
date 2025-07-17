import requests
from json import loads
from time import time
import random
from time import sleep

class PHClient():
    def __init__(self, url, tag):
        self.url = url
        self.tag = tag
    def create_tag(self):
        result = self.session.post(self.url + "/api/add_sensor/", 
                    json={"tag": self.tag, "description": "", "secret": ""}, 
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        print(result.text)
    def open(self):
        self.session = requests.session()
        result = self.session.post(self.url + "/auth/signin/", 
                                   json={"username": "admin", 
                                         "password": "password"}, 
                                    headers={"Accept": "application/json"})
        self.token = loads(result.text)["token"]
    def run_batch_insert(self, batch_size=1000, num_rounds=100):
        for j in range(0, num_rounds):
            s = time()
            batch = {"points": [{self.tag: []}]}
            #t = time() * 1000
            t = 1752883200000
            c = 0
            j = 0
            for i in range(0, batch_size):
                t += 100
                c += 1
                batch["points"][0][self.tag].append({
                    "timestamp": int(t),
                    "value": random.random()
                })
                if c >= 1000:
                    j += 1
                    s = time()
                    try:
                        result = self.session.post(self.url + "/injection/add_data/", 
                            json=batch, 
                            headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
                        batch = {"points": [{self.tag: []}]}
                        e = time()
                        print("Inserting " + str(c) + " batch took " + str(e-s) + " seconds; batch index " + \
	    	           str(j) + " start " + str(s) + " end " + str(e) + " tag " + self.tag + " " + str(c/(e-s)) + " samples per second")
                    except Exception as e:
                        print(e)
                        pass
                    c = 0
            s = time()
            j += 1
            result = self.session.post(self.url + "/injection/add_data/", 
                            json=batch, 
                            headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
            e = time()
            print("Inserting " + str(c) + " batch took " + str(e-s) + " seconds; batch index" + \
                       str(j) + " start " + str(s) + " end " + str(e) + " tag " + self.tag + " " + str(c/(e-s)) + " samples per second")
            #print(result.text)
            #e = time()
            #print("Inserting " + str(batch_size) + " batch took " + str(e-s) + " seconds tag=" + self.tag)
            #print(str(batch_size/(e-s)) + " samples per second")
from threading import Thread

def run_thread(tag):
	c = PHClient("http://process-historian.strangebit.io:5006", tag)
	c.open()
	c.create_tag()
	c.run_batch_insert(int(24*60*60*10), 1)

from sys import argv

for i in range(0, int(argv[1])):
	t = Thread(target=run_thread, args=("exp_" + str(i), ))
	t.start()

