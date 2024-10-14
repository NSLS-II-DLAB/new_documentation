import os
import bluesky.plan_stubs as bps
from megatron.exceptions import CommandNotFoundError
from megatron.support import wait_for_condition
import inspect

def process_megatron_command(command, args, context, current_script_path=None):
    command_dispatcher = {
        "email": email,
        "exit": exit_command,
        "failif": failif,
        "failifoff": failifoff,
        "l": l_command,
        "log": log,
        "lograte": lograte,
        "print": print_command,
        "run": run,
        "setao": setao,
        "setdo": setdo,
        "stop": stop,
        "t": t_command,
        "var": var,
        "waitai": waitai,
        "waitdi": waitdi
    }

    if command in command_dispatcher:
        command_function = command_dispatcher[command]

        sig = inspect.signature(command_function)
        params = list(sig.parameters)

        kwargs = {"args": args, "context": context, "current_script_path": current_script_path}
        dynamic_args = [kwargs[param] for param in params if param in kwargs]

        yield from command_function(*dynamic_args)
    else:
        raise CommandNotFoundError(command)

def l_command(args, block, context):
    for line in block:
        yield from process_megatron_command(line[0], line[1:], context)

def t_command(args):
    timer_duration = float(args[0])
    print(f"Executing timer for {timer_duration} seconds")
    yield from bps.sleep(timer_duration)

def exit_command():
    print("Exiting the interpreter.")
    raise SystemExit

def lograte(args):
    print(f"Setting lograte to {args[0]}")
    yield from bps.null()

def email(args):
    subject = args[0]
    message = args[1]
    recipients = args[2:]
    print(f"Sending email with subject '{subject}' to {recipients}")
    yield from bps.null()

def failif(args):
    pv, value, fail_script = args
    print(f"Failing if {pv} changes to {value}, running script: {fail_script}")
    yield from bps.null()

def failifoff(args):
    pv = args[0]
    print(f"Disabling failif for {pv}")
    yield from bps.null()

def log(args, context):
    signal_name = args[0]
    if signal_name in context.device_mapping:
        signal_device_name = context.device_mapping[signal_name]
        signal = getattr(context.devices, signal_device_name)
        context.logged_signals[signal_name] = signal 
        print(f"Added {signal_name} to logging signals.")
    else:
        raise RuntimeError(f"Signal {signal_name} not found in device mapping.")
    yield from bps.null()


def print_command(args):
    text = ' '.join(args)
    print(f"Executing 'print' command with text: {text}")
    yield from bps.null()

def run(args, context, current_script_path):
    script_name = args[0]

    base_path = os.path.dirname(current_script_path)
    script_path = os.path.join(base_path, *script_name.split('\\'))

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script {script_path} not found.")

    print(f"Running script: {script_name} ({script_path})")

    yield from context.run_script_callback(script_path)

def setao(args):
    sp = args[0]
    value = float(args[1])
    print(f"Setting analog output {sp} to {value}")
    yield from bps.null()

def setdo(args):
    pv = args[0]
    value = int(args[1])
    print(f"Setting digital output {pv} to {value}")
    yield from bps.null()

def stop(args):
    script_name = args[0]
    print(f"Stopping script: {script_name}")
    yield from bps.null()

def var(args):
    variable = args[0]
    expression = args[1]
    print(f"Setting variable {variable} to {expression}")
    yield from bps.null()

def waitai(args, context):
    source = args[0]
    operator = args[1]
    value = float(args[2])
    tolerance = float(args[3]) if len(args) > 3 else 0
    timeout = float(args[4]) if len(args) > 4 else None

    if source in context.device_mapping:
        device_name = context.device_mapping[source]
        signal = getattr(context.devices, device_name)
    else:
        raise RuntimeError(f"Unrecognized device name: {source!r}")

    yield from wait_for_condition(
        signal=signal, target=value / 1000000, operator=operator, tolerance=tolerance, timeout=timeout
    )

def waitdi(args, context):
    source = args[0]
    value = int(args[1])
    timeout = float(args[2]) if len(args) > 2 else None

    if source in context.device_mapping:
        device_name = context.device_mapping[source]
        signal = getattr(context.devices, device_name)
    else:
        raise RuntimeError(f"Unrecognized device name: {source!r}")

    yield from wait_for_condition(
        signal=signal, target=value / 1000000, operator="==", tolerance=0, timeout=timeout
    )
