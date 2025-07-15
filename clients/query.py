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
        print("Fetching 1 month of data took " + str(e-s) + " seconds")
        
c = PHClient("http://192.168.1.245:5006", "test2")
c.open()
c.run_query("2025-07-01 00:00:00", "2025-08-01 00:00:00")