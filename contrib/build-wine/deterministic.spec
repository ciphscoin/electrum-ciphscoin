# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

import sys
for i, x in enumerate(sys.argv):
    if x == '--name':
        cmdline_name = sys.argv[i+1]
        break
else:
    raise BaseException('no name')


home = 'C:\\electrum\\'

# see https://github.com/pyinstaller/pyinstaller/issues/2005
hiddenimports = []
hiddenimports += collect_submodules('trezorlib')
hiddenimports += collect_submodules('btchip')
hiddenimports += collect_submodules('keepkeylib')
hiddenimports += collect_submodules('websocket')
hiddenimports += [
    'lib',
    'lib.base_wizard',
    'lib.plot',
    'lib.qrscanner',
    'lib.websockets',
    'gui.qt',

    'plugins',

    'plugins.hw_wallet.qt',

    'plugins.audio_modem.qt',
    'plugins.cosigner_pool.qt',
    'plugins.digitalbitbox.qt',
    'plugins.email_requests.qt',
    'plugins.keepkey.qt',
    'plugins.labels.qt',
    'plugins.trezor.qt',
    'plugins.ledger.qt',
    'plugins.virtualkeyboard.qt',
]

# Add libusb binary
binaries = [("c:/python3.5.4/libusb-1.0.dll", ".")]

# Workaround for "Retro Look":
binaries += [b for b in collect_dynamic_libs('PyQt5') if 'qwindowsvista' in b[0]]

datas = [
    (home+'lib/checkpoints.json', 'electrum_zcash'),
    (home+'lib/servers.json', 'electrum_zcash'),
    (home+'lib/servers_testnet.json', 'electrum_zcash'),
    (home+'lib/servers_regtest.json', 'electrum_zcash'),
    (home+'lib/currencies.json', 'electrum_zcash'),
    (home+'lib/locale', 'electrum_zcash/locale'),
    (home+'lib/wordlist', 'electrum_zcash/wordlist'),
    ('C:\\Program Files (x86)\\ZBar\\bin\\', '.')
]
datas += collect_data_files('trezorlib')
datas += collect_data_files('btchip')
datas += collect_data_files('keepkeylib')

# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-remove-tkinter-tcl
sys.modules['FixTk'] = None
excludes = ['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter']
excludes += [
    'PyQt5.QtCLucene',
    'PyQt5.Qt5CLucene',
    'PyQt5.QtDesigner',
    'PyQt5.QtDesignerComponents',
    'PyQt5.QtHelp',
    'PyQt5.QtLocation',
    'PyQt5.QtMultimedia',
    'PyQt5.QtMultimediaQuick_p',
    'PyQt5.QtMultimediaWidgets',
    'PyQt5.QtNetwork',
    'PyQt5.QtOpenGL',
    'PyQt5.QtPositioning',
    'PyQt5.QtPrintSupport',
    'PyQt5.QtQml',
    'PyQt5.QtQuick',
    'PyQt5.QtQuickParticles',
    'PyQt5.QtQuickWidgets',
    'PyQt5.QtSensors',
    'PyQt5.QtSerialPort',
    'PyQt5.QtSql',
    'PyQt5.Qt5Sql',
    'PyQt5.QtTest',
    'PyQt5.QtWebChannel',
    'PyQt5.QtWebKit',
    'PyQt5.QtWebKitWidgets',
    'PyQt5.QtWebSockets',
    'PyQt5.QtXml',
    'PyQt5.QtXmlPatterns',
    'PyQt5.QtWebProcess',
    'PyQt5.QtWinExtras',
]

a = Analysis([home+'electrum-zcash'],
             pathex=[home+'plugins'],
             hiddenimports=hiddenimports,
             datas=datas,
             binaries=binaries,
             excludes=excludes,
             runtime_hooks=['pyi_runtimehook.py'])

# http://stackoverflow.com/questions/19055089/
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

# Add TOC to electrum_zcash, electrum_zcash_gui, electrum_zcash_plugins
for p in sorted(a.pure):
    if p[0].startswith('lib') and p[2] == 'PYMODULE':
        a.pure += [('electrum_zcash%s' % p[0][3:] , p[1], p[2])]
    if p[0].startswith('gui') and p[2] == 'PYMODULE':
        a.pure += [('electrum_zcash_gui%s' % p[0][3:] , p[1], p[2])]
    if p[0].startswith('plugins') and p[2] == 'PYMODULE':
        a.pure += [('electrum_zcash_plugins%s' % p[0][7:] , p[1], p[2])]

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon=home+'icons/electrum-ciphscoin.ico',
          name=os.path.join('build\\pyi.win32\\electrum', cmdline_name))

# exe with console output
conexe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          debug=False,
          strip=False,
          upx=False,
          console=True,
          icon=home+'icons/electrum-ciphscoin.ico',
          name=os.path.join('build\\pyi.win32\\electrum',
                            'console-%s' % cmdline_name))

# trezorctl separate executable
tctl_a = Analysis(['c:/python3.5.4/Scripts/trezorctl'],
                  hiddenimports=['pkgutil'],
                  excludes=excludes,
                  runtime_hooks=['pyi_tctl_runtimehook.py'])

tctl_pyz = PYZ(tctl_a.pure)

tctl_exe = EXE(tctl_pyz,
           tctl_a.scripts,
           exclude_binaries=True,
           debug=False,
           strip=False,
           upx=False,
           console=True,
           name=os.path.join('build\\pyi.win32\\electrum', 'trezorctl.exe'))

coll = COLLECT(exe, conexe, tctl_exe,
               a.binaries,
               a.datas,
               strip=False,
               upx=False,
               name=os.path.join('dist', 'electrum'))
