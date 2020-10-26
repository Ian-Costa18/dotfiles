#!/bin/python

import subprocess
from time import sleep


def start_astro_scanner():
    query_cmd = 'aplay -l'
    restart_cmd = "pulseaudio --kill; sleep 5; pulseaudio &"

    unplugged = False
    while True:
        s = subprocess.check_output(query_cmd.split(" "))
        if "Astro A20" in str(s) and unplugged:
            print("Restarting PulseAudio")
            subprocess.call(restart_cmd, shell=True)
            unplugged = False
        elif "Astro A20" not in str(s) and not unplugged:
            print("A20 not found, unplugged")
            unplugged = True
        else:
            #print("Sleeping...")
            sleep(1)

