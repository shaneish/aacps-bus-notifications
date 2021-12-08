import requests
import json
from pprint import pprint
from twilio.rest import Client
from configparser import ConfigParser
import pathlib
from datetime import datetime
import re
import os


def format_notification(row, school, col_map):
    bus = f"Bus # -- {row[col_map['bus']]}"
    school = f"School -- {school}"
    sub = row[col_map['sub bus']] if row[col_map['sub bus']].strip() != "" else "no sub!"
    sub_bus = f"Sub # -- {sub}"
    time_slot = f"Time -- {row[col_map['schedules']]}"
    impact = f"Impact -- {row[col_map['impact']]}"
    return "\n\n".join(["Affected Bus:", bus, time_slot, school, sub_bus, impact])

 
def validate_data(raw_data):
    data = raw_data.replace("\n", "").replace("\r", "").replace("\t", "")
    cols = json.loads(("[" + ", ".join(re.findall(r"columns: \[(.*?)\]", data)) + "]").lower())
    cols = [col['title'].strip() for col in cols]
    cols_map = {col: cols.index(col) for col in cols}
    return cols_map, 'bus' in cols and 'sub bus' in cols and 'schools' in cols and 'schedules' in cols and 'impact' in cols


def get_number_iterator(recipients_csv):
    # Reads the phone numbers currently just stored in a CSV
    with open(recipients_csv, "r") as recipients:
        users = [
            (
                r.split("|")[0],
                r.split("|")[1],
                r.split("|")[2],
                r.split("|")[3] if len(r.split("|")) > 3 else "F",
            )
            for r in recipients.read().split("\n")[1:]
            if len(r.split("|")) >= 3
        ]
    return users


def send_notification(
    phone_number,
    bus_number,
    school,
    always_notify,
    bus_map,
    twilio_client,
    twilio_number,
):
    for message in bus_map.get(bus_number, []):
        if school in message.lower():
            notification = twilio_client.messages.create(
                body=message, from_=twilio_number, to=phone_number
            )
            print(f"<U> {phone_number}, <M> {message}")
    if not bus_map.get(bus_number, []) and always_notify.lower() == "t":
        school_line = f" {school.title()} " if school != "" else " "
        message = f"Bus {bus_number}{school_line}is running as scheduled."
        notification = twilio_client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number,
        )
        print(f"<U> {phone_number}, <M> {message}")


if __name__ == "__main__":
    current_dir = pathlib.Path(__file__).parent
    configs = ConfigParser()
    configs.read(current_dir / "configs.properties")
    account_sid = configs["twilio"]["sid"]
    auth_token = configs["twilio"]["auth"]
    call_client = Client(os.environ[account_sid], os.environ[auth_token])

    # Welcome to the most dense, unpythonic code possible.
    # I know.  Sorry.
    # Extracts the table information from AACPS' bus website.
    raw_data = requests.get(configs["general"]["site"]).text
    
    # log current schedule
    log_folder = current_dir / "logs"
    log_file = log_folder / f"{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}-logs.html"
    with open(log_file, 'w') as log:
        log.write(raw_data.strip().replace("\r", ""))

    # delete old logs past threshold
    logs = [log_folder / log for log in os.listdir(log_folder)]
    if len(logs) >= int(configs["general"]["log_threshold"]):
        oldest_file = min(logs, key=os.path.getctime)
        os.remove(os.path.abspath(oldest_file))
    
    col_map, valid_data = validate_data(raw_data)
    if valid_data:
        data = json.loads(
            next(
                filter(
                    lambda line: "var dataArray" in line,
                    raw_data.split("\n")  # returns the line of the raw HTML that contains the table data
                )
            )
            .split("=")[-1]  # drops the "var dataArray = " part of the line
            .strip()[:-1]  # removes the trailing bracket
            .replace("'", '"')  # replaces single quotes with double quotes
        )

        # create a mapping from bus number to all outages for that particular bus
        message_map = dict()
        for row in data:
            message_map[row[col_map['bus']]] = message_map.get(row[col_map['bus']], []) + [
                format_notification(row, row[col_map["schools"]], col_map)
            ]

        # iterate over every recipient listed in the recipients file and send notification it here is an outage
        for phone_num, bus_num, school, always_notify in get_number_iterator(
            current_dir / configs['general']['users']
        ):
            try:
                send_notification(
                    phone_num,
                    bus_num,
                    school,
                    always_notify,
                    message_map,
                    call_client,
                    configs["twilio"]["from_phone"],
                )
            except Exception as e:
                print(f">>> Error: {e}")
                call_client.messages.create(
                    body=f"Bus Error: {e} / Phone: {phone_num} / Bus: {bus_num} / School: {school}",
                    from_=configs["debug"]["from_phone"],
                    to=configs["debug"]["to_phone"],
                )
    else:
       call_client.messages.create(
                    body=f"Error: Table does not have proper schema.\n\n{json.dumps(cols)}",
                    from_=configs["debug"]["from_phone"],
                    to=configs["debug"]["to_phone"],
                ) 