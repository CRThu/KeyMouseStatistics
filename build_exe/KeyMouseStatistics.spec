# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\entrance.py'],
             pathex=['..\\DataStorage.py', '..\\GetAdmin.py', '..\\KeyboardHookListenerClass.py', '..\\MouseHookListenerClass.py', '..\\SQLite_oper.py', '..\\stdout_to_log.py', '..\\tkinter_gui.py', 'C:\\Users\\YummyCarrot\\Documents\\IdeaProjects\\PyCharm\\Key&MouseStatistics\\build_exe'],
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
          name='KeyMouseStatistics',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , uac_admin=True)
