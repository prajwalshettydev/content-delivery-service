import time
import datetime
import lib
import config
import main


def tick():
    while True:
        try:
            print("\n" + config.core_service_name +
                  " service running: " + str(datetime.datetime.now()))
            main.tick()
        except Exception as e:
            print("=========\nDUH, DUH!, service ran into an error:")
            print(str(e))
            print("=========")
        finally:
            print("Sleeping for next: " + str(config.tick_frequency) + "hh:mm:ss")
            time.sleep(config.tick_frequency.seconds)

def debug_tick():
    while True:
        print("\n" + config.core_service_name + " service running: " + str(datetime.datetime.now()))
        main.tick()
        time.sleep(config.tick_frequency.seconds)

config.init()

print(config.core_service_name + " has booted: " + str(datetime.datetime.now()) +
      "\nVersion: " + str(config.version))

if config.debug_mode:
    print("Running service in DEBUG_MODE")
    debug_tick()
else:  
    tick()
