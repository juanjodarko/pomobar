#!/bin/bash

# Get the output from the Python script
output=$(python ~/.config/polybar/pomodoro/pomodoro.py status)
icon=$(echo $output | awk '{print $1}')
time=$(echo $output | awk '{print $2}')

# Format the output for Polybar
case $icon in
    "work")
        echo "%{F#F38BA8} $time%{F-}"
        ;;
    "break")
        echo "%{F#A6E3A1} $time%{F-}"
        ;;
    "long_break")
        echo "%{F#89DCEB} $time%{F-}"
        ;;
    "paused")
        echo "%{F#F9E2AF} $time%{F-}"
        ;;
    "stopped")
        echo "%{F#FAB387} $time%{F-}"
        ;;
    *)
        echo "%{F#FFFFFF}$icon $time%{F-}"
        ;;
esac

