import json
import logging
import os
from datetime import datetime, timezone, timedelta
from typing import Callable

import boto3
from botocore.exceptions import ClientError
from config import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DatabaseAdapter:

    def __init__(self, table_name: str):
        self.client = boto3.client("dynamodb")
        self.table_name = table_name

    @staticmethod
    def iso_time_string():
        current_time = datetime.now(timezone.utc)
        return str(current_time.isoformat())

    def check_exists(self, device_id: str):
        item = self.client.get_item(
            TableName=self.table_name,
            Key={
                DevicesTableFields.ID: {"S": device_id},
            },
        )
        value = item["Item"][DevicesTableFields.SW_VERSION]["S"]
        return value

    def update_record(self, device_id: str, sw_version: str):
        try:
            self.check_exists(device_id)
            self.client.update_item(
                TableName=self.table_name,
                Key={
                    DevicesTableFields.ID: {"S": device_id},
                },
                UpdateExpression=f"SET {DevicesTableFields.SW_VERSION} = :sw, {DevicesTableFields.LAST_CONNECTED} = :lastconn",
                ExpressionAttributeValues={
                    ":sw": {"S": str(sw_version)},
                    ":lastconn": {"S": self.iso_time_string()},
                }
            )
        except Exception as e:
            logger.info(f'Creating a record for {device_id}, assume not exist: {e}')
            self.client.put_item(
                TableName=self.table_name,
                Item={
                    DevicesTableFields.ID: {"S": device_id},
                    DevicesTableFields.DESCRIPTION: {"S": ""},
                    DevicesTableFields.SW_VERSION: {"S": sw_version},
                    DevicesTableFields.LAST_CONNECTED: {"S": self.iso_time_string()},
                },
            )


class Controller:

    def __init__(self,
                 device_id: str,
                 key_id: str,
                 key_secret_name: str,
                 region: str,
                 account_id: str,
                 ids_table_name: str):
        self._key_id = key_id
        self._key_secret_name = key_secret_name
        self._region = region
        self._account_id = account_id
        self._ids_table_name = ids_table_name
        self._device_id = device_id

        self._database = DatabaseAdapter(DEVICES_TABLE_NAME)

        self._requests: dict[str, Callable[[str, dict | str | list], None]] = {
            UPDATE_REQUEST_KEY: self._request_update
        }

    def _send_response(self, response: str, data: dict | str):
        client = boto3.client('iot-data',
                              region_name=self._region,
                              aws_access_key_id=self._key_id,
                              aws_secret_access_key=self._key_secret_name)
        topic = RESPONSE_TOPIC_TEMPLATE % self._device_id
        data = json.dumps(
            {
                RESPONSE_KEY: response,
                DATA_KEY: data
            }
        )
        logging.info(f'Response\n{data}\nto:\n{topic}')
        client.publish(topic=topic, payload=data)

    def _request_update(self, request: str, data: str | dict | list):
        logging.info('Get Update Request')
        sw_version = data[SW_VERSION_KEY]
        self._database.update_record(device_id=self._device_id, sw_version=sw_version)
        self._send_response(response=UPDATE_RESPONSE_KEY, data="ok")

    def _error_response(self, request: str, error: str):
        self._send_response(response=ERROR_RESPONSE_KEY,
                            data={"request": request, "error": error})

    def process(self, event):
        try:
            request = event['request']
        except Exception as e:
            logger.error("No request provided")
            return

        try:
            data = event['data']
        except Exception as e:
            logger.error("No data provided")
            return

        if request in self._requests:
            try:
                self._requests[request](request, data)
            except Exception as e:
                logging.error(f"Error processing {request}")
                self._error_response(request, f"Error processing: {e}")
        else:
            logging.error(f"Request {request} not found")
            self._error_response(request, "Not Found")


def get_secret(region, secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        raise ValueError("secret must be a string")
    return secret


# Request format:
# {"request": "<string request type>", "data": "<data>"}
# sent to
# iot/<device id>/request

# Response format:
# {"response": "<string response type>", "data": "<data>"}
# sent to
# iot/<device id>/response

def lambda_handler(event, context):
    logging.info(f'Event: {str(event)}')
    logging.info(f'Context: {str(context)}')

    device_id = ""  # TODO: extract from topic
    account_id = context.invoked_function_arn.split(":")[4]
    region = context.invoked_function_arn.split(":")[3]
    key_id = os.environ[PERMANENT_ACCESS_KEY_ID_ENV]
    ids_table_name = os.environ[IDS_TABLE_NAME_ENV]
    key_secret_name = get_secret(region, os.environ[PERMANENT_ACCESS_KEY_SECRET_NAME_ENV])
    controller = Controller(device_id=device_id,
                            key_id=key_id,
                            key_secret_name=key_secret_name,
                            region=region,
                            account_id=account_id,
                            ids_table_name=ids_table_name)
    controller.process(event)
