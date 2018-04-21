import os
import time

import schedule
from modules import config, dbox_sync, display

local_dir = os.path.expanduser('~/Desktop/Images/')
if not os.path.isdir(local_dir):
    os.mkdir(local_dir)

# Initialize Dropbox-Syncing Script
access_token = config.read_json('access_token', './secret.json')
balloon_dir = config.read_json('balloon_dir', './secret.json')
syncer = dbox_sync.dbox_syncer(access_token, local_dir, balloon_dir)
schedule.every(60 * 24).minutes.do(syncer.start_sync)

# Schedule display ON/OFF events
disp_con = display.display_control()
schedule.every().day.at('8:10').do(disp_con.toggle)
schedule.every().day.at('21:40').do(disp_con.toggle)

# Refresh the slide show b/c the never ending process may crash if left on too long
# schedule.every().day.at('8:15').do(display.refresh_slideshow)
schedule.every().day.at('8:00').do(display.start_slideshow)
schedule.every().day.at('21:50').do(display.stop_slideshow)

# Initialize Syncing and FIM on startup
syncer.start_sync()
display.refresh_slideshow()

config.send('')
config.send('Fully configured. Beginning loop to checked for queued events')
while True:
    schedule.run_pending()
    time.sleep(1)
