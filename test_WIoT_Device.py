import unittest
from unittest.mock import Mock
import os
import WIoT_Device
import time


class TestPublish(unittest.TestCase):
    def test_publish(self):
        # TODO(losi): create temporary yml so as not to use TemperatureSensor.yml
        temp_pub = WIoT_Device.create_publisher("./config/TemperatureSensor.yml")
        test_published = Mock()
        pass_test = []  # It needs to be mutable
        temp_pub("testing", {}, test_published)
        time.sleep(5)
        test_published.assert_called_once()

    def test_subscribe(self):
        os.system(('curl -u <yourApiKey>:<yourApiPassword> '
                   '-H "Content-Type: text/plain" -v -X  POST '
                   'http://<yourOrg>.messaging.internetofthings.ibmcloud.com:1883/api/v0002/application/'
                   'types/<yourDeviceType>/devices/<yourDeviceId>/commands/gpio'
                   ' -d "on" '))
        test_subs_callback = Mock()
        temp_subs = WIoT_Device.create_subscriber("./config/TemperatureSensor.yml")
        temp_subs("testing", test_subs_callback)
        time.sleep(5)
        test_subs_callback.assert_called_once()

if __name__ == "__main__":
    unittest.main()

