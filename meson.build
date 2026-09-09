#
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
#

project('kea_config', ['c'],
  version: files('src/version.txt'),
  meson_version: '>=1.10.0',
  default_options: [
    'c_std=c23',
    'warning_level=3',
    'b_pie=true',
    'prefix=/usr',
    'mandir=share/man',
    ],
)

d_etc = get_option('sysconfdir')
d_lib = get_option('libdir')
d_bin = get_option('bindir')
d_man = get_option('mandir')
d_share = get_option('datadir')

py_mod = import('python')
py = py_mod.find_installation(pure: false)
proj_root = meson.project_source_root()
py_dep = py.dependency(embed: true)

inc_dir = []
lib_sources = []

#
# top-level files
#

#
# Python submodules
#
subdir('src/kea_config_mod')

#
# Deps
#

#
# Executables
#
configure_file(
  input: 'src/kea_config_mod/apps/kea-config.py',
  output: 'kea-config',
  copy: true,
  install_dir: d_bin,
  install_mode: 'rwxr-xr-x'
)

#
# Install
#

s_license = 'src/data/license'
s_changelog = 'src/data/changelog'
s_docs = 'src/data/docs'
s_examples = 'src/data/examples'
s_scripts = 'src/scripts'
manual = 'kea-config.pdf'

# 
# /usr/share/kea_config/docs
# 
install_data(
  [
    s_docs / manual,
  ],
  install_dir: d_share / 'kea_config/docs'
)

install_subdir(
  [
    s_docs / 'html',
  ],
  install_dir: d_share / 'kea_config/docs',
  strip_directory: false
)

# 
# /usr/share/kea_config 
# 
install_data(
  [
    'README.rst',
    s_changelog / 'Changelog.rst',
    'packaging/Changelog',
  ],
  install_dir: d_share / 'kea_config'
)
install_data(
  [
    s_examples / 'dhcp4-example-1.yaml',
    s_examples / 'dhcp4-example-2.yaml',
    s_examples / 'note.txt',
    ],
  install_dir: d_share / 'kea_config/examples',
)

# 
# /usr/share/licenses/kea_config 
# 
install_data(
  [
    s_license / 'License-gpl-2.0.txt',
    s_license / 'License.rst',
  ],
  install_dir: d_share / 'licenses/kea_config'
)

#
# tests
#
srcdir = proj_root / 'src'
testdir = srcdir / 'tests'
test_exe = find_program(testdir / 'run-one-test')

foreach i : range(1, 3)
  test('test-@0@'.format(i), 
    test_exe, 
    args: ['@0@'.format(i)], 
    env: {'PYTHONPATH': srcdir},
    workdir: testdir,
    )
endforeach    
