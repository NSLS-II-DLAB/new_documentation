from ophyd import EpicsMotor
import bluesky.plan_stubs as bps
from megatron.exceptions import CommandNotFoundError

galil = EpicsMotor('sim:mtr1', name='galil')
galil.wait_for_connection(timeout=5)

def process_motor_command(command, args):
    command_dispatcher = {
        "ac": ac, "af": af, "ba": ba, "bg": bg, "bi": bi, "bl": bl, "bm": bm,
        "bt": bt, "bz": bz, "cc": cc, "ce": ce, "cn": cn, "dc": dc, "dp": dp,
        "er": er, "fa": fa, "fe": fe, "fl": fl, "fv": fv, "hv": hv, "ib": ib,
        "iht": iht, "il": il, "kd": kd, "ki": ki, "kp": kp, "ld": ld, "mo": mo,
        "mt": mt, "op": op, "pa": pa, "pr": pr, "pv": pv, "sc": sc, "sh": sh,
        "sp": sp, "st": st, "ta": ta, "tp": tp, "xq": xq
    }
    
    if command in command_dispatcher:
        yield from command_dispatcher[command](args)
    else:
        raise CommandNotFoundError(command)

def ac(args):
    acceleration = float(args[0])
    print(f"Setting acceleration to {acceleration}")
    yield from bps.mv(galil.acceleration, acceleration)

def af(args):
    print(f"Executing 'af' (Analog Feedback Select) command with args: {args}")
    yield from bps.null()

def ba(args):
    print(f"Executing 'ba' command with args: {args}")
    yield from bps.null()

def bg(args):
    print(f"Executing 'bg' (Begin movement) command")
    yield from bps.mv(galil, galil.position)

def bi(args):
    print(f"Executing 'bi' command with args: {args}")
    yield from bps.null()

def bl(args):
    print(f"Executing 'bl' (Reverse Software Limit) command with args: {args}")
    yield from bps.null()

def bm(args):
    print(f"Executing 'bm' command with args: {args}")
    yield from bps.null()

def bt(args):
    print(f"Executing 'bt' command with args: {args}")
    yield from bps.null()

def bz(args):
    print(f"Executing 'bz' (Brushless Zero) command with args: {args}")
    yield from bps.null()

def cc(args):
    print(f"Executing 'cc' (Configure Communications) command with args: {args}")
    yield from bps.null()

def ce(args):
    print(f"Executing 'ce' (Configure Encoder) command with args: {args}")
    yield from bps.null()

def cn(args):
    print(f"Executing 'cn' command with args: {args}")
    yield from bps.null()

def dc(args):
    deceleration = float(args[0])
    print(f"Setting deceleration to {deceleration}")
    yield from bps.mv(galil.acceleration, deceleration)  

def dp(args):
    position = float(args[0])
    print(f"Defining position: {position}")
    galil.set_current_position(position)
    yield from bps.null()

def er(args):
    error_limit = float(args[0])
    print(f"Setting error limit to {error_limit}")
    yield from bps.mv(galil.error_limit, error_limit)  # placeholder, depends on the motor configuration

def fa(args):
    print(f"Executing 'fa' (Acceleration Feedforward) command with args: {args}")
    yield from bps.null()

def fe(args):
    print(f"Executing 'fe' (Find Edge) command with args: {args}")
    yield from bps.null()

def fl(args):
    print(f"Executing 'fl' (Forward Software Limit) command with args: {args}")
    yield from bps.null()

def fv(args):
    velocity_feedforward = float(args[0])
    print(f"Setting velocity feedforward to {velocity_feedforward}")
    yield from bps.mv(galil.velocity, velocity_feedforward)

def hv(args):
    homing_velocity = float(args[0])
    print(f"Setting homing velocity to {homing_velocity}")
    yield from bps.mv(galil.homing_velocity, homing_velocity)

def ib(args):
    print(f"Executing 'ib' command with args: {args}")
    yield from bps.null()

def iht(args):
    print(f"Executing 'iht' (Close IP Handle) command with args: {args}")
    yield from bps.null()

def il(args):
    integrator_limit = float(args[0])
    print(f"Setting integrator limit to {integrator_limit}")
    yield from bps.mv(galil.integrator_limit, integrator_limit)

def kd(args):
    derivative_gain = float(args[0])
    print(f"Setting derivative gain to {derivative_gain}")
    yield from bps.mv(galil.kd, derivative_gain)

def ki(args):
    integrator_gain = float(args[0])
    print(f"Setting integrator gain to {integrator_gain}")
    yield from bps.mv(galil.ki, integrator_gain)

def kp(args):
    proportional_gain = float(args[0])
    print(f"Setting proportional gain to {proportional_gain}")
    yield from bps.mv(galil.kp, proportional_gain)

def ld(args):
    print(f"Executing 'ld' (Limit Disable) command with args: {args}")
    yield from bps.null()

def mo(args):
    print(f"Turning motor off")
    galil.stop()  # assume motor off is the same as stop
    yield from bps.null()

def mt(args):
    motor_type = args[0]
    print(f"Setting motor type to {motor_type}")
    yield from bps.null()

def op(args):
    output_port = int(args[0])
    print(f"Setting output port: {output_port}")
    yield from bps.null()

def pa(args):
    absolute_position = float(args[0])
    print(f"Executing 'pa' (set absolute position) command with position: {absolute_position}")
    yield from bps.mv(galil, absolute_position)

def pr(args):
    relative_position = float(args[0])
    print(f"Executing 'pr' (set relative position) command with position: {relative_position}")
    yield from bps.mvr(galil, relative_position)

def pv(args):
    print(f"Executing 'pv' command with args: {args}")
    yield from bps.null()

def sc(args):
    print(f"Executing 'sc' (stop motor) command")
    galil.stop()
    yield from bps.null()

def sh(args):
    print(f"Executing 'sh' (Servo Here) command")
    yield from bps.null()

def sp(args):
    speed = float(args[0])
    print(f"Executing 'sp' (set speed) command with args: {speed}")
    yield from bps.mv(galil.velocity, speed)

def st(args):
    print(f"Executing 'st' (stop motor) command")
    galil.stop()
    yield from bps.null()

def ta(args):
    print(f"Executing 'ta' command with args: {args}")
    yield from bps.null()

def tp(args):
    current_position = galil.position
    print(f"Executing 'tp' (tell position), current position: {current_position}")
    yield from bps.null()

def xq(args):
    print(f"Executing 'xq' (execute program) command with args: {args}")
    yield from bps.null()
