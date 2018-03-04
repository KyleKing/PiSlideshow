import os
import time

import schedule
from modules import config, dbox_sync, display

local_dir = os.path.expanduser('~/Desktop/Images/')
if not os.path.isdir(local_dir):
    os.mkdir(local_dir)

access_token = config.read_json('access_token', './secret.json')
balloon_dir = config.read_json('balloon_dir', './secret.json')
syncer = dbox_sync.dbox_syncer(access_token, local_dir, balloon_dir)
schedule.every(45).minutes.do(syncer.start_sync)
syncer.start_sync()

disp_con = display.display_control()
schedule.every().day.at('8:30').do(disp_con.toggle)
schedule.every().day.at('21:30').do(disp_con.toggle)

while True:
    schedule.run_pending()
    time.sleep(1)
