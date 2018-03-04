import time

import schedule
from modules import config, dbox_sync

access_token = config.read_json('access_token', './secret.json')
balloon_dir = config.read_json('balloon_dir', './secret.json')

syncer = dbox_sync.dbox_syncer(access_token, '~/Desktop/Images/', balloon_dir)
schedule.every(45).minutes.do(syncer.start_sync)

while True:
    schedule.run_pending()
    time.sleep(1)
