# Generic Device Communications!

## Installation:
Clone this repo such that the filesystem looks like this:

```bash
├── Communications
│ ├── setup.py
│ ├── communications
│ ├── ├── \_\_init\_\_.py
│ ├── ├── client.py
│ ├── ├── parent.py
│ ├── ├── server.py
│ ├── ├── utils.py
├── Device
│ ├── main.py
│ ├── other device code
```

## Importation
in Device/main.py
```python
from multiprocessing import Process
from ..Communications import communications
```

## Usage:
In device main, call

```python
communications = Process(target=...,
    args=(system_ip="", system_port=#, connection_ip="", connection_port=#, function_set={}))

communications.start()

#DO NON-COMS THINGS

communications.join() # Will block on this call until communications is done. Call last

```

Where system_ip is the ip of the system and system_port is the desired connection port to use on system and
connection_ip is the ip you wish to connect to and connection port is the port to use for connection

### Example:
* drone with ip 192.168.1.1, port=7777
* rover with ip 192.168.1.2, port 8888

In drone main.py:
```python
communications = Process(target=parent_proc,
    args=("192.168.1.1", 7777, "192.168.1.2", 8888, {}))
communications.start()
```
In rover main.py:
```python
communications = Process(target=parent_proc,
    args=("192.168.1.2", 8888, "192.168.1.1", 7777, {}))
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

## Sending Data to Execute Commands
To send data (assuming import from above):

In Rover:
```python3
def example(args : list[str]):
    print(args[0])

function_set = {
    "GPS": example,
}
```

In Drone:
```python3
communications.send_packet(flag="GPS", args=["1","2"])
```

Assuming the function_set input correctly, this causes the receiving device (Drone)
to execute it's "GPS" function.
