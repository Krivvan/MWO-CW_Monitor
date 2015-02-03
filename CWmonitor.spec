# -*- mode: python -*-

block_cipher = None


a = Analysis(['CWmonitor.pyw'],
             pathex=['H:\\HobbyWork\\MWO-CW_Monitor'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='CWmonitor.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='CWmonitor.ico')
