import sys
import time
from subprocess import Popen, call

import RPi.GPIO as GPIO


def refresh_slideshow(local_dir='~/Desktop/Images/'):
    """Run the FIM Command
        local_dir - path of folder to source display images from
    """
    # Kill any previously running FIM processes
    call_cmd('killall fim')
    # Start new FIM process
    fim_cmd = 'fim --random --quiet -R {}'.format(local_dir)
    fim_cmd += ' -c \'while(1){display;sleep "3";next;}\''
    print('Initiating Shell Command:', fim_cmd)
    Popen(fim_cmd, shell=True)
    time.sleep(10)
    print('')


def call_cmd(cmd_str):
    """Run arbitrary shell command
        cmd_str - arbitrary command
    """
    try:
        status = call(cmd_str, shell=True)
        if status < 0:
            print >>sys.stderr, 'Child was terminated by signal', -status
        else:
            print >>sys.stderr, 'Child returned', status
    except OSError as e:
        print >>sys.stderr, 'Execution failed:', e


class display_control(object):
    """Power display on/off"""

    pin_TFT = 17

    def __init__(self):
        print('Configuring GPIO pins')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_TFT, GPIO.OUT)
        GPIO.output(self.pin_TFT, GPIO.HIGH)
        self.display_on = True  # display should be ON

    def toggle(self):
        print('Toggling TFT state')
        GPIO.output(self.pin_TFT, GPIO.LOW)
        time.sleep(0.75)
        GPIO.output(self.pin_TFT, GPIO.HIGH)
        time.sleep(5)
        self.display_on = not self.display_on
        self.state()

    def state(self):
        print('Display is', 'ON' if self.display_on else 'OFF')

    def close(self):
        print('Releasing GPIO Pins')
        GPIO.cleanup()


if __name__ == '__main__':
    # Only works on Raspberry Pi
    refresh_slideshow()
    display = display_control()
    print('Turning display OFF')
    display.toggle()
    print('Turning display back ON')
    display.toggle()
