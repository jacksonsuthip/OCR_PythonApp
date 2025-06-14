# app.spec

from PyInstaller.utils.hooks import collect_submodules
import os

block_cipher = None
base_path = os.path.abspath(".")

a = Analysis(
    ['app.py'],  # 👈 Your main script file
    pathex=[base_path],
    binaries=[],
    datas=[
        ('poppler/Library/bin', 'poppler/Library/bin'),  # ✅ include poppler binaries
        ('.EasyOCR', '.EasyOCR'),                       # ✅ include downloaded OCR models
    ],
    hiddenimports=collect_submodules('easyocr'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',  # 👈 this is your output EXE name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False  # set True if you want to see terminal logs
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app'
)
