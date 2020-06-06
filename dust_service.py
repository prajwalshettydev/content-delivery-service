import time
import datetime
import lib
import config
import main


def tick():
    while True:
        print("\n" + config.core_service_name + " service running: " + str(datetime.datetime.now()) +
              "\nTick frequency: " + str(config.tick_frequency))
        main.tick()

        time.sleep(config.tick_frequency.seconds)


config.init()

print(config.core_service_name + " has booted: " + str(datetime.datetime.now()) +
      "\nVersion: " + str(config.version))
tick()
