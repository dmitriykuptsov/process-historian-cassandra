import requests
from json import loads
from time import time
import random
from time import sleep

class PHClient():
    def __init__(self, url):
        self.url = url
    def open(self):
        self.session = requests.session()
        result = self.session.post(self.url + "/auth/signin/", 
                                   json={"username": "admin", 
                                         "password": "password"}, 
                                    headers={"Accept": "application/json"})
        d = loads(result.text)
        self.token = d["token"]
        return d["success"]
    
    def get_tags(self, tag):
        result = self.session.post(self.url + "/api/get_sensors/", 
                    json={"tag": tag}, 
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        d = loads(result.text)
        return d["result"]
    
    def get_tags_by_attribute(self, attributes):
        result = self.session.post(self.url + "/api/get_sensors_by_attributes/", 
                    json={"attributes": attributes}, 
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        d = loads(result.text)
        return d["result"]
    
    def create_tag(self, tag, description, secret, attributes):
        result = self.session.post(self.url + "/api/add_sensor/", 
                    json={"tag": tag, 
                          "description": description, 
                          "secret": secret, 
                          "attributes": attributes}, 
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        return loads(result.text)["result"]
    
    def delete_tag(self, tag):
        result = self.session.post(self.url + "/api/delete_sensor/", 
                    json={"tag": tag},
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        return loads(result.text)["reason"]

    def get_data(self, start, end):
        result = self.session.post(self.url + "/api/get_data_raw/",
                    json={"tag": self.tag, "start": start, "end": end},
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        d = loads(result.text)
        return d["result"]
    
    def add_data(self, tag, timestamp, value):
        batch = {"points": [{self.tag: [{
                "timestamp": timestamp,
                "value": value
            }
        ]}]}

        result = self.session.post(self.url + "/injection/add_data/", 
            json=batch, 
            headers={"Accept": "application/json",
            "Authorization": "Bearer " + self.token})
        
        d = loads(result.text)
        return d["result"]  


client = PHClient("http://192.168.1.245:5006/")
client.open()
print(client.create_tag("sensor_1", "Test sensor", "123", ["test", "homeportal"]))
print(client.get_tags("sensor"))
print(client.get_tags_by_attribute(["test"]))
print(client.delete_tag("sensor_1"))
print(client.get_tags("sensor"))