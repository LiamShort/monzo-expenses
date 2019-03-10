import json
import os
import datetime
from botocore.vendored import requests

amount_high = os.environ["amount_high"]
amount_medium = os.environ["amount_medium"]

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
    message = create_teams_message(monzo_merchant, monzo_amount, monzo_created, monzo_note, monzo_city, monzo_currency, monzo_receipt, message_colour)

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

def create_teams_message(monzo_merchant, monzo_amount, monzo_created, monzo_note, monzo_city, monzo_currency, monzo_receipt, message_colour):

    current_date = (datetime.datetime.now()).strftime("%Y-%m-%d")

    message = {
        "@context": "https://schema.org/extensions",
        "@type": "MessageCard",
        "sections": [
            {
                "facts": [
                    {
                        "name": "Merchant",
                        "value": monzo_merchant
                    },
                    {
                        "name": "Location",
                        "value": monzo_city
                    },
                    {
                        "name": "Value",
                        "value": monzo_amount
                    },
                    {
                        "name": "Currency",
                        "value": monzo_currency
                    },
                    {
                        "name": "Date",
                        "value": monzo_created
                    },
                    {
                        "name": "Note",
                        "value": monzo_note
                    }
                ],
            }
        ],
        "summary": "Expense Submitted",
        "themeColor": message_colour,
        "title": current_date + " " + monzo_merchant + " Expense",
        "potentialAction": [
            {
              "@type": "OpenUri",
              "name": "Receipt",
              "targets": [
                { "os": "default", "uri": monzo_receipt }
              ]
            }
        ]
    }

    return(message)