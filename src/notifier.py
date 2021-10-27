import requests
import json
from pprint import pprint
import os
from twilio.rest import Client


def format_notification(row, school):
    bus = f"Bus # -- {row[1]}"
    school = f"School -- {school}"
    sub = row[2] if row[2].strip() != "" else "NO SUB!"
    sub_bus = f"Sub # -- {sub}"
    time_slot = f"Time -- {row[4]}"
    impact = f"Impact -- {row[5]}"
    return "\n\n".join(["Affected Bus:", bus, school, sub_bus, time_slot, impact])
    

def get_number_iterator():
    return [("+14438894517", "71")]


def load_tokens(token_file):
    pass


def send_notification(phone_number, bus_number, bus_map, twilio_client):
    for bus, message in bus_map[bus_number].items():
        notification = twilio_client.messages.create(
                body=message,
                from_='+14433643381',
                to=phone_number)
        print(notification)


if __name__ == "__main__":
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    call_client = Client(account_sid, auth_token)

    # Welcome to the most dense, unpythonic code possible.
    # I know.  Sorry.
    # Extracts the table information from AACPS' bus website.
    data = json.loads(
        next(
            filter(
                lambda line: "var dataArray" in line,
                requests.get(
                    "https://busstops.aacps.org/public/BusRouteIssues.aspx"
                ).text.split("\n"),
            )
        )
        .split("=")[-1]
        .strip()[:-1]
        .replace("'", '"')
    )

    message_map = dict()
    reorg_map = dict()
    for row in data:
        reorg_map[row[1]] = dict()
        school = row[3]
        message_map[(row[1], school)] = format_notification(row, school)
    for key, val in message_map.items():
        reorg_map[key[0]][key[1]] = val

    for phone_num, bus_num in get_number_iterator():
        send_notification(phone_num, bus_num, reorg_map, call_client)
 