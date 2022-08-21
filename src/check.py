import datetime
import os
import argparse
from _cron import *
from _file import *

from suntime import Sun, SunTimeException

parser = argparse.ArgumentParser(description="Job arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--latitude", default=float(os.getenv('LAT', 0.0)), help="latitute")
parser.add_argument("-b", "--longitude", default=float(os.getenv('LNG', 0.0)), help="longitude")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()
config = vars(args)


sun = Sun(config["latitude"], config["longitude"])

now = datetime.datetime.now()


# Get today's sunrise and sunset in UTC
try:
    if config["verbose"] is True:
        print("latitude: {}".format(config["latitude"]))
        print("longitude: {}".format(config["longitude"]))

    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()

    if config["verbose"] is True:
        print("sunrise: {}".format(today_sr))
        print("sunset: {}".format(today_ss))

    if now > today_sr:
      if is_closed():
        if config["verbose"] is True:
          print("open")
          write_state("open")
          # open door
          create_cron("e-chicken-door-job", "/usr/local/bin/python /usr/src/app/door.py --duration {duration} --pin {pin}".format(duration = 5, pin = 22), start=now)
      else:
        if config["verbose"] is True:
          print("door already open")

    if now > today_ss:
      if is_open():
        if config["verbose"] is True:
          print("close")
          write_state("closed")
          # close door
          create_cron("e-chicken-door-job", "/usr/local/bin/python /usr/src/app/door.py --duration {duration} --pin {pin}".format(duration = 5, pin = 4), start=now)
      else:
        if config["verbose"] is True:
          print("door already closed")


except SunTimeException as e:
    print("Error: {0}.".format(e))
