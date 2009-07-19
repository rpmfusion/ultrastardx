%define prever 20090719

Name:           ultrastardx
Version:        1.1.1
Release:        1%{?prever:.8.%{prever}}%{?dist}
Summary:        Karaoke game inspired by a popular commercial karaoke game

Group:          Amusements/Games
License:        GPLv2+
URL:            http://www.ultrastardeluxe.org
# Source0: svn snapshot; use supplied ultrastardx-snapshot.sh to get one
Source0:        ultrastardx%{?prever:-%{prever}}.tar.lzma
Source1:        ultrastardx-32x32.png
Source2:        ultrastardx-256x256.png
Source100:      ultrastardx-snapshot.sh
Patch0:         ultrastardx-desktop.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       bitstream-vera-sans-fonts gnu-free-sans-fonts

BuildRequires:  fpc desktop-file-utils 
BuildRequires:  ffmpeg-devel freetype-devel libpng-devel libprojectM-devel 
BuildRequires:  portaudio-devel SDL-devel SDL_image-devel sqlite-devel


%description
Karaoke game inspired by a popular commercial karaoke game. It allows up to six
players to sing along with music using microphones in order to score points,
depending on the pitch of the voice and the rhythm of singing.


%prep
%setup -q -n %{name}%{?prever:-%{prever}}
%patch0 -p1

# replace the font paths with Fedora's own
sed -i 's|File=|File=%{_datadir}/fonts/|g' game/fonts/fontsTTF.ini
sed -i 's|FreeSans|freefont/FreeSans|g' game/fonts/fontsTTF.ini
sed -i 's|Vera|bitstream-vera/Vera|g' game/fonts/fontsTTF.ini

iconv -f iso-8859-1 -t utf-8 ChangeLog.GERMAN.txt > ChangeLog.GERMAN.txt.utf-8
touch -r ChangeLog.GERMAN.txt ChangeLog.GERMAN.txt.utf-8
mv ChangeLog.GERMAN.txt.utf-8 ChangeLog.GERMAN.txt

tr -d \\r < COPYRIGHT.txt > COPYRIGHT.txt.unix
touch -r COPYRIGHT.txt COPYRIGHT.txt.unix
mv COPYRIGHT.txt.unix COPYRIGHT.txt

%build
%configure --with-libprojectM=nocheck libprojectM_VERSION=$(pkg-config --modversion libprojectM) libprojectM_INCLUDEDIR="/usr/include" libprojectM_DATADIR="/usr/share/projectM"
make %{?_smp_mflags} PFLAGS_EXTRA="-fPIC"


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
desktop-file-install --mode=644 \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications dists/%{name}.desktop
install -Dpm 644 %{SOURCE1} \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -Dpm 644 %{SOURCE2} \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS.txt ChangeLog.GERMAN.txt ChangeLog.txt COPYING.txt COPYRIGHT.txt
%doc README.txt
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*


%changelog
* Sun Jul 19 2009 Felix Kaechele <heffer@fedoraproject.org> - 1.1.1-1.8.20090719
- new snapshot
- party mode works again, tested it today :)

* Sat Apr 11 2009 Felix Kaechele <felix at fetzig dot org> - 1.1.1-1.7.20090411
- new snapshot
- fixed typos

* Wed Apr 01 2009 Felix Kaechele <felix at fetzig dot org> - 1.1.1-1.6.20090331
- new snapshot and reworked ffmpeg headers

* Tue Mar 31 2009 Felix Kaechele <felix at fetzig dot org> - 1.1.1-1.5.20090303
- fixed font deps

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.1.1-1.4.20090303
- rebuild for new F11 features

* Tue Mar 10 2009 Felix Kaechele <felix at fetzig dot org> - 1.1.1-0.4.20090303
- change package name for bitstream vera

* Tue Mar 03 2009 Felix Kaechele <felix at fetzig dot org> - 1.1.1-0.3.20090303
- new snapshot; now builds in rawhide

* Mon Feb 09 2009 Felix Kaechele <felix at fetzig dot org> - 1.1.1-0.2.20090209
- updated to new svn revision; this fixes ffmpeg

* Tue Jan 20 2009 Felix Kaechele <felix at fetzig dot org> - 1.1.1-0.1.20090120
- fixed tarball and loosened some hardcoded stuff

* Sun Jan 18 2009 Felix Kaechele <felix at fetzig dot org> - 1.1.1-0.1.20090118
- incorporated suggestions from https://bugzilla.rpmfusion.org/show_bug.cgi?id=308#c2

* Wed Dec 31 2008 Felix Kaechele <felix at fetzig dot org> - 1.1.1-0.1.20081231
- initial build
