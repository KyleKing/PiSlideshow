"""Sync with remote directory. Based on Dropbox updown Example:
    https://github.com/dropbox/dropbox-sdk-python/blob/master/example/updown.py
"""
from __future__ import print_function

import contextlib
import glob
import os
import sys
import time
import unicodedata

import config
import display
import dropbox
import six


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print 'Total elapsed time for %s: %.3f' % (message, t1 - t0)


class dbox_syncer(object):

    def __init__(self, token, local_dir, dbox_dir):
        """Configure directories for syncing
            token - Secret Dropbox authentication token
            local_dir - path to local directory
            dbox_dir - path to corresponding directory on Dropbox
        """
        self.dbx = dropbox.Dropbox(token)
        self.local_dir = os.path.expanduser(local_dir).rstrip('/')
        self.dbox_dir = dbox_dir

        print 'Dropbox folder name:', self.dbox_dir
        print 'Local directory:', self.local_dir
        if not os.path.exists(self.local_dir):
            print 'Error:', self.local_dir, 'does not exist on your file system'
            sys.exit(1)
        elif not os.path.isdir(self.local_dir):
            print 'Error:', self.local_dir, 'is not a folder on your file system'
            sys.exit(1)
        print ''

    def start_sync(self):
        """Initiate Syncing of local directory with Dropbox one"""
        new_imgs = False

        # List local files and remote Dropbox files
        local_fns = [filename.split('/')[-1] for filename in glob.glob('{}/*.*'.format(self.local_dir))]
        listing = self.list_folder(self.dbox_dir)

        # Check for local files
        for filename in local_fns:
            fullname = os.path.join(self.local_dir, filename)
            if not isinstance(filename, six.text_type):
                filename = filename.decode('utf-8')
            norm_name = unicodedata.normalize('NFC', filename)
            if filename.startswith('.'):
                pass
            elif filename.startswith('@') or filename.endswith('~'):
                pass
            elif filename.endswith('.pyc') or filename.endswith('.pyo'):
                pass
            elif norm_name in listing:
                md = listing[norm_name]
                size = os.path.getsize(fullname)
                if not (isinstance(md, dropbox.files.FileMetadata) and size == md.size):
                    print 'Replacing:', filename
                    os.unlink(fullname)
                    self.download(fullname)
                    new_imgs = True
            else:
                print 'No corresponding file on Dropbox. Deleting:', fullname
                os.unlink(fullname)
        print ''  # break
        # Download any new files not found locally
        for idx, db_fn in enumerate(listing.keys()):
            if db_fn not in local_fns:
                fullname = '{}/{}'.format(self.local_dir, db_fn)
                print 'Downloading new file:', db_fn, 'to:', fullname
                self.download(fullname)
                new_imgs = True
        print ''  # break

        # Start the FIM process
        if new_imgs:
            display.refresh_slideshow()

    def list_folder(self, folder, subfolder=''):
        """Return inventory list of Dropbox Folder
            folder - local directory to parse
            subfolder - Not currently supported
        Return a dict mapping unicode filenames to
        FileMetadata|FolderMetadata entries.
        """
        path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
        path = path.replace('//', '/').rstrip('/')
        try:
            with stopwatch('list_folder'):
                res = self.dbx.files_list_folder(path)
        except dropbox.exceptions.ApiError as err:
            print 'Folder listing failed for:', path, '-- assumed empty:', err
            return {}
        else:
            rv = {}
            for entry in res.entries:
                rv[entry.name] = entry
            return rv

    def download(self, local_name):
        """Download file through the Dropbox API
            local_name - full path to a local file
        Return the bytes of the file, or None if it doesn't exist.
        """
        dbox_fn = '{}/{}'.format(self.dbox_dir.rstrip('/'), local_name.split(os.sep)[-1])
        dbox_fn = dbox_fn.replace('//', '/')
        with stopwatch('download'):
            try:
                res = self.dbx.files_download_to_file(local_name, dbox_fn)
            except dropbox.exceptions.HttpError as err:
                print '*** HTTP error', err
                return None
        return res


if __name__ == '__main__':
    # Example script:
    access_token = config.read_json('access_token')
    balloon_dir = config.read_json('balloon_dir')
    dbox_syncer(access_token, '~/Desktop/Images', balloon_dir).start_sync()
