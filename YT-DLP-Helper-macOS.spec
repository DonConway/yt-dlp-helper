
# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

# macOS application dependencies
bin_dir = Path('bin')

required_binaries = [
    'yt-dlp',
    'ffmpeg',
    'ffprobe',
    'deno',
]

# Ensure all dependencies exist before building
for binary in required_binaries:
    if not (bin_dir / binary).is_file():
        raise FileNotFoundError(
            f'Missing macOS dependency: {bin_dir / binary}'
        )

a = Analysis(
    ['main_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        (str(bin_dir / binary), 'bin')
        for binary in required_binaries
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='YT-DLP Helper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='YT-DLP Helper',
)

app = BUNDLE(
    coll,
    name='YT-DLP Helper.app',
    bundle_identifier='com.ytdlphelper.app',
    info_plist={
        'NSHighResolutionCapable': True,
    },
)
