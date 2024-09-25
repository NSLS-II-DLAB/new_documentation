import re
from megatron.megatron_control import process_megatron_command
from megatron.motor_control import process_motor_command
import bluesky.plan_stubs as bps
from megatron.exceptions import CommandNotFoundError, LoopSyntaxError

class MegatronInterpreter:
    def __init__(self):
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

        i = 0
        while i < len(script_lines):
            line = script_lines[i].strip()

            if not line:
                yield from bps.null()
                i += 1
                continue

            match_t = re.match(r"t([\d.]+)", line, re.IGNORECASE)
            match_l = re.match(r"l(\d+)", line, re.IGNORECASE)

            try:
                if match_t:
                    command = "t"
                    timer_value = match_t.group(1)
                    yield from self.handle_timer(timer_value)

                elif match_l:
                    command = "l"
                    loop_count = int(match_l.group(1))
                    loop_end = self.find_end_of_loop(script_lines, i)

                    if loop_end == -1:
                        raise LoopSyntaxError()
                    yield from self.handle_loop(loop_count, script_lines[i + 1:loop_end])
                    i = loop_end
                else:
                    tokens = line.split(" ", 1)
                    command = tokens[0].lower()
                    args = tokens[1:] if len(tokens) > 1 else []

                    if command in self.megatron_commands:
                        yield from process_megatron_command(command, args)
                    elif command in self.motor_commands:
                        yield from process_motor_command(command, args)
                    else:
                        raise CommandNotFoundError(command)
            except (CommandNotFoundError, LoopSyntaxError) as e:
                print(e)
                yield from bps.null()
            i += 1

    def handle_timer(self, timer_value):
        print(f"Processing timer for {timer_value} seconds")
        yield from process_megatron_command("t", [timer_value])

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

            tokens = line.split(" ", 1)
            command = tokens[0].lower()
            args = tokens[1:] if len(tokens) > 1 else []

            if command in self.megatron_commands:
                yield from process_megatron_command(command, args)
            elif command in self.motor_commands:
                yield from process_motor_command(command, args)
            else:
                raise CommandNotFoundError(command)  