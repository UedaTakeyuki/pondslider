import os
import sys
import argparse
import time
import datetime
import __init__ as pondslider

parser = argparse.ArgumentParser()
parser.add_argument("--config",
                    default=os.getcwd()+'/config.toml',
                    help="config file for handler specification.")
#parser.add_argument("--imppath",
#                    help="full path for python modules import path.")
parser.add_argument("--imppaths",
										type=str, nargs='+',
                    help='list of full path for python modules import path like as "/home/pi/mh-z19 /tmp/handler" .')
parser.add_argument("--interval",
                    type=int,
                    help='minute of interval to repeat. no repeat in case not set." .')
parser.add_argument("--sensor_handlers",
                    type=str, nargs='+',
                    help='list of sensor handler modules as "sensor.mh-z19 dht22" .')
parser.add_argument("--value_handlers",
                    type=str, nargs='+',
                    help='list of value handler modules as "sender.monitor.send saver.strage.save" .')

args = parser.parse_args()

usage = 'Usage: python {} [config_file_path]'.format(__file__)

# config file
'''
if args.config:
	configfilepath = args.config
else:
  configfilepath = os.getcwd()+'/config.toml'
'''

# additional import path
'''
if args.imppath:
	sys.path.append(args.imppath)
'''
if args.imppaths:
  for imppath in args.imppaths:
    sys.path.append(imppath)

'''
if len(sys.argv) > 1:
  configfilepath = sys.argv[1]
else:
  configfilepath = os.getcwd()+'/config.toml'
'''

if args.interval:
  while True:
    now = datetime.datetime.now()
    pondslider.read(args.config)
    pondslider.read2(args.sensor_handlers, args.value_handlers)
    now_after=datetime.datetime.now()
    elapsed=(now_after - now).seconds +  float((now_after - now).microseconds)/1000000
    if (elapsed < args.interval * 60):
        time.sleep(args.interval * 60 - elapsed)
else:
  pondslider.read(args.config)
  pondslider.read2(args.sensor_handlers, args.value_handlers)
