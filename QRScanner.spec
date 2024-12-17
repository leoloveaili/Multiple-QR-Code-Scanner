# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('app.py', '.'),
    ],
    hiddenimports=[
        'flask',
        'jinja2.ext',
        'jinja2.utils',
        'jinja2.runtime',
        'jinja2.loaders',
        'jinja2.filters',
        'jinja2.tests',
        'jinja2.parser',
        'jinja2.nodes',
        'jinja2.optimizer',
        'jinja2.compiler',
        'jinja2.lexer',
        'jinja2.environment',
        'jinja2.bccache',
        'jinja2.defaults',
        'jinja2.visitor',
        'werkzeug.routing',
        'werkzeug.debug',
        'werkzeug.middleware',
        'cv2',
        'numpy',
    ],
    hookspath=[],
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
    name='QRScanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 