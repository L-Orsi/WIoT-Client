import logging
import json
import yaml
import os
import paho.mqtt.client as mqtt
import time

logging.basicConfig(level=logging.DEBUG)

__clients = []


def create_publisher(filename):
    global __clients
    with open(filename) as config_file:
        cfg = yaml.safe_load(config_file)
        org_id, dev_type, dev_id = (cfg["org_id"], cfg["dev_type"], cfg["dev_id"])
        token, port = (cfg["token"], cfg["port"])
        client_id = f'd:{org_id}:{dev_type}:{dev_id}'
        host = f'{org_id}.messaging.internetofthings.ibmcloud.com'
        client = mqtt.Client(client_id=client_id, clean_session=False)
        client.username_pw_set("use-token-auth", token)
        client.connect(host, port, 60)

        def publisher(event='+', payload=None, on_pub_callback=None):
            topic = f'iot-2/evt/{event}/fmt/json'
            if payload is None:
                payload = {}
            if on_pub_callback:
                client.on_publish = on_pub_callback
            mid = client.publish(topic, json.dumps(payload))
            time.sleep(1)
            return mid

        __clients.append(client)
        return publisher


def create_subscriber(filename):
    global __clients
    with open(filename) as config_file:
        cfg = yaml.safe_load(config_file)
        org_id, dev_type, dev_id = (cfg["org_id"], cfg["dev_type"], cfg["dev_id"])
        token, port = (cfg["token"], cfg["port"])
        client_id = f'd:{org_id}:{dev_type}:{dev_id}'
        host = f'{org_id}.messaging.internetofthings.ibmcloud.com'
        client = mqtt.Client(client_id=client_id, clean_session=False)
        client.username_pw_set("use-token-auth", token)
        client.connect(host, port, 60)
        client.loop()

        def subscriber(command='+', callback=None):
            # topic = f'iot-2/type/{dev_type}/id/{dev_id}/evt/{event}/fmt/json'
            topic = f'iot-2/cmd/{command}/fmt/json'
            client.subscribe(topic)

            def on_message(_, __, message):
                if message.topic == topic:
                    callback(json.loads(message.payload.decode("utf-8")))
                else:
                    return
            client.on_message = on_message

        __clients.append(client)
        return subscriber





'''

# Instance what you will need

# temp_subs = create_subscriber("./config/TemperatureSensor.yml")


temp_pub = create_publisher("./config/TemperatureSensor.yml")
temp_pub2 = create_publisher("./config/TemperatureSensor.yml")

# Have fun!
def my_friendly_callback(msg):
    print(f"I received {msg}")


# temp_subs("temperature", my_friendly_callback)
# time.sleep(5)
temp_pub("temperature", {"tmp": 20})
temp_pub2("humidity", {"hum": 100})
time.sleep(5)
'''



