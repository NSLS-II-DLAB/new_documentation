import re
import asyncio
import os
from datetime import datetime
from types import SimpleNamespace
import bluesky.plan_stubs as bps
from bluesky.utils import make_decorator
from megatron.megatron_control import process_megatron_command
from megatron.motor_control import process_motor_command
from megatron.exceptions import CommandNotFoundError, LoopSyntaxError

def ts_periodic_logging_wrapper(plan, signals, log_file_path, period=1):
    stop = asyncio.Event()

    async def logging_coro():
        while not stop.is_set():
            is_new_file = False
            if not os.path.isfile(log_file_path):
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
                is_new_file = True

            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

            with open(log_file_path, "at") as f:
                if is_new_file:
                    signal_names = ",".join([f"\"{_}\"" for _ in signals.keys()])
                    f.write(f"Timestamp,{signal_names}\n")

                signal_values = []
                for signal in signals.values():
                    if signal.connected:
                        try:
                            reading = await signal.read()
                            signal_value = reading['value']
                        except Exception as e:
                            signal_value = f"Error: {str(e)}"
                    else:
                        signal_value = "Disconnected"  
                    signal_values.append(str(signal_value))

                f.write(f"{timestamp},{','.join(signal_values)}\n")

            await asyncio.sleep(period)

    class StartStopLogging:
        def __enter__(self):
            print("Starting periodic logging")
            asyncio.ensure_future(logging_coro())

        def __exit__(self, *args):
            print("Stopping periodic logging")
            stop.set()

    def _inner():
        with StartStopLogging():
            yield from plan

    return (yield from _inner())

ts_periodic_logging_decorator = make_decorator(ts_periodic_logging_wrapper)

_device_mapping = {
    "Galil RBV": "galil_rbv",
    "Galil VAL": "galil_val"
}

_required_devices = ("galil", "galil_val", "galil_rbv")

def create_shared_context(devices):
    for device in _required_devices:
        if device not in devices:
            raise RuntimeError(f"Device {device} is missing in the devices list")

    return SimpleNamespace(
        devices=SimpleNamespace(**devices),
        galil_abs_rel=0,  # 0 - absolute, 1 - relative
        galil_pos=0,
        galil_speed=1000000,
        device_mapping=_device_mapping,  
        required_devices=_required_devices,
        logged_signals={} 
    )

class MegatronInterpreter:
    def __init__(self, *, shared_context):
        self.context = shared_context
        self.megatron_commands = [
            "email", "exit", "failif", "failifoff", "l", "log", "lograte", "plot",
            "print", "run", "setao", "setdo", "stop", "t", "var", "waitai", "waitdi"
        ]
        self.motor_commands = [
            "ac", "af", "ba", "bg", "bi", "bl", "bm", "bt", "bz", "cc", "ce", "cn", 
            "dc", "dp", "er", "fa", "fe", "fl", "fv", "hv", "ib", "iht", "il", "kd", 
            "ki", "kp", "ld", "mo", "mt", "op", "pa", "pr", "pv", "sc", "sh", "sp", 
            "st", "ta", "tp", "xq"
        ]

    def execute_script(self, script_path):
        with open(script_path, "r") as script_file:
            script_lines = script_file.readlines()

        def plan():
            i = 0
            while i < len(script_lines):
                line = script_lines[i].strip()
                
                # Ignore comments
                if line.startswith('#'):
                    i += 1
                    continue
                
                if not line:
                    yield from bps.null()
                    i += 1
                    continue

                # Handle timers (t) and loops (L)
                match_t = re.match(r"t([\d.]+)", line, re.IGNORECASE)
                match_l = re.match(r"l(\d+)", line, re.IGNORECASE)

                try:
                    if match_t:
                        timer_value = match_t.group(1)
                        yield from self.handle_timer(timer_value)

                    elif match_l:
                        loop_count = int(match_l.group(1))
                        loop_end = self.find_end_of_loop(script_lines, i)

                        if loop_end == -1:
                            raise LoopSyntaxError()
                        yield from self.handle_loop(loop_count, script_lines[i + 1:loop_end])
                        i = loop_end
                    else:
                        # Tokenize the command and arguments, handling quoted strings as a single argument
                        command, *args = self.tokenize_command(line)

                        # Determine the appropriate handler for the command
                        if command in self.megatron_commands:
                            yield from process_megatron_command(command, args, self.context)
                        elif command in self.motor_commands:
                            yield from process_motor_command(command, args, self.context)
                        else:
                            raise CommandNotFoundError(command)
                except (CommandNotFoundError, LoopSyntaxError) as e:
                    print(e)
                    yield from bps.null()
                i += 1

        yield from plan()

    def tokenize_command(self, line):
        # Regex to split by spaces or commas, while keeping quoted substrings intact
        regex = r'(?:(?:"([^"]+)")|([^\s,]+))'
        tokens = re.findall(regex, line)
        
        # Flatten the token list, ensuring we remove quotes and keep all values
        return [t[0] or t[1] for t in tokens if t[0] or t[1]]

    def handle_timer(self, timer_value):
        print(f"Processing timer for {timer_value} seconds")
        yield from process_megatron_command("t", [timer_value], self.context)

    def handle_loop(self, loop_count, block):
        for _ in range(loop_count):
            print(f"Executing loop iteration {_ + 1} of {loop_count}")
            yield from self.execute_block(block)

    def find_end_of_loop(self, lines, start_index):
        loop_depth = 0
        for i in range(start_index + 1, len(lines)):
            line = lines[i].strip().lower()
            if line.startswith("l"):
                loop_depth += 1
            elif line == "n":
                if loop_depth == 0:
                    return i
                else:
                    loop_depth -= 1
        return -1

    def execute_block(self, block):
        for line in block:
            line = line.strip()
            if not line:
                yield from bps.null()
                continue

            match_t = re.match(r"t([\d.]+)", line, re.IGNORECASE)
            if match_t:
                timer_value = match_t.group(1)
                yield from self.handle_timer(timer_value)
                continue

            command, *args = self.tokenize_command(line)

            if command in self.megatron_commands:
                yield from process_megatron_command(command, args, self.context)
            elif command in self.motor_commands:
                yield from process_motor_command(command, args, self.context)
