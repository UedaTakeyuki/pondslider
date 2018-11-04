# coding:utf-8 Copy Right Takeyuki UEDA © 2015 -
#
import sys
#import inspect
import traceback
#import subprocess
#import datetime
import importlib
#import logging
#import ConfigParser
import pytoml as toml

# Const
#reboot = 'sudo reboot'

def error_report():
  info=sys.exc_info()
  print (traceback.format_exc(info[0]))

def read(configfilepath):
  ############################################################
  # sensors
  #
  with open(configfilepath, 'rb') as fin:
    config = toml.load(fin)

  for sensor in config["sensors"]:
    # road sensor_handler.
    sensor_handler = importlib.import_module(sensor["handler"])
    try:
      red_values = sensor_handler.read()
      print(red_values)
    except:
      error_report()
      continue

    if "values" is not None:
      values = sensor["values"]
      for value in values:
        print(value["name"])
        for handler in value["handlers"]:
          print(handler)

          try:
            value_handler = importlib.import_module(handler)
            value_handler.handle(sensor_handler, value["name"], red_values[value["name"]])
          except:
            error_report()