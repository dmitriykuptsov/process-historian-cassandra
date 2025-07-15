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
    def run_batch_insert(self, batch_size=1000, num_rounds=100):

        s = time()
        # '{"points": [{"test": [{"timestamp": 1752599157688, "value": 5.445}]}]}'
        for j in range(0, num_rounds):
            batch = {"points": [{self.tag: []}]}
            for i in range(0, batch_size):
                batch["points"][0][self.tag].append({
                    "timestamp": int(time() * 1000),
                    "value": random.random()
                })
            result = self.session.post(self.url + "/injection/add_data/", 
                    json=batch, 
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
            #print(result.text)
        e = time()
        print("Inserting a batch took " + str(e-s) + " seconds")
c = PHClient("http://192.168.1.245:5006", "test")
c.open()
c.run_batch_insert(10000, 100)