#!/bin/bash

# Get the output from the Python script
output=$(python ~/.config/polybar/pomodoro/pomodoro.py status)
state=$(echo $output | awk '{print $1}')
time=$(echo $output | awk '{print $2}')


# Define icons based on state
case $state in
    work)
        icon=""
        color="#F38BA8"
        ;;
    break)
        icon=""
        color="#A6E3A1"
        ;;
    long_break)
        icon=""
        color="#89DCEB"
        ;;
    paused)
        icon=""
        color="#F9E2AF"
        ;;
    stopped)
        icon=""
        color="#FAB387"
        ;;
    *)
        icon=""
        color="#FFFFFF"
        ;;
esac

# Output formatted string for Polybar
echo "%{F$color}$icon $time%{F-}"
