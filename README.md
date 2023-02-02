# Generic Device Communications!

## Installation:
Clone this repo such that the filesystem looks like this:
├── Communications
│ ├── communications
│ ├── ├── \_\_init\_\_.py
│ ├── ├── client.py
│ ├── ├── parent.py
│ ├── ├── server.py
│ ├── ├── utils.py
├── Device
│ ├── main.py
│ ├── other device code

## Importation
in Device/main.py
```python
import ..Communications import communications
```

## Usage:
In device main, call

```python
communications = Process(target=...,
    args(system_ip="", system_port=#, connection_ip="", connection_port=#, function_set={}))

communications.start()

#DO NON-COMS THINGS

communications.join() # Will block on this call until communications is done. Call last

```

Where system_ip is the ip of the system and system_port is the desired connection port to use on system and
connection_ip is the ip you wish to connect to and connection port is the port to use for connection

### example:
* drone with ip 192.168.1.1, port=7777
* rover with ip 192.168.1.2, port 8888
In drone main.py:
```python
communications = Process(target=...,
    args(system_ip="192.168.1.1", system_port=7777, connection_ip="192.168.1.2", connection_port=8888, function_set={}))
communications.start()
```
In rover main.py:
```python
communications = Process(target=...,
    args(system_ip="192.168.1.2", system_port=8888, connection_ip="192.168.1.1", connection_port=7777, function_set={}))
communications.start()
```

## Function_set
### Function set rules:
* All functions MUST have an args parameter, even if the function doesn't use it!
* All arguments to functions MUST be in the form of a list[str]. The function itself must parse the arguments!
```python
function_set = {
    "GPS": lambda args : print("This is the GPS function"),
    "MOVE": lambda args : print(f"This is the MOVE function: x:{int(args[0])}, y:{int(args[1])}"),
}
```

## Sending Data
To send data (assuming import from above):
```python3
def example(args : list[str]):
    print(args[0])

function_set = {
    "GPS": example,
}

communications.send_packet(flag="GPS", args=[1,2])
```
