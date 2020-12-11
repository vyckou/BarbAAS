from twilio.rest import Client
import requests
import os


TWILIO_ACCOUNT_ID = os.environ.get("TWILIO_ACCOUNT_ID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_ACCOUNT_AUTH_TOKEN")
NUMBERS_TO_SEND_SMS = os.environ.get("TWILIO_NUMBERS_TO_SEND")
SERVICE_NUMBER_TO_SEND_SMS = os.environ.get("TWILIO_SERVICE_NUMBER_TO_SEND")

TWILIO_OUTGOING_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")    
MS_TEAMS_WEBHOOK = os.environ.get("MS_TEAMS_WEBHOOK")


def send_notifications(mesage):

    send_sms(f"{mesage}")
    send_message_to_teams(f"{mesage}")


def send_message_to_teams(message):
    if not MS_TEAMS_WEBHOOK:
        return

    message = {
        "@context": "http://schema.org/extensions",
        "@type": "MessageCard",
        "title": "Barbora Bot",
        "text": message,
    }
    requests.post(url=MS_TEAMS_WEBHOOK, json=message)

def send_sms(message):
    if not twilio_client:
        return

    for number in NUMBERS_TO_SEND_SMS.split(","):
        print(f"Sending SMS to {number} with the message {message}")
        twilio_client.messages.create(
            to=number,
            from_=TWILIO_OUTGOING_NUMBER,
            body=f"{message}",
        )

def send_service_sms(message):
    if not twilio_client:
        return

    twilio_client.messages.create(
        to=SERVICE_NUMBER_TO_SEND_SMS,
        from_=TWILIO_OUTGOING_NUMBER,
        body=f"{message}",
    )

if (
    TWILIO_ACCOUNT_ID
    and TWILIO_AUTH_TOKEN
    and TWILIO_OUTGOING_NUMBER
    and NUMBERS_TO_SEND_SMS
    and SERVICE_NUMBER_TO_SEND_SMS    
):
    twilio_client = Client(TWILIO_ACCOUNT_ID, TWILIO_AUTH_TOKEN)
    print(f"Twilio Numbers to send SMS: {NUMBERS_TO_SEND_SMS}")
    print(f"Twilio Service number to send SMS: {SERVICE_NUMBER_TO_SEND_SMS}")
    print(f"Twilio Outgoing Number: {TWILIO_OUTGOING_NUMBER}")
else:
    print(f"Twilio SMS Notifications disabled")

if MS_TEAMS_WEBHOOK:
    print(f"MS Teams Notifications Enabled")
else:
    print(f"MS Teams Notifications disabled")