import requests
import json
import sys
import datetime
import os
import notifications
import time

USERNAME = os.environ["BARBORA_USERNAME"]
PASSWORD = os.environ["BARBORA_PASSWORD"]

SESSION = requests.Session()

BARBORA_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Authorization": "Basic YXBpa2V5OlNlY3JldEtleQ==",
    "Connection": "keep-alive",
    "Host": "www.barbora.lt",
    "Referer": "https://www.barbora.lt/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

BARBORA_URL_API = "https://barbora.lt"

def get_cookie(username, password):
    endpoint = f"{BARBORA_URL_API}/api/eshop/v1/user/login"
    payload = dict(email=username, password=password, rememberMe='true')

    SESSION.cookies.set("region", "barbora.lt")
    response = SESSION.post(url=endpoint, data=payload, headers=BARBORA_HEADERS)
    response.raise_for_status()
    return response.cookies

def find_slots_by_hour(slot_by_day):
    if 'hours' not in slot_by_day:
        print("malformed response, missing 'hours'")
        return

    slots = []
    for slot_by_hour in slot_by_day['hours']:
        if not slot_by_hour.get("available"):
            continue
        slots.append(f"{slot_by_day.get('id')} at {slot_by_hour.get('hour')}")
    return slots


def find_free_slots(response_body):
    if 'deliveries' not in response_body:
        return "malformed response, missing 'deliveries'"
    if 'params' not in response_body['deliveries'][0]:
        return "malformed response missing 'params'"
    if 'matrix' not in response_body['deliveries'][0]['params']:
        return "malformed response missing 'matrix'"

    slots_during_period = []
    for slot_by_day in response_body['deliveries'][0]['params']['matrix']:
        available_slots_by_hour = find_slots_by_hour(slot_by_day)
        if not available_slots_by_hour:
            continue
        slots_during_period += available_slots_by_hour

    return slots_during_period


def get_delivery_data():
    global COOKIE
    try:
        r = SESSION.get(f"{BARBORA_URL_API}/api/eshop/v1/cart/deliveries", headers=BARBORA_HEADERS, cookies=COOKIE)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        raise err
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)

    return

COOKIE = get_cookie(USERNAME,PASSWORD)