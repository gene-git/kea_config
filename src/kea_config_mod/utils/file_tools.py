# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
file_utils
"""
import os
import stat


def get_flist(indir: str,
              which: str = 'name',
              links: bool = True,
              recurse: bool = False) -> list[str]:
    """
    read directory and return list of files or links (not dirs)
     - include links if links is True
     - which : name or path
     - recurse on dirs if recurs is True
    """
    if recurse and which == 'name':
        txt = 'recursion must return path not filename - fixing'
        print(f'Warning get_flist: {txt}')
        which = 'path'

    flist: list[str] = []
    if dir_exists(indir):
        scan = os.scandir(indir)
        for item in scan:
            if item.is_file() or (links and item.is_symlink()):
                if which == 'name':
                    flist.append(item.name)
                else:
                    flist.append(item.path)
            elif recurse and item.is_dir():
                flist += get_flist(item.path, which=which,
                                   links=links, recurse=recurse)
        scan.close()
    return flist


def dir_exists(fname: str) -> bool:
    """
    check if dir exists
    """
    res = False
    if os.path.exists(fname):
        res = os.path.isdir(fname)

    return res


def realpath(path: str) -> str:
    """
    returns the absolute realpath (no symlinks, no . or ..)
    """
    realp = os.path.abspath(os.path.realpath(path))
    return realp


def os_rename(old_path: str, new_path: str) -> bool:
    """
    Rename a file - if new_path exists it is first removed
    new_path must either not exist or be file or an empty directory.
    """
    if not (old_path and new_path):
        return True

    #
    # Check if destination exists
    #
    if os.path.exists(new_path):
        if os.path.isdir(new_path):
            try:
                os.rmdir(new_path)
            except OSError as exc:
                print(f'os_rename error unlinking target {exc}')
                return False
        else:
            try:
                os.unlink(new_path)
            except OSError as exc:
                print(f'os_rename error unlinking target {exc}')
                return False
    try:
        os.rename(old_path, new_path)
    except OSError as exc:
        print(f'os_rename error renaming {exc}')
        return False
    return True


def os_move(fpath: str, dest_dir: str) -> bool:
    """
    Move the file 'fpath' into 'dest_dir'
    """
    if not fpath or not dest_dir or not os.path.exists(fpath):
        print(f'Error cannot move file {fpath} into {dest_dir}')
        return False

    if not make_dir_path(dest_dir):
        print(f'Error creating {dest_dir}')
        return False

    filename = os.path.basename(fpath)
    dest_path = os.path.join(dest_dir, filename)

    if not os_rename(fpath, dest_path):
        print(f'Error moving {fpath} into {dest_dir}')
        return False
    return True


def make_dir_path(path_dir: str, dirmode: int = -1) -> bool:
    """
    makes directory and any missing path components
      - set reasonable permissions
    """
    if dirmode < 0:
        dirmode = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP
    try:
        os.makedirs(path_dir, exist_ok=True)
        if dirmode > 0:
            os.chmod(path_dir, dirmode)
    except OSError:
        return False
    return True
