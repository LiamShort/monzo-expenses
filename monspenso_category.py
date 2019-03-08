# monzo_access_key

import os
import json
import datetime
import boto3
from botocore.vendored import requests

ssm = boto3.client('ssm')

def lambda_handler(event, context):

    monzo_transaction_id = event['data']['id']
    url = "https://api.monzo.com/transactions/" + monzo_transaction_id
    
    monzo_access_key = get_secret('monzo_access_key')
    response = requests.get(
        url, 
        headers={"Authorization": "Bearer " + monzo_access_key}
    )
    
    response_json = (response.json())

    monzo_category = response_json["transaction"]["category"]

    if monzo_category == "expenses":
        monzo_note = "No Note"
        if response_json["transaction"]["notes"]:
            monzo_note = response_json["transaction"]["notes"]

        monzo_receipt = "No Receipt"
        if response_json["transaction"]["attachments"]:
            for attachment in response_json["transaction"]["attachments"]:
                if "file_url" in attachment:
                    print(attachment["file_url"])
                    monzo_receipt = attachment["file_url"]

    event["data"]["category"] = monzo_category
    event["data"]["notes"] = monzo_note
    event["data"]["attachments"] = monzo_receipt
    
    return(event)

def get_secret(key):
	resp = ssm.get_parameter(
		Name=key,
		WithDecryption=True
	)
	return resp['Parameter']['Value']
