from modules import dbox_sync, config

access_token = config.read_json('access_token', './secret.json')
balloon_dir = config.read_json('balloon_dir', './secret.json')

dbox_sync.main(access_token, '~/Desktop/_tmp/', balloon_dir)
