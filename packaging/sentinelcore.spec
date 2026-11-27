# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules
root=Path(SPECPATH).parent.parent
src=root/'src'
a=Analysis([str(root/'main.py')], pathex=[str(src)], binaries=[], datas=[(str(src/'sentinel/ui/styles/theme.qss'),'sentinel/ui/styles')], hiddenimports=collect_submodules('sentinel'), hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=['tkinter'], noarchive=False)
pyz=PYZ(a.pure)
exe=EXE(pyz,a.scripts,a.binaries,a.datas,[],name='Sentinel',debug=False,bootloader_ignore_signals=False,strip=False,upx=True,console=False,disable_windowed_traceback=False,argv_emulation=False,target_arch=None,codesign_identity=None,entitlements_file=None)
