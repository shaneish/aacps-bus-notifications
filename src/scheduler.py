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
        schedule.every().friday.at(time_slot).do(run_notifier)


if __name__ == "__main__":
    configs = ConfigParser()
    configs.read(pathlib.Path(__file__).parent / "configs.properties")
    weekday_schedule(
        times=(
            configs["schedule"]["morning"],
            configs["schedule"]["mid_noon"],
            configs["schedule"]["late_noon"],
            configs["schedule"]["evening"],
        )
    )

    while True:
        schedule.run_pending()
        time.sleep(1)
