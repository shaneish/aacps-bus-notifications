import requests
import json
from pprint import pprint
import os
from twilio.rest import Client
from configparser import ConfigParser
import pathlib


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


def send_notification(phone_number, bus_number, bus_map, school, twilio_client, twilio_number):
    # for message in bus_map.get(bus_number, []):
    for message in bus_map[bus_number]:
        if school in message.lower():
            notification = twilio_client.messages.create(
                body=message, from_=twilio_number, to=phone_number
            )
            print(f">>> Transmitting msg to {notification.to}")


if __name__ == "__main__":
    current_dir = pathlib.Path(__file__).parent
    configs = ConfigParser()
    configs.read(current_dir / "configs.properties")
    account_sid = os.environ[configs["twilio"]["sid"]]
    auth_token = os.environ[configs["twilio"]["auth"]]
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
        try:
            send_notification(phone_num, bus_num, message_map, school, call_client, configs["twilio"]["from_phone"])
        except Exception as e:
            print(f">>> Error: {e}")
            call_client.messages.create(
                body=f"Bus Error: {e}", from_=configs["debug"]["from_phone"], to=configs["debug"]["to_phone"]
            )