# coding:utf-8 Copy Right Takeyuki UEDA © 2015 -
#
import sys
#import inspect
import traceback
import subprocess
import datetime
import importlib
#import logging
import ConfigParser
import pytoml as toml

# Const
reboot = 'sudo reboot'

def error_report():
  info=sys.exc_info()
  print (traceback.format_exc(info[0]))

def read(configfilepath):
  ############################################################
  # sensors
  #
  with open(configfilepath, 'rb') as fin:
    config = toml.load(fin)

  for data_source in config["sources"]:
#    print (data_source["name"])
#    print (data_source)

    # read errorhandler
    if "errorhandler" in data_source:
      errorhandler = data_source["errorhandler"]
#      print ("OK")
    else:
      errorhandler = None
#      print ("NG") 

    # road data_source.
    reader = importlib.import_module(data_source["name"])
    try:
      red_values = reader.read()
      print(red_values)
    except:
      error_report()
      continue

    if "values" is not None:
      values = data_source["values"]
      for value in values:
        print(value["name"])
        for handler_name in value["handlers"]:
          print(handler_name)

          try:
            handler = importlib.import_module(handler_name)
            handler.handle(data_source["name"], value["name"], red_values[value["name"]])
          except:
            error_report()