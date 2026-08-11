# -*- mode: python ; coding: utf-8 -*-
#
# Build with:  pyinstaller run.spec
# Output exe:  dist/LocalShare.exe  (or dist/LocalShare on Linux/macOS)
#
# IMPORTANT — run this BEFORE building, from the project root
# (same folder as manage.py), so static files are collected:
#
#   python manage.py collectstatic --noinput
#
# Folder layout this spec assumes (adjust the two "datas" lines below
# if yours is different):
#   project_root/
#     run.py
#     run.spec
#     manage.py
#     file_manager/            (settings.py, urls.py, wsgi.py)
#     file/                    (views.py, forms.py, models.py, migrations/)
#       templates/file/*.html
#     templates/base.html
#     static/                  (created by collectstatic)

import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hidden_imports = (
    collect_submodules('django')
    + collect_submodules('file')
    + [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
)

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),   # project-level templates (base.html)
        ('file', 'file'),  # app-level templates
        ('static', 'static'),         # output of collectstatic
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LocalShare',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # set True temporarily if you need to see errors
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
