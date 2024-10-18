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
import argparse
from datetime import datetime
from bluesky.utils import ProgressBarManager
from bluesky.run_engine import RunEngine
import bluesky.preprocessors as bp
from ophyd import EpicsSignal, EpicsSignalRO
from megatron.context import create_shared_context
from megatron.interpreter import MegatronInterpreter
from megatron.logger import ts_periodic_logging_decorator
from megatron.support import register_custom_instructions, EpicsMotorGalil

parser = argparse.ArgumentParser(description="Run a Megatron script.")
parser.add_argument(
    "-p", "--path", type=str, help="The path to the Megatron script to execute."
)
args = parser.parse_args()

#prefix = "Test{DMC:1}A"
prefix = "sim:mtr1"

galil = EpicsMotorGalil(f"{prefix}", name='galil')
galil_val = EpicsSignal(f'{prefix}.VAL', name='galil_val', auto_monitor=True)
galil_rbv = EpicsSignalRO(f'{prefix}.RBV', name='galil_rbv', auto_monitor=True)

galil.wait_for_connection()
galil_val.wait_for_connection()
galil_rbv.wait_for_connection()

devices = {"galil": galil, "galil_val": galil_val, "galil_rbv": galil_rbv}

RE = RunEngine({})
RE.waiting_hook = ProgressBarManager()

register_custom_instructions(re=RE)

context = create_shared_context(devices)
interpreter = MegatronInterpreter(shared_context=context)

script_path = args.path if args.path else "scripts/script2.txt"
logging_dir = "./logs"
log_file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
log_file_path = os.path.join(logging_dir, log_file_name)

@bp.reset_positions_decorator([galil.velocity])
@ts_periodic_logging_decorator(signals=context.logged_signals, log_file_path=log_file_path, period=1)
def run_with_logging(script_path):
    yield from interpreter.execute_script(script_path)

RE(run_with_logging(script_path))
