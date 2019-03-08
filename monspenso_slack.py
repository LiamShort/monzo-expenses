# amount_high
# amount_medium
# channel
# slack_webhook

import json
import os
import datetime
from botocore.vendored import requests

slack_webhook = os.environ["slack_webhook"]
amount_high = os.environ["amount_high"]
amount_medium = os.environ["amount_medium"]
channel = os.environ["channel"]

def lambda_handler(event, context):
    
    response_data = event["monzo"]["response"]
    
    monzo_transaction = response_data["transaction"]
    
    monzo_created_datettime = datetime.datetime.strptime(monzo_transaction["created"], "%Y-%m-%dT%H:%M:%S.%fZ")

    monzo_amount_original = str(monzo_transaction["local_amount"]).replace("-", "")
    monzo_amount_length = int(len(monzo_amount_original) - 2)
    monzo_amount = float(monzo_amount_original[:monzo_amount_length] + "." + monzo_amount_original[monzo_amount_length:])
    monzo_created = monzo_created_datettime.strftime("%Y/%m/%d")
    monzo_currency = monzo_transaction["local_currency"]
    
    
    monzo_merchant = "No Merchant"
    monzo_city = "No City"

    monzo_note = monzo_transaction["notes"]
    if monzo_note == "":
        monzo_note = "No Note"

    #monzo_city = monzo_transaction["merchant"]["address"]["city"]
    #if monzo_city == "":
        #monzo_city = "No City"

    monzo_receipt = "No Receipt"
    for attachment in monzo_transaction["attachments"]:
        if "file_url" in attachment:
            monzo_receipt = attachment["file_url"]
    
    slack_message_colour = get_slack_colour(monzo_amount)
    slack_message = create_slack_message(monzo_merchant, monzo_amount, monzo_created, monzo_note, monzo_city, monzo_currency, monzo_receipt, slack_message_colour)
    send_slack_notification(slack_message)

def get_slack_colour(monzo_amount):

    if monzo_amount >= float(amount_high):
        slack_message_colour = '#ad0614'

    elif monzo_amount >= float(amount_medium):
        slack_message_colour = '#e2d43b'

    else:
        slack_message_colour = '#7CD197'

    return(slack_message_colour)

def create_slack_message(monzo_merchant, monzo_amount, monzo_created, monzo_note, monzo_city, monzo_currency, monzo_receipt, slack_message_colour):

    current_date = (datetime.datetime.now()).strftime("%Y-%m-%d")

    slack_message = {
        "icon_url": "https://github.com/twitter/twemoji/blob/gh-pages/72x72/1f4b0.png?raw=true",
        "username": "Expense",
        "channel": channel,
        "attachments": [{
            "pretext": "Monzo Expense Application",
            "color": slack_message_colour,
            "title": current_date + " " + monzo_merchant + " Expense",
            "title_link": "https://login.salesforce.com/?locale=uk",
            "footer": "Submit to Salesforce ASAP",
            "fields": [
                {'title': "Merchant", "value": monzo_merchant, "short": "true"},
                {'title': "Location", "value": monzo_city, "short": "true"},
                {'title': "Value", "value": monzo_amount, "short": "true"},
                {'title': "Currency", "value": monzo_currency, "short": "true"},
                {'title': "Date", "value": monzo_created, "short": "true"},
                {'title': "Note", "value": monzo_note}
            ],
            "footer_icon": "https://github.com/twitter/twemoji/blob/gh-pages/72x72/1f4b0.png?raw=true",
            "image_url": monzo_receipt
            }
        ]}

    return(slack_message)

def send_slack_notification(slack_message):

    response = requests.post(
        slack_webhook, data=json.dumps(slack_message),
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()