import sys
from apscheduler.schedulers.blocking import BlockingScheduler

def some_job():
    print("Decorated job")

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(some_job, 'interval', seconds=2)
    scheduler.start()

    return 0

if __name__ == "__main__":
    sys.exit(main())
