[![Downloads](https://pepy.tech/badge/pondslider)](https://pepy.tech/project/pondslider)
[![Downloads](https://pepy.tech/badge/pondslider/month)](https://pepy.tech/project/pondslider)
[![Downloads](https://pepy.tech/badge/pondslider/week)](https://pepy.tech/project/pondslider)
# pondslider

Multipurpose sensor handler, read sensor & do somethings (send, save, trigger, ...) with the value.


## What is pondslider
The pondslider is a python module to read sensor values by Sensor handler, and do somethins with the value by Value handler.

<img src="https://raw.githubusercontent.com/UedaTakeyuki/pondslider/master/pics/ss.2018-11-03.13.56.11.png">

### What is pondslider for?
The pondslider is for making IoT device side project quickly by ***reusing existing codes***.

- Reusing existing ***Sensor reading*** code through ***unified interface*** provided by ***Sensor handler*** mention later.
- Reusing existing ***Value handling*** code through ***unified interface*** provided by ***Value handler*** mention later.


### How the pondslider work?
First, the pondslider read a configration file to specify:

- Which sensors shoul be read.
- Which values are returned by specific sensor.
- What shoud it do for each value.

Then, pondslider get sensor values through specific ***sensor handlers***, and call ***value handlers*** which is related.

### What is Sensor handler?
The Sensor handler is a python module which wrap existing sensor reading code having various interface, to provide unified interface as follows:

- unified read() function:
  Sensor handler unifies various function call of sensor value reading on the existing codes as ***read()***

- well-formed return value:
  The ***read()*** function return a python dictionally of ***name*** and ***value*** pairs as follow:

``` {'humiditydeficit': 15.9, 'temp': 26.8, 'humidity': 37.6}```

<img src="https://raw.githubusercontent.com/UedaTakeyuki/pondslider/master/pics/ss.2018-11-07.15.21.07.png">

Typically, a sensor handler is created as a wrapper module of exising python module with ***import*** and call there function to read sensor value as follow:

```python:
# import existing module
import SomethingExistingSensorModule

#####################################
#
# unified read() interface
#

def read():
  
  # prepare existing module
  a_sensor = SomethingExistingSensorModule.new()

  # call there function to read sensor value 
  values   = a_sensor.there_func_to_read_sensor()

  # re-format to name-value pair.
  return adjust_the_format(values)

def adjust_the_format(value)
  ''' adjst the format of value as a dictionaly of name & value pair. '''

```

In other case, with external executable file,

```python:
# import python standard external executable handle module
import subprocess

def read():

  # call external executable and get return strings
  p = subprocess.Popen("./SomethingExistingExecutable2GetSensorValue",
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, 
                       shell=True)
  std_out, std_err = p.communicate(None, timeout=20)
  value = std_out.strip()

  # re-format to name-value pair.
  return adjust_the_format(value)

def adjust_the_format(value)
  ''' adjst the format of value as a dictionaly of name & value pair. '''

```

Of cource, It's OK to make Sensor handler as reading sensor value directory.

```python:
import serial

def read():
  # mh-z19 CO2 sensor https://github.com/UedaTakeyuki/mh-z19
  try:
    ser = serial.Serial(serial_dev,
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0)
    while 1:
      result=ser.write("\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s=ser.read(9)
      if len(s) >= 4 and s[0] == "\xff" and s[1] == "\x86":
        return {'co2': ord(s[2])*256 + ord(s[3])}
      break
  except:
     traceback.print_exc()

```

### What is Value handler?
The Value handler is a python module which recieve sensor value, and do something with it, for example, send to server, write to strage, and so on.
The purpose of valule handler is to provide a unified interface to handle acquired sensor value with following interface:

```python:
def handle(sensor_hander, data_name, value):
```
<img src="https://github.com/UedaTakeyuki/pondslider/blob/master/pics/ss.2018-11-08.10.57.59.png?raw=true">

## example handlers
example of handlers are available at https://github.com/UedaTakeyuki/handlers


## install

```bash:
pip install pondslider
```

## How to set Sensor and Value handlers

There are 2 way to set handers. One is to use command-line option, the other is [TOML](https://github.com/toml-lang/toml) formatted config file.
In case both config and command-line option is set, the pondslider handle also both in the order config file first, then command-line.

### Set Sensor and Value handlers by command-line option
The Sensor handlers can be set by command-line option ***--sensor_handlers***.
This is list type command-line option, you can specify nesessary sensor handlers module like mh-z19 and dht22 as follows:

```
--sensor_handlers mh_z19 dht22
```

For the value handlers also has similar command-line option ***--value_handlers***.
For example, spesify modules of ***sender.monitor.send*** and ***saver.strage.save*** as follows:

```
--value_handlers sender.monitor.send saver.strage.save
```

Each value handlers ***handle()*** functions is called with ***All*** value red from  ***All*** Sensor handlers. In case you need to call corresponding value handler with ***ONLY*** corresponding value, you shoud check value name and value handler module which passed as function parameter of handle(), like as follow.

```python:
def handle(data_source_name, data_name, value):
    if data_name is "co2":
        # do something
    else:
        # do nothing
        pass
``` 

Or, use config file mention later, which can relate value and value handler one to one.


### Set Sensor and Value handlers by [TOML](https://github.com/toml-lang/toml) formatted config file.

You can specify one to one relation with which sensor handler's which value and corresponding value handler, by config file. 
The contents are expected as follows:

```
[[sensors]]
  handler   = "dht22"
  [[sensors.values]]
    name = "temp"
    handlers = [
      "send",
      "save"
    ]
  [[sensors.values]]
    name = "humidity"
    handlers = [
      "send",
      "save"
    ]
  [[sensors.values]]
    name = "humiditydeficit"
    handlers = [
      "send",
      "save"
    ]


[[sensors]]
  handler   = "mh-z19"
  [[sensors.values]]
    name = "co2"
    handlers = [
      "send",
      "save"
  ]
```

The config file of pondslider consist of an array of table ***[[sensors]]***.
The pondslider read this array, then read each sensor handler and call corresponding value handler.

The element of ***sensors*** have a couple of keys, the one is ***handler*** which indicate corresponding Sensor handler, the other is ***[[sensors.values]]*** which indicate corresponding Value handlers.

***[[sensors.values]]*** have also a couple of kyes, the one is ***name*** which indicate correcponding red sensor value name, which is the key of the dictionally of Sensor handlers ***read()*** function's return. The others are ***handlers*** array which indicate value handler module. The ***handle()*** funcitons of these handler are called ***Only*** with the red sensor value which has same ***name***, unlike the valuehandlers specified by command-line option ***value_handlers*** is called with ***All*** value red from  ***All*** Sensor handlers.

The config file is specified by command-line option ***--config***. With out --config option, the pondslider search the file named ***config.toml*** on the current working directory and use it if found.

### Add python module search path
In case your handler module is not linked by standard python module search path, you can tell the pondslider to add search path by command-line option ***--imppaths*** as follows:

```bash:
  --imppaths IMPPATHS [IMPPATHS ...]
                        list of full path for python modules import path like
                        as "/home/pi/mh-z19 /tmp/handler" .
``` 

For example, in case your mh-z19 sensor handler is in /home/pi/mh-z19 and your send handler is in /home/pi/handlers/send.py, you can read mh-z19 and send the value as follows:

```
sudo python -m pondslider --sensor_handlers mh_z19 --value_handlers sender.monitor.send --imppaths /home/pi/mh-z19 /home/pi/handlers
```

Note, mh-z19 need to read serial interface and it might be necessary of sudo.

## How to use 
### as python program.

```bash:
usage: python -m pondslider [-h] [--config CONFIG] [--imppaths IMPPATHS [IMPPATHS ...]]
                  [--interval INTERVAL]
                  [--sensor_handlers SENSOR_HANDLERS [SENSOR_HANDLERS ...]]
                  [--value_handlers VALUE_HANDLERS [VALUE_HANDLERS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       config file for handler specification.
  --imppaths IMPPATHS [IMPPATHS ...]
                        list of full path for python modules import path like
                        as "/home/pi/mh-z19 /tmp/handler" .
  --interval INTERVAL   minute of interval to repeat. no repeat in case not
                        set." .
  --sensor_handlers SENSOR_HANDLERS [SENSOR_HANDLERS ...]
                        list of sensor handler modules as "sensor.mh-z19
                        dht22" .
  --value_handlers VALUE_HANDLERS [VALUE_HANDLERS ...]
                        list of value handler modules as "sender.monitor.send
                        saver.strage.save" .
p
```
The path specified by --imppaths is used ad additional Python import library path.
With --interval option, pondslider repeat it in specified interval minutes. Without --interval, just run one time and quit.


### as python library.

```python:
import pondslider

print (pondslider.read(config_file_path))
```
## Q&A
Any questions, suggestions, reports are welcome! Please make [issue](https://github.com/UedaTakeyuki/pondslider/issues) without hesitation! 

## history
- 0.1.1  2018.11.03  first version self-forked from [sensorhandler](https://github.com/UedaTakeyuki/sensorhandler).
- 0.2.1  2018.11.06  add --interval option.
- 0.2.2  2018.11.06  minor fix: remove redundant print
- 0.3.1  2018.11.07  add --sensor_handlers and --value_handlers
