# import json
import sys
# import time
# from pprint import pprint
from subprocess import Popen, call

# import config as cg
# import RPi.GPIO as GPIO


def refresh_slideshow(local_dir='~/PiSlideShow/test/'):
    """Run the FIM Command
        local_dir - path of folder to source display images from
    """
    # Kill any previously running FIM processes
    call_cmd('killall fim')
    # Start new FIM process
    fim_cmd = 'fim --random --quiet -R {}'.format(local_dir)
    fim_cmd += ' -c \'while(1){display;sleep "2";next;}'
    print 'Initiating Shell Command:', fim_cmd
    Popen(fim_cmd, shell=True)


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


# pin_TFT = 17
# status_file = 'status.json'


# def update_status(new_status, target_file):
#     """Print the JSON object, then write to file"""
#     pprint(new_status)
#     json.dump(new_status, target_file, sort_keys=True, indent=4,
#               ensure_ascii=False)


# def configure():
#     cg.send('Configuring m_TFT')
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(pin_TFT, GPIO.OUT)
#     GPIO.output(pin_TFT, GPIO.HIGH)
#     with open('status.json', 'w') as target_file:
#         new_status = {'on': 'true'}
#         update_status(new_status, target_file)
#     cg.send('< DONE configuring m_TFT')


# def toggle(line):
#     # Get previous status:
#     with open(status_file, 'r') as target_file:
#         p_stat = json.load(target_file)
#         if 'false' in p_stat['on']:
#             new_status = {'on': 'true'}
#         else:
#             new_status = {'on': 'false'}

#     # Keep current screen state:
#     if line.lower() in str(p_stat['on']).lower():
#         cg.send('Already in desired state (' + str(line) + ')')
#     # Toggle TFT State:
#     elif line.lower() in str(new_status['on']).lower():
#         cg.send('Updating state from: ' + str(p_stat['on']))
#         GPIO.output(pin_TFT, GPIO.LOW)
#         time.sleep(0.75)
#         with open(status_file, 'w') as target_file:
#             update_status(new_status, target_file)
#     # Deal with gibberish:
#     else:
#         cg.send("Error: unknown state: " + line)

#     GPIO.output(pin_TFT, GPIO.HIGH)
#     time.sleep(5)
#     cg.send('< DONE toggling m_TFT state')


# def close():
#     GPIO.cleanup()
#     cg.send('< DONE closing m_TFT')


if __name__ == '__main__':
    # Only works on Raspberry Pi
    refresh_slideshow()
