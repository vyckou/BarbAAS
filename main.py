from twilio.rest import Client
import requests
import os
import json
import re
import time
import sys
import datetime
import traceback
import notifications
import barbora
import random

HOURS_TO_SLEEP = int(os.environ.get("HOURS_TO_SLEEP_AFTER_GETTING_SLOT", "6"))
NOTIFICATIONS_TO_SEND = int(os.environ.get("NOTIFICATIONS_TO_SEND", "1"))

DRY_RUN = os.environ.get("DRY_RUN")

PUSH_BACK_SECONDS = int(os.environ.get("PUSH_BACK_BARBORA_API_IN_SECONDS", "60"))
sleep_long_as_informed = HOURS_TO_SLEEP * 60 * 60 * 1

print(f"Now: {datetime.datetime.now()}")



def run():

    NOTIFICATIONS_THROTTLE = NOTIFICATIONS_TO_SEND

    if DRY_RUN:
        with open('barbora.json') as mock:
            payload = mock.read()
            response = json.loads(payload)    

    while True:

        time.sleep(random.randint(60, 120))
        if NOTIFICATIONS_THROTTLE == 0:
            NOTIFICATIONS_THROTTLE = NOTIFICATIONS_TO_SEND
            print(f"Going to sleep for {HOURS_TO_SLEEP} hours")
            notifications.send_message_to_teams(f"Going for sleep for {HOURS_TO_SLEEP} hours")
            time.sleep(sleep_long_as_informed)

        today = time.ctime()

        if not DRY_RUN:
            response = barbora.get_delivery_data()

        try:
            resp_str = json.dumps(response)
        except Exception as e:
            print(f"Was not able to parse response. Error: {e}")
            continue

        if not response:
            continue

        slots_during_period= barbora.find_free_slots(response)

        if not slots_during_period:
            continue
        
        print(f"Slot found at {today}")
        if not DRY_RUN:
            string_with_new_lines = ",".join(slots_during_period)
            notifications.send_notifications(f"Available time:{string_with_new_lines}")
        print(slots_during_period)            
        NOTIFICATIONS_THROTTLE = NOTIFICATIONS_THROTTLE - 1

try:
    run()
except Exception as ex:
    print(ex)
    traceback.print_exc()
    notifications.send_service_sms("Bot got exception and exited")