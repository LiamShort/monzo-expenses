# monzo_account_id

import os
import json
import boto3

ssm = boto3.client('ssm')

def lambda_handler(event, context):

    monzo_account_id = get_secret('monzo_account_id')
    monzo_account = event["data"]["account_id"]
    
    if monzo_account == monzo_account_id:
        return (event)
        
    else:
        return (event)

def get_secret(key):
	resp = ssm.get_parameter(
		Name=key,
		WithDecryption=True
	)
	return resp['Parameter']['Value']
            
