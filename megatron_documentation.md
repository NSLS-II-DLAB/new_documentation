Megatron Control System Documentation
=====================================

Table of Contents
-----------------

*   [Basic Commands](#basic-commands)
*   [Script Overview and Flow Control](#script-overview-and-flow-control)
*   [Script Functionality Breakdown](#script-functionality-breakdown)
*   [Debugging and Testing](#debugging-and-testing)

* * *

Introduction
------------

The **Megatron Control System** is a powerful scripting language used for controlling hardware components, monitoring processes, and executing automated tasks in industrial and laboratory environments. This documentation provides detailed descriptions of all commands, their syntax, and examples to help users effectively use the system.

* * *

Basic Commands
--------------

### `alm`

**Description**: Controls the AllMotion device.

*   **Syntax**: `alm "text"`
*   **Example**:
    
        alm "start"
        alm "stop"
        
    
*   **Usage**: Used to control and send commands to AllMotion devices. See `alm help` for further details on subcommands.

### `edit`

**Description**: Opens a script for editing.

*   **Syntax**: `edit "script_name"`
*   **Example**:
    
        edit "process_control_script"
        
    
*   **Usage**: Opens the specified script for editing within the control environment.

### `email`

**Description**: Sends an email from `depositionlab@gmail.com`.

*   **Syntax**: `email "Subject", "Message", to_address1[, to_address2, ...]`
*   **Example**:
    
        email "Process Completed", "The deposition process has finished.", "admin@example.com"
        
    
*   **Usage**: Sends email notifications for process completions, errors, or other events.

### `exec`

**Description**: Executes Python code. Reserved for internal use.

*   **Syntax**: `exec "python_code"`
*   **Example**:
    
        exec "print('Internal use only')"
        
    
*   **Usage**: Used to execute Python code within the script. Primarily for internal development.

### `failif`

**Description**: Stops a script if a digital input changes to a specific value.

*   **Syntax**: `failif "PV", y, "script_to_run_on_fail"`
*   **Example**:
    
        failif "DoorOpen", 1, "emergency_stop"
        
    
*   **Usage**: Stops the current script and runs another if a process variable (PV) meets the specified condition.

### `failifoff`

**Description**: Disables the `failif` condition for a specified PV.

*   **Syntax**: `failifoff "PV"`
*   **Example**:
    
        failifoff "DoorOpen"
        
    
*   **Usage**: Turns off the fail condition for a specific PV.

### `fopen`

**Description**: Opens a file for writing data.

*   **Syntax**: `fopen "filename"`
*   **Example**:
    
        fopen "process_log.txt"
        
    
*   **Usage**: Opens the specified file to log process data or write information.

### `fprint`

**Description**: Appends text to a file opened with `fopen`.

*   **Syntax**: `fprint "filename", "text"`
*   **Example**:
    
        fprint "process_log.txt", "Process started."
        
    
*   **Usage**: Writes information to a file for tracking or logging purposes.

### `h` / `help`

**Description**: Displays help information for a specific command.

*   **Syntax**: `help [keyword]`
*   **Example**:
    
        help "log"
        help "setdo"
        
    
*   **Usage**: Displays detailed information about the command and its usage.

### `ion`

**Description**: Sends a command directly to the ION 1500 system.

*   **Syntax**: `ion "text"`
*   **Example**:
    
        ion "set voltage 1000"
        
    
*   **Usage**: Used for controlling the ION 1500, typically to adjust voltage or power output.

### `l`

**Description**: Loops the following block of commands `n` times.

*   **Syntax**: `ln`
*   **Example**:
    
        l5
          print "Iteration"
        n
        
    
*   **Usage**: Repeats a block of commands for a specified number of iterations.

### `length`

**Description**: Retrieves the length of a queue and stores it in a variable.

*   **Syntax**: `length "queue_name", "variable"`
*   **Example**:
    
        length "taskQueue", "queueLength"
        
    
*   **Usage**: Retrieves the number of items in a queue and stores the result in the specified variable.

### `log`

**Description**: Adds a process variable (PV) to the log list for tracking.

*   **Syntax**: `log "PV1" [, "PV2", ...]`
*   **Example**:
    
        log "Temperature"
        log "Pressure", "FlowRate"
        
    
*   **Usage**: Logs specified process variables to monitor their values over time.

### `lograte`

**Description**: Sets the logging interval for process variables.

*   **Syntax**: `lograte n`
*   **Example**:
    
        lograte 5
        
    
*   **Usage**: Adjusts how frequently process variables are logged, in seconds.

### `monitor`

**Description**: Monitors digital PLC changes.

*   **Syntax**: `monitor [on | off]`
*   **Example**:
    
        monitor on
        
    
*   **Usage**: Turns monitoring on or off for digital PLC changes.

### `mos`

**Description**: Controls the MOS system with specified settings.

*   **Syntax**: `mos (on | off), [samples], [data_points], [timeout]`
*   **Example**:
    
        mos on, 100, 10, 60
        
    
*   **Usage**: Turns the MOS system on or off and sets sample sizes, data points, and timeouts.

### `nolog`

**Description**: Removes a process variable from the log list.

*   **Syntax**: `nolog "PV"`
*   **Example**:
    
        nolog "Pressure"
        
    
*   **Usage**: Stops logging the specified process variable.

### `overview`

**Description**: Opens an overview window for monitoring.

*   **Syntax**: `overview [force]`
*   **Example**:
    
        overview
        
    
*   **Usage**: Opens a graphical overview of system data and current state.

### `plot`

**Description**: Plots process variables for real-time monitoring.

*   **Syntax**: `plot "PV1" [, "PV2", ...] [+x,y,width,height]`
*   **Example**:
    
        plot "Temperature", "Pressure" +100,100,400,300
        
    
*   **Usage**: Creates a plot of one or more process variables with optional positioning and size.

### `pop`

**Description**: Removes a value from a queue and stores it in a variable.

*   **Syntax**: `pop "queue_name", "variable"`
*   **Example**:
    
        pop "taskQueue", "currentTask"
        
    
*   **Usage**: Retrieves and removes the first value from the specified queue and stores it in a variable.

### `print`

**Description**: Prints text to the console.

*   **Syntax**: `print "text"`
*   **Example**:
    
        print "Process starting"
        
    

### `profile`

**Description**: Loads a PVT profile for motion control.

*   **Syntax**: `profile "profile_name", [equation_velocity], [equation_position]`
*   **Example**:
    
        profile "standard_profile", "%velocity%", "%position%"
        
    

### `push`

**Description**: Appends a value to a queue.

*   **Syntax**: `push "queue_name", "value"`
*   **Example**:
    
        push "taskQueue", "newTask"
        
    

### `restart`

**Description**: Restarts or reconnects specified components.

*   **Syntax**: `restart [components]`
*   **Example**:
    
        restart "network"
        
    

### `resume`

**Description**: Resumes a paused script.

*   **Syntax**: `resume "script_name"`
*   **Example**:
    
        resume "data_collection"
        
    

### `run`

**Description**: Runs a specified script.

*   **Syntax**: `run "script_name"`
*   **Example**:
    
        run "data_collection_script"
        
    

### `say`

**Description**: Uses text-to-speech to read a string aloud.

*   **Syntax**: `say "text"`
*   **Example**:
    
        say "Process complete"
        
    

### `search`

**Description**: Searches for text in command descriptions.

*   **Syntax**: `search "text"`
*   **Example**:
    
        search "log"
        
    

### `setao`

**Description**: Sets an analog output.

*   **Syntax**: `setao "SP", value`
*   **Example**:
    
        setao "MFC1 Setpoint", 5.0
        
    

### \`set

do\` **Description**: Sets a digital output.

*   **Syntax**: `setdo "PV", value`
*   **Example**:
    
        setdo "Relay1", 1
        
    

### `stop`

**Description**: Stops a running script.

*   **Syntax**: `stop "script_name"`
*   **Example**:
    
        stop "data_collection_script"
        
    

### `stops`

**Description**: Stops a running service.

*   **Syntax**: `stops "service_name"`
*   **Example**:
    
        stops "network_service"
        
    

### `t`

**Description**: Pauses execution for a specified number of seconds.

*   **Syntax**: `tn`
*   **Example**:
    
        t10  # Pauses for 10 seconds
        
    

### `tic`

**Description**: Controls the TIC thermocouple gauge.

*   **Syntax**: `tic [gauge1 | gauge2], "command"`
*   **Example**:
    
        tic gauge1, "degas"
        
    

### `tts`

**Description**: Enables or disables text-to-speech for console output.

*   **Syntax**: `tts [on | off]`
*   **Example**:
    
        tts on
        
    

### `var`

**Description**: Sets a variable to a specified value or expression.

*   **Syntax**: `var "variable", "expression"`
*   **Example**:
    
        var "setpoint", 100
        
    

### `waitai`

**Description**: Waits for an analog input to meet a condition.

*   **Syntax**: `waitai "PV", operator, value [, tolerance] [, timeout]`
*   **Example**:
    
        waitai "Pressure", ">", 50.0
        
    

### `waitdi`

**Description**: Waits for a digital input to meet a condition.

*   **Syntax**: `waitdi "PV", value`
*   **Example**:
    
        waitdi "DoorClosed", 1
        
    

Here's the full section on **Script Overview and Flow Control** for the **Megatron Control System Documentation**:

* * *

Script Overview and Flow Control
--------------------------------

### Introduction

In the **Megatron Control System**, scripts are sequences of commands executed to control hardware components, monitor processes, and automate tasks. These scripts can range from simple sequences of digital or analog controls to complex logic-based operations involving loops, conditions, file handling, and timing controls. Understanding how commands are combined and executed in scripts is crucial for effective automation and control.

* * *

### Command Sequencing

Commands in Megatron are executed in sequence, one after the other, unless control commands like loops, conditions, or file operations change the flow. A typical script might include commands to start a process, log data, control hardware components, and manage timing.

**Example Script**:

    setdo "Relay1", 1            # Turn on relay 1
    log "Temperature"            # Log the temperature
    t10                         # Wait for 10 seconds
    setdo "Relay1", 0            # Turn off relay 1
    

In this script:

1.  `setdo` turns on a relay.
2.  `log` tracks the temperature.
3.  `t` pauses the script for 10 seconds before proceeding.
4.  `setdo` then turns off the relay.

This sequence illustrates the basic structure of command execution.

* * *

### Loops and Repetition (`l` Command)

Loops are used to repeat a block of commands multiple times. The `l` command defines how many times the subsequent block of commands will execute. The loop ends with an `n` to mark the conclusion of the loop block.

**Syntax**:

    ln
        <commands>
    n
    

**Example**:

    l3                         # Loop the following block 3 times
        setdo "Relay1", 1
        t5                     # Wait 5 seconds
        setdo "Relay1", 0
        t2                     # Wait 2 seconds before restarting loop
    n
    

In this example:

*   The `l3` command creates a loop that runs the block three times.
*   Inside the loop, relay 1 is turned on, held for 5 seconds, and then turned off, followed by a 2-second pause before repeating.

* * *

### Conditional Controls: `failif` and `failifoff`

Conditions are essential for handling process failures or system triggers. The `failif` command is used to interrupt the script if a process variable (PV) reaches a specified condition. When triggered, the specified fail script is executed.

**Syntax**:

    failif "PV", condition_value, "fail_script"
    failifoff "PV"
    

*   `failif` sets up a condition that checks if the process variable `PV` meets the `condition_value`. If true, the script will stop, and the `fail_script` will run.
*   `failifoff` disables the `failif` condition for a given process variable.

**Example**:

    failif "Pressure", 0, "emergency_shutdown"   # If pressure drops to 0, trigger emergency shutdown
    setdo "Pump", 1                              # Turn on the pump
    t10                                         # Wait 10 seconds
    setdo "Pump", 0                              # Turn off the pump
    failifoff "Pressure"                         # Disable the fail condition
    

In this example:

*   The script monitors the "Pressure" variable.
*   If the pressure drops to 0, the script halts and runs the "emergency\_shutdown" script.
*   After the main actions (controlling the pump), the fail condition is disabled.

* * *

### File Manipulation: `fopen` and `fprint`

The Megatron system allows you to log data and process outputs to files using the `fopen` and `fprint` commands. These commands open a file and append text to it, respectively.

*   `fopen`: Opens a file for writing.
*   `fprint`: Appends specified text to an open file.

**Syntax**:

    fopen "filename"
    fprint "filename", "text"
    

**Example**:

    fopen "process_log.txt"                # Open or create the log file
    fprint "process_log.txt", "Process started at 10:00"   # Append data to the log file
    setdo "Relay1", 1                      # Turn on relay
    t10                                   # Wait 10 seconds
    fprint "process_log.txt", "Relay turned off"    # Append another log entry
    setdo "Relay1", 0                      # Turn off relay
    

In this example:

*   The script logs the start and end of a process to a file named `process_log.txt`.
*   This approach is useful for tracking events, error logging, or recording process outputs.

* * *

### Timing Control: `t` Command

The `t` command is used to pause script execution for a specified number of seconds. This is particularly useful when waiting for a process to complete or for a device to stabilize before proceeding with the next command.

**Syntax**:

    t[seconds]
    

**Example**:

    setdo "Relay1", 1          # Turn on relay 1
    t5                        # Wait for 5 seconds
    setdo "Relay1", 0          # Turn off relay 1
    

In this script:

*   The relay is turned on.
*   The script then waits for 5 seconds before proceeding to turn off the relay.

* * *

### Flow of Execution

Megatron scripts execute commands in sequence unless a loop, conditional control, or timing is introduced. When commands are combined, they create a workflow that may involve monitoring, hardware control, logging, and decision-making based on process conditions.

**Example of Full Workflow**:

    fopen "logfile.txt"
    log "Temperature"
    lograte 5
    
    failif "Pressure", 0, "emergency_shutdown"
    
    l10                             # Loop 10 times
        setdo "Relay1", 1            # Turn on relay 1
        fprint "logfile.txt", "Relay 1 activated"
        t5                          # Wait 5 seconds
        setdo "Relay1", 0            # Turn off relay 1
        fprint "logfile.txt", "Relay 1 deactivated"
    n
    
    failifoff "Pressure"
    

This script demonstrates:

1.  **File Handling**: A file is opened to log data.
2.  **Logging**: The temperature is logged every 5 seconds.
3.  **Fail Conditions**: The script stops and triggers an emergency shutdown if the pressure drops to 0.
4.  **Looping**: A block of commands turns the relay on and off in a loop, with corresponding log entries.
5.  **Flow**: The script combines conditionals, looping, file handling, and timing controls to create a well-structured process.

* * *

Script Functionality Breakdown
------------------------------

### Introduction

In the **Megatron Control System**, scripts are written to automate and control various hardware components. Common scripts include operations such as switching relays, controlling pressure, and monitoring system variables. This section breaks down some commonly used scripts, explaining their functionality and the key steps involved. By understanding these examples, users can better apply the commands in their own scripts.

* * *

### Example 1: Relay Switch Control Script

This type of script is commonly used to turn relays on and off, controlling hardware devices like pumps, lights, or other electrical components. The following script demonstrates a simple sequence for toggling a relay, including logging and timed delays.

**Script:**

    fopen "relay_log.txt"                  # Open a file to log relay events
    setdo "Relay1", 1                      # Turn on Relay 1
    fprint "relay_log.txt", "Relay 1 activated"   # Log the relay activation
    t10                                   # Wait 10 seconds
    setdo "Relay1", 0                      # Turn off Relay 1
    fprint "relay_log.txt", "Relay 1 deactivated" # Log the relay deactivation
    

**Key Steps**:

1.  **File Handling**: The `fopen` command opens or creates a log file, `relay_log.txt`, to track the relay status.
2.  **Relay Control**: The `setdo` command turns the relay on (`setdo "Relay1", 1`) and off (`setdo "Relay1", 0`).
3.  **Logging**: The `fprint` command writes information about when the relay is turned on and off to the log file.
4.  **Timing**: The `t` command introduces a 10-second delay between turning the relay on and off.

This script is useful for switching devices on and off with timed delays and logging events for future reference.

* * *

### Example 2: Pressure Monitoring and Control Script

This script demonstrates how to monitor pressure in a system and trigger actions based on pressure values. If the pressure drops below a threshold, the system will initiate a shutdown.

**Script:**

    failif "Pressure", 0, "emergency_shutdown"    # If pressure drops to 0, run the emergency shutdown script
    log "Pressure"                                # Log the pressure
    lograte 5                                     # Log every 5 seconds
    setdo "Pump", 1                               # Turn on the pump
    t60                                          # Wait for 60 seconds
    setdo "Pump", 0                               # Turn off the pump
    failifoff "Pressure"                          # Disable the fail condition for pressure
    

**Key Steps**:

1.  **Failure Condition**: The `failif` command monitors the "Pressure" process variable. If the pressure drops to 0, the `emergency_shutdown` script is triggered to stop the process.
2.  **Logging**: The `log` command records the pressure variable, and `lograte` sets the logging interval to 5 seconds, allowing the pressure to be tracked at regular intervals.
3.  **Pump Control**: The `setdo` command controls the pump by turning it on for 60 seconds (`t 60`) and then turning it off.
4.  **Failure Handling**: The `failifoff` command disables the failure condition at the end of the script, ensuring the system returns to normal.

This script is ideal for controlling hardware components based on environmental or system conditions, such as pressure, temperature, or flow rates.

* * *

### Example 3: Process Automation with Loops

This script demonstrates how to automate repetitive tasks using loops. The script toggles a relay in 5-second intervals and logs each activation/deactivation.

**Script:**

    fopen "automation_log.txt"                   # Open a log file to track automation events
    l10                                         # Repeat the block of commands 10 times
        setdo "Relay1", 1                        # Turn on Relay 1
        fprint "automation_log.txt", "Relay 1 activated"   # Log relay activation
        t5                                      # Wait 5 seconds
        setdo "Relay1", 0                        # Turn off Relay 1
        fprint "automation_log.txt", "Relay 1 deactivated" # Log relay deactivation
        t2                                      # Wait 2 seconds before the next loop
    n
    

**Key Steps**:

1.  **Looping**: The `l10` and `n` commands create a loop that repeats the block of commands 10 times.
2.  **Relay Control**: Inside the loop, the relay is turned on for 5 seconds and then turned off, with a 2-second delay before the next iteration.
3.  **Logging**: The `fprint` command records when the relay is activated and deactivated for each loop iteration.
4.  **Timing**: The `t` command manages the timing for the relay switching and delays between iterations.

This script is useful for automating repetitive tasks in a controlled sequence, such as cycling power to a component or running timed tests.

* * *

### Example 4: Monitoring System Variables and Logging Data

In this script, system variables such as temperature and pressure are continuously monitored and logged. The script demonstrates how to track multiple variables over time and adjust logging rates.

**Script:**

    fopen "system_log.txt"                      # Open a log file to track system data
    log "Temperature"                           # Log the temperature
    log "Pressure"                              # Log the pressure
    lograte 10                                  # Set the logging rate to every 10 seconds
    l20                                        # Loop to log the data 20 times
        fprint "system_log.txt", "Logging data at interval"
        t10                                    # Wait 10 seconds
    n
    

**Key Steps**:

1.  **Logging Setup**: The `log` command tracks the temperature and pressure, while `lograte` sets the logging interval to 10 seconds.
2.  **Looping**: The script logs data at 10-second intervals for 20 iterations using the `l20` loop.
3.  **File Output**: The `fprint` command writes a timestamped log entry for each interval.
4.  **Timing**: The `t10` command introduces a 10-second delay between log entries, ensuring data is captured at the specified intervals.

This script is commonly used for data acquisition, allowing system variables to be recorded at regular intervals for later analysis.

* * *

### Example 5: Emergency Shutdown Script

This script handles emergency conditions, such as pressure dropping to zero, by shutting down the system and stopping all processes.

**Script:**

    fprint "logfile.txt", "Emergency shutdown initiated"    # Log the emergency shutdown
    setdo "Pump", 0                                         # Turn off the pump
    setdo "Heater", 0                                       # Turn off the heater
    setdo "Relay1", 0                                       # Turn off relay 1
    setao "Flow", 0                                         # Set flow to 0
    fprint "logfile.txt", "System shut down completed"
    

**Key Steps**:

1.  **Logging the Event**: The `fprint` command writes the emergency shutdown event to the log file.
2.  **Hardware Control**: The `setdo` command turns off the pump, heater, and relay, while `setao` sets the flow to zero, stopping all processes.
3.  **Completion Logging**: Another `fprint` command records when the shutdown is complete.

This script is typically run when an emergency condition (such as `failif "Pressure" 0`) is triggered, ensuring a safe and orderly shutdown of system components.

* * *

Debugging and Testing
---------------------

### Introduction

Debugging and testing are critical steps in the script development process, ensuring that your Megatron scripts behave as expected. This section provides guidance on effective debugging techniques, focusing on using logging (`log`, `lograte`), checking outputs, and interpreting results. Testing scripts before deploying them in production environments helps to catch issues early, reduce downtime, and improve system reliability.

* * *

### Using Logging for Debugging

Logging is one of the most powerful tools for testing and debugging in the **Megatron Control System**. By logging key process variables, you can observe the system's behavior in real time, understand how inputs are changing, and identify issues such as incorrect sensor readings or unexpected timing.

#### Logging Process Variables (`log` and `lograte`)

The `log` command allows you to track specific process variables (PVs) over time, while the `lograte` command controls how frequently these variables are logged. Logged data is stored either in the console or a specified file, which can then be reviewed to identify issues.

*   **`log`**: Monitors specific variables.
*   **`lograte`**: Sets the frequency (in seconds) at which these variables are logged.

**Syntax**:

    log "PV1", "PV2", ...     # Monitors process variables
    lograte n                 # Sets log interval to n seconds
    

**Example**:

    log "Temperature", "Pressure"    # Log temperature and pressure
    lograte 5                        # Log every 5 seconds
    

In this example, the script logs the `Temperature` and `Pressure` every 5 seconds. By reviewing these log outputs, you can check if the system is behaving as expected (e.g., if the pressure is increasing or decreasing as desired).

#### File-Based Logging with `fopen` and `fprint`

If you need to save logs to a file, use `fopen` and `fprint` to append log entries into a specified file. This is particularly useful for long-term debugging or for capturing logs during complex operations.

**Syntax**:

    fopen "filename"              # Opens or creates a log file
    fprint "filename", "text"     # Appends log entries to the file
    

**Example**:

    fopen "debug_log.txt"                    # Open the log file
    log "Temperature"                        # Log temperature
    lograte 10                               # Log every 10 seconds
    fprint "debug_log.txt", "Starting debug" # Log a custom message
    

Here, logs are written both to the console and saved in a file named `debug_log.txt`. This is helpful for tracking issues over long periods or debugging while the system is not being actively monitored.

* * *

### Interpreting Log Output

When debugging with logs, it's important to know how to interpret the output. Here are a few things to look out for:

1.  **Expected Value Ranges**:
    
    *   Verify that logged values are within the expected ranges. For example, if the temperature should be between 50°C and 100°C, make sure the values stay within this range over time.
2.  **Rate of Change**:
    
    *   Look at how values change between log intervals. For example, if a pressure reading should gradually increase, make sure the rate of change is consistent and that there are no sudden drops or spikes.
3.  **Timestamps and Event Timing**:
    
    *   Ensure that key events are happening at the right times. If you're controlling a relay and logging its state, check the timing of when it's activated and deactivated, comparing this with expected wait times or conditions.

**Example Output**:

    Temperature: 60°C
    Pressure: 25 psi
    Relay 1: ON
    ---
    Temperature: 62°C
    Pressure: 26 psi
    Relay 1: OFF
    

In this log output, you can track how the temperature and pressure values change over time, as well as when Relay 1 is turned on and off. If the values deviate from what’s expected, there may be a hardware issue or an error in the script logic.

* * *

### Testing with Fail Conditions (`failif`)

Another way to test scripts is by using `failif` commands to trigger alternative behavior when specific conditions are met. This is useful for simulating failure scenarios and ensuring that your failover or emergency processes are working as intended.

**Syntax**:

    failif "PV", condition, "fail_script"
    

**Example**:

    failif "Pressure", 0, "emergency_shutdown"   # Trigger emergency shutdown if pressure drops to 0
    

In this example, the script will trigger the `emergency_shutdown` script if the `Pressure` process variable drops to 0. Testing fail conditions like this ensures that the system behaves correctly during critical failures.

* * *

### Step-by-Step Testing with Timing Controls (`t`)

Use the `t` command to introduce controlled delays between commands during testing. This is useful for:

*   Verifying that commands are executed in the correct order.
*   Ensuring hardware components have time to respond.
*   Debugging timing issues where operations happen too quickly or too slowly.

**Example**:

    setdo "Relay1", 1           # Turn on relay
    t10                        # Wait 10 seconds
    setdo "Relay1", 0           # Turn off relay
    

In this example, the script waits for 10 seconds after turning on Relay 1 before proceeding. By adjusting the time delay with `t`, you can test the impact of timing changes on the overall process.

* * *

### Incremental Testing with Loops (`l`)

When testing repetitive processes, such as toggling relays or logging data, use loops (`l`) to run a block of commands multiple times. Start with a low number of iterations to ensure everything works as expected before expanding the loop.

**Syntax**:

    ln
        <commands>
    n
    

**Example**:

    l5                          # Loop 5 times for initial testing
        setdo "Relay1", 1
        t 5                      # Wait 5 seconds
        setdo "Relay1", 0
        t 2                      # Wait 2 seconds before next loop
    n
    

In this script, the relay is toggled on and off in a loop. Testing the process with a small number of iterations ensures that everything works as expected before scaling up.

* * *

### Testing with Conditional Logic

For scripts that include conditional logic, such as fail conditions or variables that affect flow, it’s important to simulate different scenarios and conditions during testing. This can include:

*   Manually adjusting the values of process variables.
*   Using test scripts to mimic various hardware states.

**Example**:

    var "temperature_threshold", 80            # Set a variable for the temperature threshold
    log "Temperature"                          # Log the temperature
    lograte 10                                 # Log every 10 seconds
    failif "Temperature", >, "temperature_threshold", "overheat_shutdown"  # Trigger shutdown if temperature exceeds threshold
    

In this script, the temperature is monitored and compared to a threshold. If the temperature exceeds 80°C, the `overheat_shutdown` script is triggered. By adjusting the threshold and testing under different conditions, you can verify that the conditional logic is working as expected.

* * *

### General Debugging Tips

*   **Start Simple**: Begin testing with small, simple scripts before building more complex ones. This will help isolate issues early on.
*   **Test in Steps**: Test sections of your script individually before running the entire script.
*   **Use Log Outputs**: Log everything you can—this is especially useful for tracking the flow of operations and catching any unexpected behavior.
*   **Check Hardware Response**: Ensure that hardware components, such as relays or pumps, are responding as expected to script commands.
*   **Simulate Failures**: Test failure scenarios to ensure that emergency or recovery scripts are triggered when needed.

* * *
