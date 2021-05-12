#!/bin/bash
set -ev

BUILD_REPO_URL=https://github.com/ciphscoin/electrum-siphscoin

#git clone --branch dev $BUILD_REPO_URL electrum-ciphscoin

cp libusb-1.0.dylib electrum-ciphscoin/contrib

cd electrum-ciphscoin

export PY36BINDIR=/Library/Frameworks/Python.framework/Versions/3.6/bin/
export PATH=$PATH:$PY36BINDIR
source ./contrib/zcash/travis/electrum_zcash_version_env.sh;
echo wine build version is $ELECTRUM_ZCASH_VERSION

sudo pip3 install --upgrade pip
sudo pip3 install -r contrib/deterministic-build/requirements.txt
sudo pip3 install -r contrib/deterministic-build/requirements-hw.txt

pyrcc5 icons.qrc -o gui/qt/icons_rc.py

export PATH="/usr/local/opt/gettext/bin:$PATH"
./contrib/make_locale
find . -name '*.po' -delete
find . -name '*.pot' -delete

pyinstaller \
    -y \
    --name electrum-zcash-$ELECTRUM_ZCASH_VERSION.bin \
    contrib/build-osx/osx.spec

sudo hdiutil create -fs HFS+ -volname "Electrum-Ciphscoin" \
    -srcfolder dist/Electrum-Ciphscoin.app \
    dist/electrum-ciphscoin-$ELECTRUM_ZCASH_VERSION-macosx.dmg
