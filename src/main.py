# Set environment variables, e.g add the following to .bashrc
#   export EPICS_CA_AUTO_ADDR_LIST=NO
#   export EPICS_CA_ADDR_LIST="172.17.255.255 127.0.0.1"
#
# Start simulated motor IOC before running the code (requires sudo).
# Refer to docker documentation on how to maintain downloaded images.
#   docker pull dchabot/simioc
#   sudo docker run --network="host" -d dchabot/simioc
#   sudo docker exec -it <ID> bash
# Iniside the container shell
#   telnet localhost 2048

import os
from megatron.interpreter import MegatronInterpreter
from bluesky import RunEngine
from megatron.exceptions import InvalidScriptPathError

def main():
    RE = RunEngine({})
    interpreter = MegatronInterpreter()

    script_path = "scripts/demo.txt"
    
    if not os.path.exists(script_path) or not os.path.isfile(script_path):
        raise InvalidScriptPathError(script_path)  

    try:
        plan = interpreter.execute_script(script_path)
        RE(plan)
    except InvalidScriptPathError as e:
        print(e) 
    except Exception as e:
        print(f"Execution failed with error: {e}")  

if __name__ == "__main__":
    main()
