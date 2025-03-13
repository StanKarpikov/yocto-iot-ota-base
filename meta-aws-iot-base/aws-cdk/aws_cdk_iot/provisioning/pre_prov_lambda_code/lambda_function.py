import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logging.info(f'Event: {str(event)}')
    logging.info(f'Context: {str(context)}')
    return {
            'allowProvisioning': True
           }

