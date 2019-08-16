"""Watson IoT Client
    By Lucas Orsi 8-2019
"""
import logging
import json
import os
import paho.mqtt.client as mqtt
import time


class WIoT(object):
    """Watson IoT Client Instance."""

    def __init__(self, filename='config.example.json', device_name=None):
        self._client = None
        self.device_name = device_name or filename.split()[0]
        self._credentials_from_file(filename)
        self.on_connect = lambda: logging.info(f'[{self.device_name}] Connected.')
        self.on_message = lambda _, __, msg: logging.info(f'[{self.device_name}] Received:{msg}')

    def connect(self):
        self._client = mqtt.Client(client_id=self._client_id, clean_session=False)
        print(self._user)
        print(self._token)
        print(self._host)
        print(self._client_id)
        self._client.username_pw_set(self._user, self._token)
        self._client.on_connect = self.on_connect
        self._client.connect(self._host, self._port, 60)
        self._client.loop()

    def publish(self, topic='+', payload=None):
        topic = f'iot-2/evt/{topic}/fmt/json'
        if payload is None:
            payload = {}
        self._client.publish(topic, json.dumps(payload))
        time.sleep(1)

    def _credentials_from_file(self, filename):
        if not filename.endswith('.json'):
            raise ValueError(f'{filename} must be a .json file')

        if filename not in os.listdir('./config'):
            raise FileNotFoundError(f'{filename} does not exist in /config directory')

        with open(f'./config/{filename}', 'r') as f:
            config = json.load(f)
            try:
                self._save_credentials(**config)
            except ValueError:
                raise ValueError(
                    "Chosen file does not have the adequate format."
                    " Please, follow config.example.json file structure."
                )

    def _save_credentials(self, org_id, dev_type, dev_id, user, token, port=1883):
        self._client_id = f'd:{org_id}:{dev_type}:{dev_id}'
        self._host = f'{org_id}.messaging.internetofthings.ibmcloud.com'
        self._user = user
        self._token = token
        self._port = port



my_wiot = WIoT()
my_wiot.connect()
my_wiot.publish("temperature", {"temperature": 8})
print(my_wiot)
