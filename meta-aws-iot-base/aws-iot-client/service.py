import json
import logging
import time
from config import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = AWS_HOST
rootCAPath = ROOT_CA_PATH
certificatePath = CERTIFICATE_PATH
privateKeyPath = KEY_PATH
port = 8883
device_id = CLIENT_ID

logger = logging.getLogger("aws-iot")
logger.setLevel(logging.INFO)


def message_callback(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


def subscribe_ack_callback(mid, data):
    print("Received SUBACK packet id: ")
    print(mid)
    print("Granted QoS: ")
    print(data)
    print("++++++++++++++\n\n")


def publish_callback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")


if not certificatePath or not privateKeyPath:
    logger.error("Missing credentials for authentication.")
    exit(2)

client = AWSIoTMQTTClient(device_id)
client.configureEndpoint(host, port)
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec
client.onMessage = message_callback

client.connect()
client.subscribeAsync(RESPONSE_TOPIC_TEMPLATE % device_id, 1, ackCallback=subscribe_ack_callback)
time.sleep(2)

while True:
    message = {
        REQUEST_KEY: UPDATE_REQUEST_KEY,
        DATA_KEY: {
            SW_VERSION_KEY: "1.0"
        }
    }
    message_str = json.dumps(message)
    client.publishAsync(REQUESTS_TOPIC_TEMPLATE % device_id, message_str, 1, ackCallback=publish_callback)
    time.sleep(10)
