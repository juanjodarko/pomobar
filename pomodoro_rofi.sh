#!/bin/bash

options="Start\nPause\nResume\nStop\nSet Work/Break Time"
selection=$(echo -e "$options" | rofi -dmenu -p "Pomodoro")

case "$selection" in
    "Start")
        python ~/.config/polybar/pomodoro/pomodoro.py start
        ;;
    "Pause")
        python ~/.config/polybar/pomodoro/pomodoro.py pause
        ;;
    "Resume")
        python ~/.config/polybar/pomodoro/pomodoro.py resume
        ;;
    "Stop")
        python ~/.config/polybar/pomodoro/pomodoro.py stop
        ;;
    "Set Work/Break Time")
        WORK_TIME=$(rofi -dmenu -p "Set Work Time (minutes)")
        BREAK_TIME=$(rofi -dmenu -p "Set Break Time (minutes)")
        LONG_BREAK_TIME=$(rofi -dmenu -p "Set Long Break Time (minutes)")
        python ~/.config/polybar/pomodoro/pomodoro.py set $WORK_TIME $BREAK_TIME $LONG_BREAK_TIME
        ;;
esac
