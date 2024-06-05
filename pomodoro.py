import sys
import time
import os
from datetime import datetime, timedelta

WORK_TIME = 25
BREAK_TIME = 5
LONG_BREAK_TIME = 15
SESSIONS_BEFORE_LONG_BREAK = 4
CURRENT_SESSION = 0
STATE = "stopped"
TIMER_FILE = "/tmp/pomodoro_timer"
LOG_FILE = f"{os.path.expanduser('~')}/.pomodoro_log"
REMAINING_TIME_FILE = "/tmp/pomodoro_remaining_time"
STATE_FILE = "/tmp/pomodoro_state"
SESSION_FILE = "/tmp/pomodoro_session"

# Create log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        f.write("Pomodoro Log\n")

def update_timer(time_left):
    with open(TIMER_FILE, 'w') as f:
        f.write(f"{time_left}")

def log_session(state, duration):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()} - {state} session for {duration} minutes\n")

def start_timer(duration, state):
    global STATE, CURRENT_SESSION
    end_time = datetime.now() + timedelta(minutes=duration)

    with open(STATE_FILE, 'w') as f:
        f.write(state)

    with open(SESSION_FILE, 'w') as f:
        f.write(f"{CURRENT_SESSION}")

    while datetime.now() < end_time:
        with open(STATE_FILE, 'r') as f:
            STATE = f.read().strip()
        if STATE == "paused":
            remaining_time = end_time - datetime.now()
            with open(REMAINING_TIME_FILE, 'w') as f:
                f.write(f"{remaining_time.seconds}")
            return

        if STATE == "stopped":
            update_timer("")
            return

        remaining_time = end_time - datetime.now()
        minutes, seconds = divmod(remaining_time.seconds, 60)
        update_timer(f"{minutes}:{seconds:02d}")
        time.sleep(1)

    if state == "work":
        CURRENT_SESSION += 1
    
    next_state = "work"
    next_duration = WORK_TIME
    if state == "work":
        if CURRENT_SESSION >= SESSIONS_BEFORE_LONG_BREAK:
            next_state = "long_break"
            next_duration = LONG_BREAK_TIME
            CURRENT_SESSION = 0
        else:
            next_state = "break"
            next_duration = BREAK_TIME
    
    update_timer("0:00")
    log_session(state, duration)
    start_timer(next_duration, next_state)

def resume_timer():
    global STATE, CURRENT_SESSION
    with open(REMAINING_TIME_FILE, 'r') as f:
        remaining_time = int(f.read())
    with open(STATE_FILE, 'r') as f:
        state = f.read().strip()
    with open(SESSION_FILE, 'r') as f:
        CURRENT_SESSION = int(f.read().strip())
    STATE = "running"
    start_timer(remaining_time / 60, state)

def main():
    global STATE, WORK_TIME, BREAK_TIME, LONG_BREAK_TIME
    if len(sys.argv) < 2:
        print("Usage: pomodoro.py {start|pause|resume|stop|set|status}")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        STATE = "running"
        start_timer(WORK_TIME, "work")
    elif command == "pause":
        STATE = "paused"
        with open(STATE_FILE, 'w') as f:
            f.write(STATE)
    elif command == "resume":
        resume_timer()
    elif command == "stop":
        STATE = "stopped"
        with open(STATE_FILE, 'w') as f:
            f.write(STATE)
        update_timer("")
    elif command == "set":
        WORK_TIME = int(sys.argv[2])
        BREAK_TIME = int(sys.argv[3])
        LONG_BREAK_TIME = int(sys.argv[4])
    elif command == "status":
        with open(TIMER_FILE, 'r') as f:
            print(f.read())
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()

