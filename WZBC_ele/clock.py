import schedule
import datetime
from get_today_ele import run

def job1():
    print("I'm working for job1",datetime.datetime.now())
    try:
        run()
    except:
        print("job1: break",datetime.datetime.now())
    else:
        print("job1:", datetime.datetime.now())

schedule.every(10).minutes.do(job1)
while True:
    schedule.run_pending()
