# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\Users\\Alexandre\\Desktop'],
             binaries=[],
             datas=[(r'C:\Users\alexa\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\folium\templates','folium_templates'),
             (r'C:\Users\alexa\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\branca','branca'),
             ('background.jpg','.'),
             ('logo-pharmacie-médical.ico','.'),
             ("Notice d'utilisation.pdf",'.')],
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
          name='Medical_Data_Analyser',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
