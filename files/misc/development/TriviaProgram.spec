# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

a = Analysis(['TriviaProgram.py'],
             pathex=['C:\\Users\\Kian\\Desktop'],
             binaries=[],
             datas=[],
             hiddenimports=['pandas._libs.tslibs.timedeltas','pandas._libs.tslibs.nattype','pandas._libs.tslibs.np_datetime','pandas._libs.skiplist'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt5'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='TriviaProgram',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False)
