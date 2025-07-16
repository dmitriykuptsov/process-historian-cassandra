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
        print("Fetching 1 hour of data took " + str(e-s) + " seconds")
        
c = PHClient("http://process-historian.strangebit.io:5006", "dima2")
c.open()
for i in range(0, 100):
	c.run_query("2025-07-14 23:30:00", "2025-07-18 00:30:00")
