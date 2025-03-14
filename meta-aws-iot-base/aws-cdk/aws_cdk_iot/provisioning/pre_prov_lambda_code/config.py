DEVICES_TABLE_NAME = 'devices'
DEVICES_TABLE_NAME_ID = 'devicesTable'

REQUESTS_TOPIC = 'iot/+/request'
REQUESTS_TOPIC_TEMPLATE = 'iot/%s/request'
RESPONSE_TOPIC_TEMPLATE = 'iot/%s/response'

DEVICES_TABLE_NAME_ENV = 'DEVICES_TABLE_NAME'
PERMANENT_ACCESS_KEY_SECRET_NAME_ENV = 'PERMANENT_ACCESS_KEY_SECRET_NAME'
PERMANENT_ACCESS_KEY_ID_ENV = 'PERMANENT_ACCESS_KEY_ID'


class DevicesTableFields:
    ID = "deviceId"
    DESCRIPTION = "description"
    SW_VERSION = "swVersion"
    LAST_CONNECTED = "lastConnected"


REQUEST_KEY = "request"
RESPONSE_KEY = "response"
SW_VERSION_KEY = "swVersion"
DATA_KEY = "data"

UPDATE_REQUEST_KEY = "update"
UPDATE_RESPONSE_KEY = "update"
ERROR_RESPONSE_KEY = "error"

LAMBDA_USER = "LambdaUser"
LAMBDA_ACCESS_KEY = "LambdaAccessKey"
LAMBDA_ACCESS_KEY_SECRET = "LambdaAccessKeySecret"
LAMBDA_REQUESTS = "LambdaRequests"

PRODUCTION_POLICY_NAME = "ProductionPolicy"
CLAIM_POLICY_NAME = "ClaimPolicy"
PROVISIONING_TEMPLATE_NAME = "IoTProvisioningTemplate"
