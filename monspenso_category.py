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
    event["monzo"] = {"category": monzo_category, "response": response_json}
    
    return(event)

def get_secret(key):
	resp = ssm.get_parameter(
		Name=key,
		WithDecryption=True
	)
	return resp['Parameter']['Value']
