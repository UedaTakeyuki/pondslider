# coding:utf-8 Copy Right Takeyuki UEDA © 2015 -
#
import os
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
  if os.path.exists(configfilepath):
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
          if value["name"] in red_values.keys():
            for handler in value["handlers"]:
              try:
                value_handler = importlib.import_module(handler)
                value_handler.handle(sensor_handler, value["name"], red_values[value["name"]])
              except:
                error_report()
                continue

def read2(sensor_handlers, value_handlers):
  if not sensor_handlers is None:
    for s in sensor_handlers:
      # road sensor_handler.
      sensor_handler = importlib.import_module(s)
      try:
        red_values = sensor_handler.read()
        print(red_values)
      except:
        error_report()
        continue

      for name, value in red_values.items():
        if not value_handlers is None:
          for v in value_handlers:
            try:
              value_handler = importlib.import_module(v)
              value_handler.handle(sensor_handler, name, value)
            except:
              error_report()
              continue
