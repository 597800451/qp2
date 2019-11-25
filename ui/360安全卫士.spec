# -*- mode: python -*-

block_cipher = None


a = Analysis(['360\xb0\xb2\xc8\xab\xce\xc0\xca\xbf.py'],
             pathex=['C:\\Users\\59780\\Documents\\project\\qp2\\ui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='360°²È«ÎÀÊ¿',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='360.ico')
