USAGE = "Usage: python3 main.py [system ip] [connection ip] [port]"
BUFFER_SIZE = 1024

RETURN_SUCCESS = 0x0
RETURN_ERROR = 0x1

def checkFunctionValidity(function_set) -> bool:
    # Check to see that the function set has at least 1 key
    return len(function_set.keys()) >= 1
