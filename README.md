# pondslider
General sensor handler, read sensor & do somethings (send, save, trigger, ...) with the value.


## What is pondslider
The pondslider is a python module to read sensor values by Sensor handler, and do somethins with the value by Value handler.

<img src="https://raw.githubusercontent.com/UedaTakeyuki/pondslider/master/pics/ss.2018-11-03.13.56.11.png">

### What is pondslider for?
The pondslider is for making IoT device side project quickly by ***reusing existing codes***.

- Reusing ***Sensor reading*** code.
- Reusing ***Value handling*** code.


### How the pondslider work?
First, the pondslider read a configration file to specify:

- Which sensors shoul be read.
- Which values are returned by specific sensor.
- What shoud it do for each value.

Then, pondslider read sensor values through specific ***sensor handlers***, and call ***value handlers*** which is specified for the value.

### What is Sensor handler?
The Sensor handler is a python module which wrap existing sensor value reading code to provide unified interface as follows:

- unified read() function
Sensor handler unifies various function call of sensor value reading on the existing codes as ***read()***

- well-formed return value:
The ***read()*** function return a python dictionally of ***name*** and ***value*** pairs as follow:

``` {'humiditydeficit': 15.9, 'temp': 26.8, 'humidity': 37.6}```


Typically, a sensor handler is created as a wrapper module of exising python module of sensor reading as:

```python:
import SomethingExistingSensorModule

def read():
  a_sensor = SomethingExistingSensorModule.new()
  values   = a_sensor.read()
  return adjust_the_format(values)

def adjust_the_format(value)
  ''' adjst the format of value as a dictionaly of name & value pair. '''

```

In other case, with external executable file,

```python:
import subprocess

def read():
  p = subprocess.Popen("./SomethingExistingExecutable2GetSensorValue",
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, 
                       shell=True)
  std_out, std_err = p.communicate(None, timeout=20)
  value = std_out.strip()

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

## example handlers
example of handlers are available at https://githubcom/UedaTakeyuki/handlers


## install

```bash:
pip install pondslider
```

## input
config.toml. The contents are expected as follows:

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

Each element of the array of table ***sources*** correspond to one actual data source like a Sensor Device and so on. Tha table is consist of ***handler *** and ***value***.

- handler: Python module of Sensor handler. The pondslider import this module dynamically and call function ***read()*** to get value. The returned value is expecte as a dictionally as key of ***value name*** and correcponding value like:

``` {'humiditydeficit': 15.9, 'temp': 26.8, 'humidity': 37.6}```

- values: The array of table corresponding to the python dictionally of values which is the returned value of read() mentioned above. The table is consist of ***name*** and ***handlers***. 
  - name: The key of dictionally of values like "humiditydeficit", "temp", "humidity" on the above example.

  - handlers: The array of Python module of Value handler's. The pondslider import these modules dynamically and call function ***handle(source_modlue, name, value)*** for each acquired value.

## How to use 
### as python program.

```bash:
usage: python -m sensorhandler [-h] [--config CONFIG] [--imppaths IMPPATHS [IMPPATHS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       config file for handler specification.
  --imppaths IMPPATHS [IMPPATHS ...]
                        list of full path for python modules import path like
                        as "/home/pi/mh-z19" "/tmp/handler"
```
The path specified by --imppaths is used ad additional Python import library path.

### as python library.

```python:
import sensorhandler

print (sensorhandler.read(config_file_path))
```
## Q&A
Any questions, suggestions, reports are welcome! Please make [issue](https://github.com/UedaTakeyuki/sensorhandler/issues) without hesitation! 

## history
- 0.1.1  2018.11.03  first version self-forked from [sensorhandler](https://github.com/UedaTakeyuki/sensorhandler)
