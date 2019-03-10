import os
import json
from botocore.vendored import requests

webhook_url = os.environ["webhook_url"]

def lambda_handler(event, context):

    message = event["message"]

    send_message(message)
    
def send_message(message):

    response = requests.post(
        webhook_url, data= json.dumps(message),
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()