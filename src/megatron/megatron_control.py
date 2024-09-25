import bluesky.plan_stubs as bps
from megatron.exceptions import CommandNotFoundError

def process_megatron_command(command, args):
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
        yield from command_dispatcher[command](args)
    else:
        raise CommandNotFoundError(command)

def l_command(args, block):
    for line in block:
        yield from process_megatron_command(line[0], line[1:])

def t_command(args):
    timer_duration = float(args[0])
    print(f"Executing timer for {timer_duration} seconds")
    yield from bps.sleep(timer_duration)

def exit_command(args):
    print("Exiting the interpreter.")
    raise SystemExit

def lograte(args):
    print(f"Setting lograte to {args[0]}")
    yield from bps.null()

def email(args):
    # need to implement
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

def log(args):
    pv_list = args
    print(f"Adding to log list: {pv_list}")
    yield from bps.null()

def print_command(args):
    text = ' '.join(args)
    print(f"Executing 'print' command with text: {text}")
    yield from bps.null()

def run(args):
    script_name = args[0]
    print(f"Running script: {script_name}")
    # implement here 
    yield from bps.null()

def setao(args):
    sp = args[0]
    value = float(args[1])
    print(f"Setting analog output {sp} to {value}")
    # implement here
    yield from bps.null()

def setdo(args):
    pv = args[0]
    value = int(args[1])
    print(f"Setting digital output {pv} to {value}")
    # implement here 
    yield from bps.null()

def stop(args):
    script_name = args[0]
    print(f"Stopping script: {script_name}")
    # implement here
    yield from bps.null()

def var(args):
    variable = args[0]
    expression = args[1]
    print(f"Setting variable {variable} to {expression}")
    # implement here 
    yield from bps.null()

def waitai(args):
    pv = args[0]
    operator = args[1]
    value = float(args[2])
    print(f"Waiting for analog input {pv} to be {operator} {value}")
    # implement here 
    yield from bps.null()

def waitdi(args):
    pv = args[0]
    value = args[1]
    print(f"Waiting for digital input {pv} to be {value}")
    # implement here   
    yield from bps.null()
