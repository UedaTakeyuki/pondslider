import os
import sys
import argparse
import __init__ as sensorhandler

parser = argparse.ArgumentParser()
parser.add_argument("--config",
                    help="config file path for handler specification.")
parser.add_argument("--imppath",
                    help="full path for python modules import path.")
parser.add_argument("--list_imppath",
										type=list,
                    help='list "a b c" of full path for python modules import path.')
args = parser.parse_args()

usage = 'Usage: python {} [config_file_path]'.format(__file__)

# config file
if args.config:
	configfilepath = args.config
else:
  configfilepath = os.getcwd()+'/config.toml'

# additional import path
if args.imppath:
	sys.path.append(args.imppath)

if args.list_imppath:
	for path in list_imppath:
		sys.path.append(args.imppath)

'''
if len(sys.argv) > 1:
  configfilepath = sys.argv[1]
else:
  configfilepath = os.getcwd()+'/config.toml'
'''

sensorhandler.read(configfilepath)