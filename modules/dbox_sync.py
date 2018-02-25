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
import dropbox
import six


def main(token, local_dir, dbox_dir):
    """TODO"""

    dbx = dropbox.Dropbox(token)
    local_dir = os.path.expanduser(local_dir).rstrip('/')

    print('Dropbox folder name:', dbox_dir)
    print('Local directory:', local_dir)
    if not os.path.exists(local_dir):
        print(local_dir, 'does not exist on your file system')
        sys.exit(1)
    elif not os.path.isdir(local_dir):
        print(local_dir, 'is not a folder on your file system')
        sys.exit(1)
    print('')

    # Only one directory level to walk
    full_filenames = glob.glob('{}/*.*'.format(local_dir))
    local_filenames = [filename.split('/')[-1] for filename in full_filenames]
    # Determine all files in Dropbox Directory to sync
    listing = list_folder(dbx, dbox_dir)

    # Check for local files
    for filename in local_filenames:
        fullname = os.path.join(local_dir, filename)
        print('Local filename:', filename)
        if not isinstance(filename, six.text_type):
            filename = filename.decode('utf-8')
        nname = unicodedata.normalize('NFC', filename)
        if filename.startswith('.'):
            print('Skipping dot file:', filename)
        elif filename.startswith('@') or filename.endswith('~'):
            print('Skipping temporary file:', filename)
        elif filename.endswith('.pyc') or filename.endswith('.pyo'):
            print('Skipping generated file:', filename)
        elif nname in listing:
            md = listing[nname]
            # mtime = os.path.getmtime(fullname)
            # mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
            size = os.path.getsize(fullname)
            if (isinstance(md, dropbox.files.FileMetadata) and size == md.size):
                print('Already synced [stats match]:', filename)
                # # Breaks when local file timestamp differs from dbox timezone
                # if mtime_dt != md.client_modified:
                #     print('Warn: timestamps disagree > local:', mtime_dt, '| dbox:', md.client_modified)
            else:
                print('Exists, but with different stats, downloading and replacing:', filename)
                os.unlink(fullname)
                download(dbx, dbox_dir, fullname)
        else:
            print('No corresponding file on dbox, deleting local file:', fullname)
            os.unlink(fullname)

        print('')  # break

    # Download any new files not found locally
    for idx, db_fn in enumerate(listing.keys()):
        if db_fn not in local_filenames:
            fullname = '{}/{}'.format(local_dir, db_fn)
            print('Downloading new file:', db_fn, 'to:', fullname)
            download(dbx, dbox_dir, fullname)
            print('')  # break


def list_folder(dbx, folder, subfolder=''):
    """Return inventory list of Dropbox Folder

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv


def download(dbx, dbox_dir, local_name):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    dbox_fn = '{}/{}'.format(dbox_dir.rstrip('/'), local_name.split(os.sep)[-1])
    while '//' in dbox_fn:
        dbox_fn = dbox_fn.replace('//', '/')
    with stopwatch('download'):
        try:
            res = dbx.files_download_to_file(local_name, dbox_fn)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    return res


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))


if __name__ == '__main__':
    access_token = config.read_json('access_token')
    balloon_dir = config.read_json('balloon_dir')
    main(access_token, '~/Desktop/_tmp', balloon_dir)
