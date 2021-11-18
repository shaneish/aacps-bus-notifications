import schedule
from subprocess import run
import time
import pathlib
from configparser import ConfigParser


def run_notifier():
    notifier = pathlib.Path(__file__).parent / "notifier.py"
    run(f"python {notifier}", shell=True)


def weekday_schedule(times=()):
    for time_slot in times:
        schedule.every().monday.at(time_slot).do(run_notifier)
        schedule.every().tuesday.at(time_slot).do(run_notifier)
        schedule.every().wednesday.at(time_slot).do(run_notifier)
        schedule.every().thursday.at(time_slot).do(run_notifier)

    for time_slot in times[:-1]:
        schedule.every().friday.at(time_slot).do(run_notifier)

    schedule.every().sunday.at(times[-1]).do(run_notifier)


if __name__ == "__main__":
    current_dir = pathlib.Path(__file__).parent
    configs = ConfigParser()
    configs.read(current_dir / "configs.properties")
    weekday_schedule(times=(configs["schedule"]["morning"], configs["schedule"]["afternoon"], configs["schedule"]["evening"]))

    while True:
        schedule.run_pending()
        time.sleep(1)
