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
call_client = Client(
    os.environ[configs["twilio"]["sid"]], os.environ[configs["twilio"]["auth"]]
)


def run_notifier_compare(call_client=call_client):
    print("[info] running notifier")
    notifier = pathlib.Path(__file__).parent / "notifier.py"
    notifs = run(f"python {str(notifier)} -l -c", shell=True)
    if notifs.returncode != 0:
        print("failed")
        call_client.messages.create(
            body=f"Error: Notifier failed with code {notifs.returncode}",
            from_=configs["debug"]["from_phone"],
            to=configs["debug"]["to_phone"],
        )


def run_notifier_no_compare(call_client=call_client):
    print("[info] running notifier")
    notifier = pathlib.Path(__file__).parent / "notifier.py"
    notifs = run(f"python {str(notifier)} -l -p Tomorrow", shell=True)
    if notifs.returncode != 0:
        print("failed")
        call_client.messages.create(
            body=f"Error: Notifier failed with code {notifs.returncode}",
            from_=configs["debug"]["from_phone"],
            to=configs["debug"]["to_phone"],
        )


def run_notifier_on_start(call_client=call_client):
    print("[info] running notifier")
    notifier = pathlib.Path(__file__).parent / "notifier.py"
    notifs = run(f"python {str(notifier)} -a", shell=True)
    if notifs.returncode != 0:
        print("failed")
        call_client.messages.create(
            body=f"Error: Notifier failed with code {notifs.returncode}",
            from_=configs["debug"]["from_phone"],
            to=configs["debug"]["to_phone"],
        )


def weekday_schedule(times=(), notifier=run_notifier_compare):
    for time_slot in times:
        schedule.every().monday.at(time_slot).do(notifier)
        schedule.every().tuesday.at(time_slot).do(notifier)
        schedule.every().wednesday.at(time_slot).do(notifier)
        schedule.every().thursday.at(time_slot).do(notifier)
        schedule.every().friday.at(time_slot).do(notifier)


if __name__ == "__main__":
    morning_times = configs["schedule"]["morning"].split(",")
    noon_times = configs["schedule"]["afternoon"].split(",")
    evening_times = configs["schedule"]["evening"].split(",")
    scheduled_times = tuple(morning_times + noon_times + evening_times)
    print(scheduled_times)
    weekday_schedule(
        times=scheduled_times
    )
    weekday_schedule(
        times=tuple(evening_times),
        notifier=run_notifier_no_compare,  # on first evening look for next day, don't compare to current day
    )
    run_notifier_on_start()  # send notifications only to all 'always notify' users

    while True:
        schedule.run_pending()
        time.sleep(1)
