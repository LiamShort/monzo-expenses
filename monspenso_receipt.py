import json
import boto3
import os
import datetime
import urllib.request

s3 = boto3.client("s3")

bucket_name = os.environ["bucket_name"]

def lambda_handler(event, context):

    monzo_receipt = event["data"]["attachments"]

    urllib.request.urlretrieve(monzo_receipt, "/tmp/receipt.jpg")

    datetime_string = datetime.datetime.now().strftime("%d%m%H%M")
    
    local_filename = "/tmp/receipt.jpg"
    remote_filename = "receipt-" + datetime_string + ".jpg"
    bucket_name = "monspenso-receipts"
    
    s3.upload_file(local_filename, bucket_name, "receipts/" + remote_filename)
    
    receipt_url = "https://s3-eu-west-1.amazonaws.com/" + bucket_name + "/receipts/receipt-" + datetime_string + ".jpg"
       
    return {
            "data": event["data"],
            "receipt_url": receipt_url
    }