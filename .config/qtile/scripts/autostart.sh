#!/bin/sh
echo "Starting picom"
picom -b &
echo "Starting nitrogen"
nitrogen --restore &
echo "Starting flameshot"
flameshot &
echo "Starting pamac-tray"
pamac-tray &
echo "Starting nm-applet"
nm-applet &
echo "Starting starting polkit"
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
echo "Starting signal"
signal-desktop-beta --start-in-tray > /dev/null 2>&1 &
echo "Starting rclone"
rclone mount SammyTheBEASTGDrive:linux ~/Cloud/SammyTheBEASTGDrive --rc --daemon &
echo "Starting KDEConnect"
/usr/lib/kdeconnectd &
echo "Starting GreenClip"
greenclip daemon
