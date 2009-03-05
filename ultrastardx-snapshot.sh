#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
svn=$(date +%Y%m%d)

cd "$tmp"

svn checkout -r {$svn} https://ultrastardx.svn.sourceforge.net/svnroot/ultrastardx/trunk ultrastardx-$svn

cd ultrastardx-$svn
find . -type d -name .svn -print0 | xargs -0r rm -rf
# remove installer stuff as it's not needed for linux
rm -rf installer*
# remove precompiled stuff
find . -name *.res -exec rm -rf {} \;
# remove fonts, fedora has it's own
find game/fonts/ -name *.ttf -exec rm -rf {} \;
cd ..

tar --lzma -cf "$pwd"/ultrastardx-$svn.tar.lzma ultrastardx-$svn

cd - >/dev/null
