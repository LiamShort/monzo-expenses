import json
import os
import datetime

amount_high = os.environ["amount_high"]
amount_medium = os.environ["amount_medium"]
channel = os.environ["channel"]

def lambda_handler(event, context):
    
    monzo_transaction = event["data"]
    
    monzo_created_datettime = datetime.datetime.strptime(monzo_transaction["created"], "%Y-%m-%dT%H:%M:%S.%fZ")

    monzo_amount_original = str(monzo_transaction["local_amount"]).replace("-", "")
    monzo_amount_length = int(len(monzo_amount_original) - 2)
    monzo_amount = float(monzo_amount_original[:monzo_amount_length] + "." + monzo_amount_original[monzo_amount_length:])
    monzo_created = monzo_created_datettime.strftime("%Y/%m/%d")
    monzo_currency = monzo_transaction["local_currency"]
    monzo_note = monzo_transaction["notes"]
    monzo_receipt = monzo_transaction["attachments"]

    monzo_merchant = "No Merchant"
    monzo_city = "No City"
    if monzo_transaction["merchant"]:
        if "name" in monzo_transaction["merchant"]:
            monzo_merchant = monzo_transaction["merchant"]["name"]

        if "address" in monzo_transaction["merchant"]:
            monzo_city = monzo_transaction["merchant"]["address"]["city"]
    
    message_colour = get_message_colour(monzo_amount)
    message = create_slack_message(monzo_merchant, monzo_amount, monzo_created, monzo_note, monzo_city, monzo_currency, monzo_receipt, message_colour)
    
    return {
            "message": message
        }

def get_message_colour(monzo_amount):

    if monzo_amount >= float(amount_high):
        message_colour = '#ad0614'

    elif monzo_amount >= float(amount_medium):
        message_colour = '#e2d43b'

    else:
        message_colour = '#7CD197'

    return(message_colour)

def create_slack_message(monzo_merchant, monzo_amount, monzo_created, monzo_note, monzo_city, monzo_currency, monzo_receipt, message_colour):

    current_date = (datetime.datetime.now()).strftime("%Y-%m-%d")

    message = {
        "icon_url": "https://github.com/twitter/twemoji/blob/gh-pages/72x72/1f4b0.png?raw=true",
        "username": "Expense",
        "channel": channel,
        "attachments": [{
            "pretext": "Monzo Expense Application",
            "color": message_colour,
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

    return(message)