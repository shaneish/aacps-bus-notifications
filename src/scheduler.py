import schedule
from subprocess import run
import time
import pathlib
from configparser import ConfigParser
from twilio.rest import Client
from datetime import datetime
import os


configs = ConfigParser()
configs.read(pathlib.Path(__file__).parent / "configs.properties")
account_sid = configs["twilio"]["sid"]
auth_token = configs["twilio"]["auth"]
call_client = Client(os.environ[account_sid], os.environ[auth_token])


def run_notifier(call_client=call_client):
    print("running notifier")
    notifier = pathlib.Path(__file__).parent / "notifier.py"
    notifs = run(f"python {notifier}", shell=True)
    if notifs.returncode != 0:
        print("failed")
        call_client.messages.create(
                    body=f"Error: Notifier failed with code {notifs.returncode}",
                    from_=configs["debug"]["from_phone"],
                    to=configs["debug"]["to_phone"],
                )



def weekday_schedule(times=()):
    for time_slot in times:
        schedule.every().monday.at(time_slot).do(run_notifier)
        schedule.every().tuesday.at(time_slot).do(run_notifier)
        schedule.every().wednesday.at(time_slot).do(run_notifier)
        schedule.every().thursday.at(time_slot).do(run_notifier)
        schedule.every().friday.at(time_slot).do(run_notifier)


if __name__ == "__main__":
    weekday_schedule(
        times=(
            configs["schedule"]["morning"],
            configs["schedule"]["mid_noon"],
            configs["schedule"]["late_noon"],
            configs["schedule"]["evening"],
        )
    )
    run_notifier()

    while True:
        schedule.run_pending()
        time.sleep(1)
