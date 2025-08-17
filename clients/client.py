import requests
from json import loads, dumps
from time import time
import random
from time import sleep
from datetime import datetime, UTC
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC

ALERT_TYPES = {"MAX_OVERSHOOT": 0, "MIN_OVERSHOOT": 1}

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
            print(result.text)
            d = loads(result.text)
            self.token = d.get("token", None)
            return d.get("success", False)
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
    
    def get_data_with_aggregation(self, tag, start, end, aggr = "avg", interval = 360):
        result = self.session.post(self.url + "/api/get_data_raw_with_aggregation/",
                    json={"tag": tag, "start": start, "end": end, "aggregation": aggr, "interval": interval},
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        print(result.text)
        d = loads(result.text)
        return d["result"]

    def get_data_public(self, tag, start, end):
        result = self.session.post(self.url + "/api/get_data_raw_public/",
                    json={"tag": tag, "start": start, "end": end},
                    headers={"Accept": "application/json"})
        print(result.text)
        d = loads(result.text)
        return d["result"]
    
    def get_alerts(self, tag, start, end):
        result = self.session.post(self.url + "/api/get_alerts/",
                    json={"tag": tag, "start": start, "end": end},
                    headers={"Accept": "application/json",
                            "Authorization": "Bearer " + self.token})
        print(result.text)
        d = loads(result.text)
        return d["result"]
    
    def get_alerts_public(self, tag, start, end):
        result = self.session.post(self.url + "/api/get_alerts_public/",
                    json={"tag": tag, "start": start, "end": end},
                    headers={"Accept": "application/json"})
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
    
    def add_alert_batch(self, tag, data, secret):

        data_to_sign = dumps(data)
        hmac = self.__compute_hmac__(data_to_sign, secret)

        data = {
                "alerts": {
                    tag: {
                        "data": data, 
                        "hmac": hmac
                    }
                }
            }

        result = self.session.post(self.url + "/injection/add_alert/", 
            json=data, 
            headers={"Accept": "application/json"})
        
        d = loads(result.text)
        return d["result"]  
