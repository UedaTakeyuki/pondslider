# pondslider
Multipurpose sensorhandler, read the value from source & do somethings (send, save, trigger, ...) with it, as configed.

## install

```bash:
pip install pondslider
```

## input
config.toml. The contents are expected as follows:

```
[[sources]]
  handler   = "dht22"
  [[sources.values]]
    name = "temp"
    handlers = [
      "send",
      "save"
    ]
  [[sources.values]]
    name = "humidity"
    handlers = [
      "send",
      "save"
    ]
  [[sources.values]]
    name = "humiditydeficit"
    handlers = [
      "send",
      "save"
    ]


[[sources]]
  handler   = "mh-z19"
  [[sources.values]]
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

  - handlers: The array of Python module of Value handler's. The pondslider import these modules dynamically and call function ***handle(source_modlue, name, value)*** for each acquired value. You can 

## How to use 
### as python program.

```bash:
python -m sensorhandler [--config config_file_path] [--imppath python_module_import_path] [ --list_imppath list_of_python_module_import_path]
```
In case no --config, "config.toml" on the running path is used.
The path specified by --imppath and --list_imppath is used ad additional Python import library path.

### as python library.

```python:
import sensorhandler

print (sensorhandler.read(config_file_path))
```
## Q&A
Any questions, suggestions, reports are welcome! Please make [issue](https://github.com/UedaTakeyuki/sensorhandler/issues) without hesitation! 

## history
- 0.1.1  2018.09.28  first version confirmed Raspberry Pi model B2+
- 0.1.2  2018.09.29  add config_file_path
- 0.1.3  2018.09.29  add --config, --imppath, --list_imppath
