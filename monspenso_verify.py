import os
import json
import boto3

message_service = os.environ["message_service"]

ssm = boto3.client('ssm')

def lambda_handler(event, context):

    monzo_account = event["data"]["account_id"]
    monzo_account_id = get_secret('monzo_account_id')
    
    if monzo_account == monzo_account_id:
        return {
            "data": event["data"], 
            "valid": True,
            "message_service": message_service
        }
        
    else:
        return {
            "valid": False
        }

def get_secret(key):
	resp = ssm.get_parameter(
		Name=key,
		WithDecryption=True
	)
	return resp['Parameter']['Value']
            
