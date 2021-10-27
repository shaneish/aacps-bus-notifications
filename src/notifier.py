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
    return "\n\n".join(["Affected Bus:", bus, time_slot, school, sub_bus, impact])


def get_number_iterator():
    return [("+14438894517", "71", "jessup")]


def send_notification(phone_number, bus_number, bus_map, school, twilio_client):
    for message in bus_map[bus_number]:
        if school in message.lower():
            notification = twilio_client.messages.create(
                body=message, from_="+14433643381", to=phone_number
            )
            print(notification.to)
            print(notification.status)
            print(notification.body)


if __name__ == "__main__":
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
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
    for row in data:
        school = row[3]
        message_map[row[1]] = message_map.get(row[1], []) + [
            format_notification(row, school)
        ]

    for phone_num, bus_num, school in get_number_iterator():
        send_notification(phone_num, bus_num, message_map, school, call_client)
