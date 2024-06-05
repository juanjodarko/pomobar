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
LOG_FILE = f"{sys.path[0]}/.pomodoro_log"

# Read icons and colors from command line arguments
ICONS = {
    "work": sys.argv[2] if len(sys.argv) > 2 else "",
    "break": sys.argv[3] if len(sys.argv) > 3 else "",
    "long_break": sys.argv[4] if len(sys.argv) > 4 else "",
    "paused": sys.argv[5] if len(sys.argv) > 5 else "",
    "stopped": sys.argv[6] if len(sys.argv) > 6 else ""
}

COLORS = {
    "work": sys.argv[7] if len(sys.argv) > 7 else "#BF616A",
    "break": sys.argv[8] if len(sys.argv) > 8 else "#A3BE8C",
    "long_break": sys.argv[9] if len(sys.argv) > 9 else "#88C0D0",
    "paused": sys.argv[10] if len(sys.argv) > 10 else "#EBCB8B",
    "stopped": sys.argv[11] if len(sys.argv) > 11 else "#D08770"
}

def update_timer(state, time_left):
    with open(TIMER_FILE, 'w') as f:
        icon = ICONS.get(state, "")
        color = COLORS.get(state, "#D08770")
        f.write(f"%{{F{color}}}{icon} {time_left}%{{F-}}")

def log_session(state, duration):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()} - {state} session for {duration} minutes\n")

def start_timer(duration, state):
    global CURRENT_SESSION
    end_time = datetime.now() + timedelta(minutes=duration)
    
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        minutes, seconds = divmod(remaining_time.seconds, 60)
        update_timer(state, f"{minutes}:{seconds:02d}")
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
    
    update_timer(next_state, "0:00")
    log_session(state, duration)
    start_timer(next_duration, next_state)

def main():
    global STATE, WORK_TIME, BREAK_TIME, LONG_BREAK_TIME
    if len(sys.argv) < 2:
        print("Usage: pomodoro.py {start|pause|resume|stop|set|status} [work_icon] [break_icon] [long_break_icon] [paused_icon] [stopped_icon] [work_color] [break_color] [long_break_color] [paused_color] [stopped_color]")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        STATE = "running"
        start_timer(WORK_TIME, "work")
    elif command == "pause":
        STATE = "paused"
    elif command == "resume":
        STATE = "running"
    elif command == "stop":
        STATE = "stopped"
        update_timer("stopped", "")
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

