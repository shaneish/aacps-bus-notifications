import schedule
from subprocess import run
import time
import pathlib


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
    weekday_schedule(times=("00:50", "07:30", "14:00", "20:00"), command="python notifier.py")

    while True:
        schedule.run_pending()
        time.sleep(1)
