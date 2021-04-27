# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/brendanlee/Desktop/cmm_testint_run_mac'],
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
a.datas += [('cms_logo.png', '/Users/brendanlee/Desktop/cmm_testint_run_mac/cms_logo.png', 'DATA'),
            ('purdue_logo.png', '/Users/brendanlee/Desktop/cmm_testint_run_mac/purdue_logo.png', 'DATA'),
            ('cmsc_logo.png', '/Users/brendanlee/Desktop/cmm_testint_run_mac/cmsc_logo.png', 'DATA'),
            ('fermi_logo.png','/Users/brendanlee/Desktop/cmm_testint_run_mac/fermi_logo.png', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
