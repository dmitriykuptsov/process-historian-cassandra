import requests
from json import loads, dumps
from time import time
import random
from time import sleep
from datetime import datetime, UTC
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC

class PHClient():
    def __init__(self, url):
        self.url = url
    def open(self, username = None, password = None):
        self.session = requests.session()
        if username:
            result = self.session.post(self.url + "/auth/signin/", 
                                   json={"username": username, 
                                         "password": password}, 
                                    headers={"Accept": "application/json"})
            d = loads(result.text)
            self.token = d["token"]
            return d["success"]
        else:
            return True

    def __compute_hmac__(self, data, key):
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
    
    def update_sensor(self, tag, description, secret, attributes):
        result = self.session.post(self.url + "/api/update_sensor/", 
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

    def get_data_public(self, tag, start, end):
        result = self.session.post(self.url + "/api/get_data_raw_public/",
                    json={"tag": tag, "start": start, "end": end},
                    headers={"Accept": "application/json"})
        print(result.text)
        d = loads(result.text)
        return d["result"]
    
    def add_data(self, tag, timestamp, value, secret):

        data_to_sign = dumps([{
                                "timestamp": timestamp,
                                "value": value
                            }])
        hmac = self.__compute_hmac__(data_to_sign, secret)

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
            headers={"Accept": "application/json"})
        
        d = loads(result.text)
        return d["result"] 
    def add_data_batch(self, tag, data, secret):

        data_to_sign = dumps(data)
        hmac = self.__compute_hmac__(data_to_sign, secret)

        data = {
                "points": {
                    tag: {
                        "data": data, 
                        "hmac": hmac
                    }
                }
            }

        result = self.session.post(self.url + "/injection/add_data/", 
            json=data, 
            headers={"Accept": "application/json"})
        
        d = loads(result.text)
        return d["result"]  


client = PHClient("https://process-historian.strangebit.io/")
#client.open("admin", "cicurdyifyuWyadvurlyondaizJibOts")
client.open()
#print(client.create_tag("demo_temperature_tag", "Demo sensor", "mudCewofalEjNacsyivHothfuikcewdyaicAbbighravOladHottOcisfadEgNaz", ["demo", "temperature"]))


import subprocess
while True:
    data = []
    current_datetime = datetime.now(UTC)
    process = subprocess.Popen(["cat", " /sys/class/thermal/thermal_zone0/temp"], stdout=subprocess.PIPE, text=True)
    output, errors = process.communicate()
    #value = float(output)/1000
    value = 10.2
    data.append({
        "timestamp": current_datetime.timestamp() * 1000,
        "value": value
    })
    client.add_data_batch("CO2_sensor_outside", data, "mudCewofalEjNacsyivHothfuikcewdyaicAbbighravOladHottOcisfadEgNaz")
