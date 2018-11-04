import os
import sys
import argparse
import __init__ as pondslider

parser = argparse.ArgumentParser()
parser.add_argument("--config",
                    default=os.getcwd()+'/config.toml',
                    help="config file for handler specification.")
#parser.add_argument("--imppath",
#                    help="full path for python modules import path.")
parser.add_argument("--imppaths",
										type=str, nargs='+',
                    help='list of full path for python modules import path like as "/home/pi/mh-z19" "/tmp/handler" .')
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
print(args.imppaths)
if args.imppaths:
  for imppath in args.imppaths:
    print(imppath)
    sys.path.append(imppath)

'''
if len(sys.argv) > 1:
  configfilepath = sys.argv[1]
else:
  configfilepath = os.getcwd()+'/config.toml'
'''

pondslider.read(args.config)