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


cd "$tmp"
svnpath=https://ultrastardx.svn.sourceforge.net/svnroot/ultrastardx/trunk
svn=`svn info $svnpath | grep Revision | awk '{print $2}'`

svn export $svnpath  ultrastardx-r$svn

cd ultrastardx-r$svn
# remove installer stuff as it's not needed for linux
rm -rf installer*
# remove precompiled stuff
find . -name *.res -exec rm -rf {} \;
# remove fonts, fedora has it's own
rm -rf game/fonts/DejaVu game/fonts/FreeSans
cd ..

tar --xz -cf "$pwd"/ultrastardx-r$svn.tar.xz ultrastardx-r$svn

cd - >/dev/null
