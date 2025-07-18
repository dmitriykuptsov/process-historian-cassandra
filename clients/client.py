import requests
from json import loads, dumps
from time import time
import random
from time import sleep
from datetime import datetime
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC

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
    
    def __compute_hmac(self, data, key):
        """
        Computes the HMAC of the data
        """
        h = HMAC.new(key.encode("ASCII"), digestmod=SHA256)
        h.update(data.encode("ASCII"))
        return h.hexdigest()
    
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
        return loads(result.text)["result"]

    def get_data(self, tag, start, end):
        result = self.session.post(self.url + "/api/get_data_raw/",
                    json={"tag": tag, "start": start, "end": end},
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        d = loads(result.text)
        return d["result"]
    
    def add_data(self, tag, timestamp, value, secret):

        data_to_sign = dumps([{
                                "timestamp": timestamp,
                                "value": value
                            }])
        hmac = self.__compute_hmac(data_to_sign, secret)

        data = {
                "points": {
                    tag: {
                        "data": [{
                            "timestamp": timestamp,
                            "value": value
                            }], 
                        "hmac": hmac
                    }
                }
            }

        result = self.session.post(self.url + "/injection/add_data/", 
            json=data, 
            headers={"Accept": "application/json",
            "Authorization": "Bearer " + self.token})
        
        d = loads(result.text)
        return d["result"]  

"""
client = PHClient("http://192.168.1.245:5006/")
client.open()
print(client.create_tag("sensor_1", "Test sensor", "123", ["test", "homeportal"]))
print(client.get_tags("sensor"))
print(client.get_tags_by_attribute(["test"]))
#print(client.delete_tag("sensor_1"))
print(client.get_tags("sensor"))
i = 0
while i < 100:
    current_datetime = datetime.now()
    client.add_data("sensor_1", current_datetime.timestamp() * 1000, 100, "123")
    i += 1
print(client.get_data("sensor_1", "2025-07-18 00:00:00", "2025-07-18 23:00:00"))
"""