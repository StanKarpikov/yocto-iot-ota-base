import json
import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prov")

TOPIC_CERT_REJECT = "$aws/certificates/create/json/rejected"
TOPIC_CERT_ACCEPT = "$aws/certificates/create/json/accepted"
TOPIC_PROVISION_ACCEPT = f"$aws/provisioning-templates/{PROVISIONING_TEMPLATE_NAME}/provision/json/accepted"
TOPIC_PROVISION_REJECT = f"$aws/provisioning-templates/{PROVISIONING_TEMPLATE_NAME}/provision/json/rejected"

THING_NAME_REQUEST_TEMPLATE = '''
{
    "certificateOwnershipToken": "%s",
    "parameters": {
        "SerialNumber": "%s"
    }
}
'''

TOKEN_SIZE = 500
THING_NAME_LEN_MAX = 128

# MQTT Configuration
CERTIFICATE_REQUEST_PUBLISH_TOPIC = "$aws/certificates/create/json"
CERTIFICATE_REQUEST_PAYLOAD = "{}"
CERTIFICATE_REQUEST_QOS = 1

THING_PUBLISH_TOPIC = f"$aws/provisioning-templates/{PROVISIONING_TEMPLATE_NAME}/provision/json"
THING_REQUEST_QOS = 1

certificate_storage = {
    "private_key": None,
    "certificate": None,
    "ownership_token": None
}

def mqtt_publish(topic, payload, qos):
    logger.info(f"Publishing to {topic}: {payload} (QoS: {qos})")
    # Simulated MQTT publish function


def mqtt_subscribe(topic, callback):
    logger.info(f"Subscribing to {topic}")
    # Simulated MQTT subscription


def on_init_request_credentials():
    global provisioning_timer
    logger.info("Requesting certificate/private key")

    mqtt_publish(CERTIFICATE_REQUEST_PUBLISH_TOPIC, CERTIFICATE_REQUEST_PAYLOAD, CERTIFICATE_REQUEST_QOS)


def on_request_thing_name():
    logger.info("Requesting thing name")
    
    thing_name = "MyDeviceThing"
    request_payload = THING_NAME_REQUEST_TEMPLATE % (certificate_storage["ownership_token"], thing_name)
    mqtt_publish(THING_PUBLISH_TOPIC, request_payload, THING_REQUEST_QOS)



def iot_subscribe_callback_handler_cert_accept(payload):
    try:
        data = json.loads(payload)
        certificate_storage["private_key"] = data.get("privateKey")
        certificate_storage["certificate"] = data.get("certificatePem")
        certificate_storage["ownership_token"] = data.get("certificateOwnershipToken")
    except json.JSONDecodeError:
        logger.error("Invalid JSON received in certificate acceptance")


def iot_subscribe_callback_handler_provision_accept(payload):
    try:
        data = json.loads(payload)
        thing_name = data.get("thingName")
    except json.JSONDecodeError:
        logger.error("Invalid JSON received in provisioning acceptance")


if __name__ == "__main__":
    provisioning_start()
