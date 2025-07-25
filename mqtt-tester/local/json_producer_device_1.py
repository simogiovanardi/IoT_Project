# For this example we rely on the Paho MQTT Library for Python
# You can install it through the following command: pip install paho-mqtt

from model.temperature_sensor import TemperatureSensor
from model.message_descriptor import MessageDescriptor
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion  # Add this import
import time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))

# Full MQTT client creation with all the parameters. The only one mandatory in the ClientId that should be unique
# mqtt_client = Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)

print(dir(CallbackAPIVersion))

# Configuration variables
device_id = "test_device_1"
client_id = "clientId0001-Producer"
broker_ip = "127.0.0.1"
broker_port = 1883
default_topic = "device/{}/temperature".format(device_id)
message_limit = 1000

mqtt_client = mqtt.Client(client_id=client_id, callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect

print("Connecting to "+ broker_ip + " port: " + str(broker_port))
mqtt_client.connect(broker_ip, broker_port)

mqtt_client.loop_start()

# Create Demo Temperature Sensor
temperature_sensor = TemperatureSensor()

# MQTT Paho Publish method with all the available parameters
# mqtt_client.publish(topic, payload=None, qos=0, retain=False)

for message_id in range(message_limit):
    temperature_sensor.measure_temperature()
    payload_string = MessageDescriptor(int(time.time()),
                                       "TEMPERATURE_SENSOR",
                                       temperature_sensor.temperature_value).to_json()
    infot = mqtt_client.publish(default_topic, payload_string)
    infot.wait_for_publish()
    print(f"Message Sent: {message_id} Topic: {default_topic} Payload: {payload_string}")
    time.sleep(5)

mqtt_client.loop_stop()
