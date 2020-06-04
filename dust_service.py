import time
import datetime
import lib
import config
import main


def tick():
    while True:
        print(config.CoreServiceName + " service running: " +
              str(datetime.datetime.now()))
        time.sleep(config.Refresh_time)
        main.tick()


config.init()

print(config.CoreServiceName + " has booted: " + str(datetime.datetime.now()) +
      "\nVersion: " + str(config.Version))

tick()
