#!/bin/bash

# Define the icons and colors as environment variables
export POMODORO_WORK_ICON=""
export POMODORO_BREAK_ICON=""
export POMODORO_LONG_BREAK_ICON=""
export POMODORO_PAUSED_ICON=""
export POMODORO_STOPPED_ICON=""
export POMODORO_WORK_COLOR="#BF616A"
export POMODORO_BREAK_COLOR="#A3BE8C"
export POMODORO_LONG_BREAK_COLOR="#88C0D0"
export POMODORO_PAUSED_COLOR="#EBCB8B"
export POMODORO_STOPPED_COLOR="#D08770"

options="Start\nPause\nResume\nStop\nSet Work/Break Time"
selection=$(echo -e "$options" | rofi -dmenu -p "Pomodoro")

case "$selection" in
    "Start")
        python ~/.config/polybar/pomodoro.py start "$POMODORO_WORK_ICON" "$POMODORO_BREAK_ICON" "$POMODORO_LONG_BREAK_ICON" "$POMODORO_PAUSED_ICON" "$POMODORO_STOPPED_ICON" "$POMODORO_WORK_COLOR" "$POMODORO_BREAK_COLOR" "$POMODORO_LONG_BREAK_COLOR" "$POMODORO_PAUSED_COLOR" "$POMODORO_STOPPED_COLOR"
        ;;
    "Pause")
        python ~/.config/polybar/pomodoro.py pause
        ;;
    "Resume")
        python ~/.config/polybar/pomodoro.py resume
        ;;
    "Stop")
        python ~/.config/polybar/pomodoro.py stop
        ;;
    "Set Work/Break Time")
        WORK_TIME=$(rofi -dmenu -p "Set Work Time (minutes)")
        BREAK_TIME=$(rofi -dmenu -p "Set Break Time (minutes)")
        LONG_BREAK_TIME=$(rofi -dmenu -p "Set Long Break Time (minutes)")
        python ~/.config/polybar/pomodoro.py set $WORK_TIME $BREAK_TIME $LONG_BREAK_TIME
        ;;
esac
