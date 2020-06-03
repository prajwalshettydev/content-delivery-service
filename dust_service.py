import time
import datetime
import sys
import lib
import os
import main
import config

sys.stderr = open(os.path.join(log_loc, 'log_err.txt'), 'w', 1)
sys.stdout = open(os.path.join(log_loc, 'log_out.txt'), 'w', 1)


def tick():
    main.tick()


def main_call():
    while True:
        print(config.CoreServiceName + " service running: " +
              str(datetime.datetime.now()))
        time.sleep(config.Refresh_time)


print(config.CoreServiceName + " has booted: " + str(datetime.datetime.now()) +
      "\nVersion: " + str(config.Version))

main_call()
