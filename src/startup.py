# Set environment variables, e.g add the following to .bashrc
#   export EPICS_CA_AUTO_ADDR_LIST=NO
#   export EPICS_CA_ADDR_LIST="172.17.255.255 127.0.0.1"
#
# Start simulated motor IOC before running the code (requires sudo).
# Refer to docker documentation on how to maintain downloaded images.
#   docker pull dchabot/simioc
#   sudo docker run --network="host" -d dchabot/simioc
#   sudo docker exec -it <ID> bash
# Inside the container shell
#   telnet localhost 2048
#   caRepeater &
# Run the code
#   ipython
#   run -i "startup.py"

import os
from datetime import datetime
from bluesky.utils import ProgressBarManager
from bluesky import RunEngine
from ophyd import EpicsMotor, EpicsSignal, EpicsSignalRO
from megatron.interpreter import MegatronInterpreter, create_shared_context, ts_periodic_logging_decorator 
from megatron.exceptions import InvalidScriptPathError
from epics import ca

ca.use_initial_context()

galil = EpicsMotor('sim:mtr1', name='galil')
galil_val = EpicsSignal('sim:mtr1.VAL', name='galil_val', auto_monitor=True)
galil_rbv = EpicsSignalRO('sim:mtr1.RBV', name='galil_rbv', auto_monitor=True)

devices = {"galil": galil, "galil_val": galil_val, "galil_rbv": galil_rbv}

RE = RunEngine({})
RE.waiting_hook = ProgressBarManager()

context = create_shared_context(devices)
interpreter = MegatronInterpreter(shared_context=context)

script_path = "scripts/script.txt"
logging_dir = "./logs"
log_file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
log_file_path = os.path.join(logging_dir, log_file_name)

if not os.path.exists(script_path) or not os.path.isfile(script_path):
    raise InvalidScriptPathError(script_path)

try:
    @ts_periodic_logging_decorator(signals=context.logged_signals, log_file_path=log_file_path, period=1)
    def run_with_logging():
        yield from interpreter.execute_script(script_path)

    RE(run_with_logging())
except InvalidScriptPathError as e:
    print(e)
except Exception as e:
    print(f"Execution failed with error: {e}")
