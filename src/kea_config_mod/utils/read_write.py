# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
File tools
"""
# pylint: disable=too-many-branches
from typing import (IO)
import os
import stat


from .file_tools import make_dir_path
from .file_tools import os_rename


def open_file(path: str, mode: str, encoding: str | None = None) -> IO | None:
    """
    Open a file and return file object
    """
    # pylint: disable=unspecified-encoding, consider-using-with
    try:
        if encoding:
            fob = open(path, mode, encoding=encoding)
        else:
            fob = open(path, mode)
    except OSError as _err:
        fob = None
        # print(f'Error opening file {path} : {err}')
    return fob


def write_file(data: str, targ_dir: str, file: str) -> bool:
    """
    Write out text file
    """
    if not targ_dir:
        return False

    fpath = os.path.join(targ_dir, file)
    okay = write_path_atomic(data, fpath)
    if not okay:
        print(f'Failed to write {fpath}')
        return False
    return True


def write_path_atomic(data: str | list[str],
                      fpath: str,
                      fmode: int = -1,
                      dmode: int = -1,
                      save_prev: bool = False
                      ) -> bool:
    """
    Write data to fpath - atomic version.

    Args:
        data (str | list[str]):
            The data to write to file 'fpath'

        fmode (int):
            If positive number then file has chmod(fmode) applied to it.
            defaults to (rw-r----)
                stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP.

        dmode (int):
            If positive number then any directories that are created
            has chmod(dmode) applied to it.
            defaults to (rwxr-x--):
                stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP

        save_prev (bool):
            If true then if fpath exists it will be moved
            to Prev/xxx

    Return:
        bool:
            Success or fail.
    """
    #
    # Error if no data to write
    #
    if not data:
        print('write_path_atomic: no data to write')
        return False

    #
    # Create dest directories if needed
    #
    dirname = os.path.dirname(fpath)
    if dirname:
        if not make_dir_path(dirname, dmode):
            txt = f'Error making dest dirs {dirname}'
            print(f'write_path_atomic: {txt}')
            return False

    #
    # write temp file in same dir.
    #
    fpath_tmp = fpath + '.tmp'
    fob = open_file(fpath_tmp, "w")
    if not fob:
        return False

    if isinstance(data, list):
        for item in data:
            fob.write(item)
    else:
        fob.write(data)

    fob.flush()
    fd = fob.fileno()
    os.fsync(fd)

    #
    # Set any requested permissions
    #
    if fmode < 0:
        fmode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP

    if fmode > 0:
        try:
            os.chmod(fd, fmode)

        except OSError as err:
            print(f' Warning chmod {fpath}: {err}')

    fob.close()

    #
    # Save any existing to dirname/Prev if requested
    #
    if save_prev and os.path.exists(fpath):
        print(f'\twrite_path_atomic saving {fpath} to Prev\n')
        save_dir = os.path.join(dirname, 'Prev')
        if make_dir_path(save_dir, dmode):
            filename = os.path.basename(fpath)
            saved_path = os.path.join(save_dir, filename)
            os_rename(fpath, saved_path)
        else:
            txt = f'Error making save dir {save_dir}'
            print(f'write_path_atomic: {txt}')
    #
    # rename to real file
    #
    if not os_rename(fpath_tmp, fpath):
        print(f'write_path_atomic rename error: {fpath_tmp}')
        return False
    return True


def copy_file_atomic(src: str, dst: str) -> bool:
    """
    Copy local file from src to dst
    """
    if not os.path.exists(src):
        return True

    fob = open_file(src, "r")
    if not fob:
        return False

    data = fob.read()
    fob.close()
    try:
        src_stat = os.stat(src)
    except OSError:
        # stat failed
        src_stat = None

    okay = write_path_atomic(data, dst)
    if not okay:
        return False

    # Set file time to match src
    if src_stat:
        os.utime(dst, ns=(src_stat.st_atime_ns, src_stat.st_mtime_ns))
    return True


def read_file_path(fpath: str, verb: bool = False) -> str:
    """
    Read a text file
    """
    if not fpath:
        return ''

    data: str = ''
    try:
        fobj = open_file(fpath, 'r')
        if not fobj:
            if verb:
                print(f'Failed to read {fpath}')
            return ''

        data = fobj.read()

    except OSError as err:
        if verb:
            print(f'Error with file {fpath} : {err}')
        data = ''
    return data


def read_file(targ_dir: str, file: str, verb: bool = False) -> str:
    """
    read text file
    """

    if not targ_dir:
        return ''

    fpath = os.path.join(targ_dir, file)
    return read_file_path(fpath, verb)
