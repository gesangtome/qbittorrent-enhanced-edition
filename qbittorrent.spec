%global giturl  https://github.com/qbittorrent/qBittorrent

Name:    qbittorrent
Summary: A Bittorrent Client
Epoch:   1
Version: 4.3.3
Release: 1%{?dist}
License: GPLv2+
URL:     http://www.qbittorrent.org
Source0: %{giturl}/archive/release-%{version}/%{name}-%{version}.tar.gz
Source1: qbittorrent-nox.README
Source2: qbittorrent-nox
# These flags are needed for the hardening feature. It's probably not interesting for upstream
Patch0:  qbittorrent-3.3.11-build_flags.patch
# disable silent qmake config, enable verbose build
Patch1:  qbittorrent-3.3.1-verbose_build.patch


BuildRequires: cmake3
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: systemd
BuildRequires: pkgconfig(Qt5Core) >= 5.5
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(zlib)
BuildRequires: qt5-linguist
BuildRequires: rb_libtorrent-devel >= 1.1.4
BuildRequires: desktop-file-utils
BuildRequires: boost-devel >= 1.60
BuildRequires: libappstream-glib

Requires: python3

%description
A Bittorrent client using rb_libtorrent and a Qt4 Graphical User Interface.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%package nox
Summary: A Headless Bittorrent Client

%description nox
A Headless Bittorrent client using rb_libtorrent.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%prep
%setup -q -n qBittorrent-release-%{version} -c

mv qBittorrent-release-%{version} build

pushd build
%patch0 -p1
%patch1 -p1 -b .verbose_build
sed -i -e 's@Exec=qbittorrent %U@Exec=env TMPDIR=/var/tmp qbittorrent %U@g' dist/unix/org.qbittorrent.qBittorrent.desktop
cp README.md NEWS AUTHORS TODO Changelog COPYING ..
popd

cp -p %{SOURCE1} .
cp -Rp build build-nox

%build
export LDFLAGS="%{?__global_ldflags} -pthread"
# Build headless first
pushd build-nox
%cmake3 -DSYSTEMD=ON -Wno-dev -GNinja -DGUI=OFF
%cmake3_build
popd

# Build gui version
pushd build
%cmake3 -Wno-dev -GNinja
%cmake3_build
popd

%install
# install headless version
pushd build-nox
%cmake3_install
popd

# install gui version
pushd build
%cmake3_install
popd

mv %{buildroot}%{_bindir}/qbittorrent-nox %{buildroot}%{_bindir}/qbittorrent-nox-bin
install -pm 0755 %{SOURCE2} %{buildroot}%{_bindir}/qbittorrent-nox


desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications/ \
  %{buildroot}%{_datadir}/applications/org.qbittorrent.qBittorrent.desktop

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.qbittorrent.qBittorrent.appdata.xml

%files
%license COPYING
%doc README.md NEWS AUTHORS TODO Changelog
%{_bindir}/qbittorrent
%{_metainfodir}/org.qbittorrent.qBittorrent.appdata.xml
%{_datadir}/applications/org.qbittorrent.qBittorrent.desktop
%{_datadir}/icons/hicolor/*/apps/qbittorrent.png
%{_datadir}/icons/hicolor/*/status/qbittorrent-tray.png
%{_datadir}/icons/hicolor/*/status/qbittorrent-tray*.svg
%{_mandir}/man1/qbittorrent.1*

%files nox
%license COPYING
%doc qbittorrent-nox.README NEWS AUTHORS TODO Changelog
%{_bindir}/qbittorrent-nox
%{_bindir}/qbittorrent-nox-bin
%{_unitdir}/qbittorrent-nox@.service
%{_mandir}/man1/qbittorrent-nox.1*

%changelog
* Tue Jan 19 2021 Leigh Scott <leigh123linux@gmail.com> - 1:4.3.3-1
- Update to 4.3.3

* Mon Dec 28 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.3.2-1
- Update to 4.3.2

* Thu Nov 26 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.3.1-1
- Update to 4.3.1

* Mon Oct 26 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.3.0-2
- Revert 'Disable webui for gui build' (rhbz#1891273)

* Mon Oct 19 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.3.0-1
- Update to 4.3.0

* Fri Oct  9 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.2.5-5
- Switch to cmake
- Disable webui for gui build

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.2.5-3
- Revert 'Remove html code from tooltip'

* Sat Jun 20 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.2.5-2
- Remove html code from tooltip
- Simplify the build process

* Sat May 09 2020 Fabio Alessandro Locati <me@fale.io> - 1:4.2.5-1
- Update to 4.2.5

* Wed Apr 15 2020 Charalampos Stratakis <cstratak@redhat.com> - 1:4.2.3-1
- Update to 4.2.3

* Wed Mar 25 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.2.2-1
- Update to 4.2.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:4.2.1-1
- Update to 4.2.1

* Wed Dec 04 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:4.2.0-2
- Remove unused build requires and configure options

* Wed Dec 04 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:4.2.0-1
- Update to 4.2.0

* Mon Oct 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:4.2.0-0.1.20191027.git9c466d8
- Update to 4.2.0 beta1 git snapshot
- Rebuild for libtorrent SONAME bump

* Wed Oct 16 2019 Leigh Scott <leigh123linux@gmail.com> - 1:4.1.8-1
- Update to 4.1.8

* Mon Aug 05 2019 Leigh Scott <leigh123linux@gmail.com> - 1:4.1.7-1
- Update to 4.1.7
- Drop unused patch

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Leigh Scott <leigh123linux@gmail.com> - 1:4.1.6-1
- Update to 4.1.6

* Thu Jan 31 2019 Kalev Lember <klember@redhat.com> - 1:4.1.5-2
- Rebuilt for Boost 1.69

* Tue Jan 08 2019 Charalampos Stratakis <cstratak@redhat.com> - 1:4.1.5-1
- Update to 4.1.5

* Mon Oct 01 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:4.1.3-1
- Update to 4.1.3

* Thu Aug 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:4.1.2-1
- Update to 4.1.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:4.1.1-1
- Update to 4.1.1

* Sat May 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:4.1.0-1
- Update to 4.1.0

* Thu Feb 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:4.0.4-1
- Update to 4.0.4

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:4.0.3-2
- Rebuild for boost-1.66
- Remove scriptlets

* Thu Dec 28 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:4.0.3-1
- Update to 4.0.3

* Fri Nov 24 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:4.0.1-1
- Update to 4.0.1

* Mon Sep 18 2017 Charalampos Stratakis <cstratak@redhat.com> - 1:3.3.16-1
- Update to 3.3.16

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 1:3.3.13-3
- Rebuilt for Boost 1.64

* Mon Jul 17 2017 Charalampos Stratakis <cstratak@redhat.com> - 1:3.3.13-2
- Use python3 for runtime
Resolves: rhbz#1471349

* Thu Jul 13 2017 Tom Callaway <spot@fedoraproject.org> - 1:3.3.13-1
- update to 3.3.13

* Thu Mar 16 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.11-1
- Rebuild

* Mon Mar 06 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.11-1
- Update to 3.3.11
- Fix CVE-2017-6503
- Fix CVE-2017-6504
- Rebase patch qbittorrent-3.3.1-build_flags.patch
- Rebase patch qbittorrent-3.3.1-gcc6_hack.patch
- Package tray icons as well

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.10-1
- Update to 3.3.10

* Wed Sep 28 2016 Leigh Scott <leigh123linux@googlemail.com> - 1:3.3.7-2
- Rebuild for new rb_libtorrent .so version 

* Mon Sep 19 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.7-1
- Update to 3.3.7

* Mon Jun 27 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.5-1
- Upgrade to 3.3.5
- Fix patch remove_donate since it was not applying properly
- Fix patch for CXX code since it was not applying properly

* Mon Apr 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.4-1
- Bump to 3.3.4
- Fix patch remove_donate since it was not applying properly

* Fri Mar 18 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-11
- Rebuild for rb_libtorrent 1.0.9-2

* Thu Mar 17 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-10
- Bodhi did not noticed the builds

* Wed Mar 16 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-9
- build rewrite was not yet ready :(

* Wed Mar 16 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-8
- rebuild to fix bug #1294336

* Sun Mar 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:3.3.3-7
- qbittorrent: FTBFS in rawhide (#1307961) 
- disable silent build rules
- use qmake-qt5 wrapper to ensure proper build flags

* Sat Mar 12 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-6
- Rebuild for rb_libtorrent 1.0.9

* Tue Feb 23 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-5
- Rebuilt for qtsingleapplication 2.6.1-28

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-3
- Rebuilt for rb_libtorrent 1.0.8

* Sat Jan 23 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-2
- Rebuilt for Boost 1.60

* Thu Jan 21 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.3-1
- New upstream release

* Wed Jan 20 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.2-1
- New upstream release

* Mon Jan 18 2016 Jonathan Wakely <jwakely@redhat.com> - 1:3.3.1-3
- Rebuilt for Boost 1.60

* Tue Dec 08 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.1-2
- A little bit of cleanup

* Tue Dec 08 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.3.1-1
- New upstream version
- Move from Qt4 to Qt5
- Complete recreation of dependencies and patches

* Mon Dec 07 2015 Rafael Fonseca <rdossant@redhat.com> - 1:3.2.4-3
- Add suport to ppc64le
- Solves #1255788, #1252961

* Sun Oct 25 2015 Fabio Alessandro Locati - 1:3.2.4-2
- Fix patch for removing the donate button

* Sun Oct 25 2015 Fabio Alessandro Locati - 1:3.2.4-1
- New upstream

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1:3.2.3-3
- Rebuilt for Boost 1.59

* Sat Aug 15 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.2.3-1
- New upstream

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Sun Jul 26 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:3.2.1-1
- New upstream
- Less lint warning (7->2)

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1:3.2.0-3
- rebuild for Boost 1.58

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-1
- update to 3.2.0 release

* Sun May 03 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.16.git6e4fbcf
- update to the latest git (RC1)

* Sun Apr 26 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.15.git866f965
- fix systemd file

* Sat Apr 25 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.14.git866f965
- include systemd file for nox

* Sat Apr 25 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.13.git866f965
- update to the latest git (pre beta)

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1:3.2.0-0.12.git060d3fc
- Rebuild for boost 1.57.0

* Tue Dec 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.11.git060d3fc
- fix ARM build

* Tue Nov 25 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.10.git060d3fc
- update to the latest git
- armv7hl build disabled till upstream fixes it

* Mon Oct 27 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.9.gitb0f767e
- update to the latest git

* Tue Sep 16 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.8.git94043e6
- update to the latest git

* Mon Sep 08 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.7.git2b061da
- remove donate from help tab

* Fri Aug 22 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.6.git2b061da
- update to the latest git

* Mon Aug 18 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.5.gitd58d87a
- Rebuild against new rb_libtorrent

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.0-0.4.gitd58d87a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 22 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.3.gitd58d87a
- fix bz 1072046

* Sun Jun 08 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.2.gitd58d87a
- remove bundled qjson
- patch to use system qjson
- add build requires qjson-devel

* Sun Jun 08 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-0.1.gitd58d87a
- update to 3.2.0alpha git

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 1:3.1.9-3
- rebuild for boost 1.55.0

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:3.1.9-2
- Rebuild against fixed qt to fix -debuginfo (#1074041)

* Sun Mar 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.9-1
- update to 3.1.9 release

* Sat Jan 18 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.5-3
- add upstream commit to fix file preview

* Fri Jan 17 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.5-2
- fix file preview

* Fri Jan 17 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.5-1
- update to 3.1.5 release

* Mon Jan 13 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.4-5
- add wrapping script to fix (bz 998265)

* Fri Jan 10 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.4-4
- drop the _hardened_build global as it's crap

* Fri Jan 10 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.4-3
- fix build flags so hardened build works

* Fri Jan 10 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.4-2
- hardened build

* Sun Jan 05 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.4-1
- update to 3.1.4 release

* Sat Dec 07 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.3-1
- update to 3.1.3 release

* Sun Oct 13 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:3.1.0-1
- update to 3.1.0 release

* Thu Oct 03 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.11-3
- rebuilt

* Thu Oct 03 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.11-2
- bump

* Thu Aug 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.11-1
- update to 3.0.11 release

* Sun Jul 28 2013 Petr Machata <pmachata@redhat.com> - 1:3.0.10-2
- Rebuild for boost 1.54.0

* Wed Jul 10 2013 leigh scott <leigh123linux@googlemail.com> - 1:3.0.10-1
- update to 3.0.10 release

* Tue Mar 19 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.9-1
- update to 3.0.9 release

* Sun Feb 24 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1:3.0.8-5
- Rebuild for rb_libtorrent soname bump

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:3.0.8-4
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:3.0.8-3
- Rebuild for Boost-1.53.0

* Wed Jan 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.8-2
- Rebuild against new rb_libtorrent .so version

* Tue Jan 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.8-1
- update to 3.0.8 release

* Tue Oct 09 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.6-1
- update to 3.0.6 release

* Mon Oct 01 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.5-1
- update to 3.0.5 release

* Tue Sep 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.4-1
- update to 3.0.4 release

* Tue Aug 21 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.1-1
- update to 3.0.1 release
- change source to .xz

* Thu Aug 09 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.0-1
- update to 3.0.0 release

* Thu Jul 26 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.0-0.10.rc5
- Rebuild for boost-1.50.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.0-0.9.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.0-0.8.rc5
- update to 3.0.0rc5

* Sun Jul 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.0-0.7.rc4
- update to 3.0.0rc4

* Wed Jul 04 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.0-0.6.rc3
- update to 3.0.0rc3

* Mon Jul 02 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.0-0.5.rc2
- update to 3.0.0rc2

* Sun Jul 01 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.0-0.4.rc1
- update to 3.0.0rc1

* Sun Jun 24 2012 leigh scott <leigh123linux@googlemail.com> - 1:3.0.0-0.3.beta4
- rebuilt for rb_libtorrent-0.16.1

* Sun Jun 24 2012 leigh scott <leigh123linux@googlemail.com> - 1:3.0.0-0.2.beta4
- update to 3.0.0beta4

* Sun May 20 2012 leigh scott <leigh123linux@googlemail.com> - 1:3.0.0-0.1.beta2
- update to 3.0.0beta2

* Mon May 07 2012 leigh scott <leigh123linux@googlemail.com> - 1:2.9.8-1
- update to 2.9.8

* Mon Mar 19 2012 leigh scott <leigh123linux@googlemail.com> - 1:2.9.7-1
- update to 2.9.7

* Sun Feb 19 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.5-1
- update to 2.9.5

* Sun Feb 19 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.4-1
- update to 2.9.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.3-1
- update to 2.9.3

* Tue Nov 22 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.2-1
- update to 2.9.2

* Sun Oct 23 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.1-1
- update to 2.9.1

* Sat Oct 08 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.0-1
- update to 2.9.0

* Sun Oct 02 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.0-0.5.rc3
- update to 2.9.0rc3

* Wed Sep 28 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.0-0.4.rc2
- update to 2.9.0rc2

* Sun Sep 25 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.0-0.3.rc1
- update to 2.9.0rc1

* Thu Sep 22 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.0-0.2.beta2
- update to 2.9.0beta2

* Sun Sep 18 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.9.0-0.1.beta1
- update to 2.9.0beta1

* Sun Sep 18 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.5-1
- update to 2.8.5

* Fri Aug 12 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.4-2
- spec file cleanup

* Fri Aug 12 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.4-1
- update to 2.8.4

* Tue Aug 02 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.3-1
- update to 2.8.3

* Thu Jul 21 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.2-2
- rebuild against boost 1.47.0

* Sat Jun 18 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.2-1
- update to 2.8.2

* Sun Jun 05 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.1-1
- update to 2.8.1

* Thu Jun 02 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-1
- update to 2.8.0

* Fri May 27 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.8.rc3
- update to 2.8.0rc3

* Sun May 22 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.7.rc2
- update to 2.8.0rc2

* Sun May 22 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.6.rc1
- update to 2.8.0rc1

* Wed May 04 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.5.beta5
- update to 2.8.0beta5

* Mon Apr 18 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.4.beta4
- update to 2.8.0beta4

* Sat Apr 16 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.3.beta3
- update to 2.8.0beta3

* Mon Apr 11 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.2.beta2
- update to 2.8.0beta2

* Sat Apr 09 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.1.beta1
- update to 2.8.0beta1

* Thu Apr 07 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.2-1
- update to 2.7.2

* Wed Apr 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.1-1
- update to 2.7.1

* Sun Mar 20 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-1
- update to 2.7.0 release

* Wed Mar 16 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.6.rc1
- update to 2.7.0rc1

* Sun Mar 13 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.5.beta4
-  update to 2.7.0beta4

* Sat Mar 12 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.4.beta3
-  update to 2.7.0beta3

* Thu Mar 03 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.3.beta2
-  update to 2.7.0beta2

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1:2.7.0-0.2.beta1
- Rebuild against new rb_libtorrent

* Wed Feb 09 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.1.beta1
-  update to 2.7.0beta1

* Wed Feb 09 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.6-1
-  update to 2.6.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.5-2
- drop boost_filesystem v2 patch (bug 654807)

* Sat Feb 05 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.5-1
-  update to 2.6.5
-  rebuilt and patched for boost changes

* Thu Jan 27 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.4-2
- rebuilt

* Sun Jan 23 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.4-1
-  update to 2.6.4

* Sat Jan 15 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.3-1
-  update to 2.6.3

* Wed Jan 12 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.2-1
- update to 2.6.2

* Mon Jan 10 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.1-1
- update to 2.6.1

* Sun Jan 09 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.0-1
- update to 2.6.0 release

* Thu Jan 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.0-0.6.rc2
- update to 2.6.0rc2

* Thu Jan 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.0-0.5.rc1
- update to 2.6.0rc1

* Sat Jan 01 2011 leigh scott <leigh123linux@googlemail.com> - 1:2.6.0-0.4.beta4
- update to 2.6.0beta4

* Sun Dec 26 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.6.0-0.3.beta3
- update to 2.6.0beta3

* Sat Dec 25 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.6.0-0.2.beta2
- update to 2.6.0beta2

* Sun Dec 19 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.6.0-0.1.beta1
- update to 2.6.0beta1

* Sun Dec 05 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.1-1
- update to 2.5.1

* Sun Dec 05 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-1
- update to 2.5.0 release

* Mon Nov 29 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.12.rc4
- update to 2.5.0rc4

* Mon Nov 29 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.11.rc3
- update to 2.5.0rc3

* Thu Nov 25 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.10.rc2
- update to 2.5.0rc2

* Tue Nov 23 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.9.rc1
- update to 2.5.0rc1

* Sun Nov 21 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.8.beta7
- update to 2.5.0beta7

* Sun Nov 21 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.7.beta6
- replaced wrongly versioned source code

* Sun Nov 21 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.6.beta6
- update to 2.5.0beta6

* Sun Nov 21 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.5.beta5
- update to 2.5.0beta5

* Thu Nov 18 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.4.beta4
- update to 2.5.0beta4
- add temp build fix

* Sat Nov 13 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.3.beta3
- update to 2.5.0beta3

* Sat Nov 06 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.2.beta2
- rebuilt and patched for new libnotify version

* Mon Oct 25 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.1.beta2
- update to 2.5.0beta2

* Sun Oct 24 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.8-1
- update to 2.4.8

* Mon Oct 18 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.6-1
- update to 2.4.6

* Sat Oct 02 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.4-1
- update to 2.4.4

* Mon Sep 27 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.3-1
- update to 2.4.3

* Sun Sep 26 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.2-1
- update to 2.4.2
- drop qt_deprecated patch as it was merged upstream

* Sun Sep 26 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.1-1
- update to 2.4.1

* Mon Aug 30 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.0-2
- rebuilt

* Tue Aug 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-1
- update to 2.4.0 release

* Mon Aug 23 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.6.rc3
- update to 2.4.0rc3

* Sat Aug 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.5.rc2
- update to 2.4.0rc2

* Fri Aug 20 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.4.rc1
- update to 2.4.0rc1

* Fri Aug 20 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.3.beta3
- drop upstream missing includes patch
- update to 2.4.0beta3

* Thu Aug 19 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.2.beta2
- add upstream missing includes patch
- update to 2.4.0beta2

* Tue Aug 17 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.1.beta1
- drop upstream patches
- update to 2.4.0beta1

* Fri Aug 13 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-3
- remove temporary gcc45 patch and replace with upstream fix

* Fri Jul 30 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-2
- rebuild for new boost version
- add gcc45 patch (temporary patch till it's fixed properly)

* Tue Jul 27 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-1
- update to 2.3.0 final

* Sun Jul 25 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.13.rc10
- update to 2.3.0rc10

* Sat Jul 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.12.rc9
- update to 2.3.0rc9

* Fri Jul 23 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.11.rc8
- update to 2.3.0rc8

* Thu Jul 22 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.10.rc7
- add Br qtsinglecoreapplication-devel
- add patch so nox uses qtsinglecoreapplication

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.9.rc7
- revert last commit

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.8.rc7
- disable qtsingleapplication for nox build

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.7.rc7
- update to 2.3.0rc7

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.6.rc6
- disable extra debugging

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.5.rc6
- update to 2.3.0rc6
- drop Br gtk3-devel
- add Br qtsingleapplication-devel
- use system qtsingleapplication

* Mon Jul 19 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.4.rc5
- update to 2.3.0rc5
- add patch to fix libnotify gtk problem

* Thu Jul 08 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.3.rc2
- update to 2.3.0rc2
- add Br gtk3-devel
- fix qt deprecated warning

* Sun Jun 13 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.2.beta2
- update to 2.3.0beta2

* Mon May 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.1.beta1
- update to 2.3.0beta1

* Mon May 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.8-1
- update to 2.2.8

* Thu May 13 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.7-1
- update to 2.2.7

* Sun Apr 18 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.6-1
- update to 2.2.6

* Wed Apr 07 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.5-1
- update to 2.2.5

* Tue Apr 06 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.4-1
- update to 2.2.4

* Sun Apr 04 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.3-1
- update to 2.2.3
- drop upstream patch (disable peer host name resolution)

* Fri Apr 02 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.2-2
- add patch to disable peer host name resolution (bz577723)

* Mon Mar 22 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.2-1
- update to 2.2.2
- remove upstream patches (abrt & robust_resume)

* Sun Mar 21 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.1-3
- add robust_resume patch

* Sat Mar 20 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.1-2
- add abrt patch

* Sat Mar 20 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.1-1
- update to 2.2.1

* Sun Mar 14 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.0-1
- update to 2.2.0

* Mon Mar 08 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.0-0.12.rc2
- update to 2.2.0rc2

* Thu Mar 04 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.0-0.11.rc1
- update to 2.2.0rc1

* Wed Feb 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.10.beta4
- rebuilt for new qt version

* Wed Feb 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.9.beta4
- rebuilt for new qt version

* Wed Feb 10 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.8.beta4
- update to 2.2.0beta4
- drop upstream patch
- add build require GeoIP-devel

* Tue Feb 09 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.7.beta3
- redo duplicate crash patch (svn 3564)

* Tue Feb 09 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.6.beta3
- add duplicate crash patch to fix crash when adding 
  a torrent that already exists in the transfer list
- add patch to fix DSO link problem

* Mon Feb 08 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.0-0.5.beta3
- update to 2.2.0beta3

* Sun Jan 31 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.4.beta2
- update to 2.2.0beta2
- drop upstream patch

* Mon Jan 25 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.3.beta1
- add patch to Fix alternative upload speed limit overwriting

* Sun Jan 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.2.beta1
- add patch to disable extra debugging (corrects build flags)

* Sun Jan 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.1.beta1
- update to 2.2.0beta1

* Sun Jan 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.2-1
- update to 2.1.2
- drop gcc patch

* Thu Jan 21 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.1-3
- add some docs to the nox package

* Wed Jan 20 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.1-2
- seperate the gui and nox build processes so debuginfo is built properly

* Wed Jan 20 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.1-1
- update to 2.1.1

* Mon Jan 18 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.0-1
- update to 2.1.0

* Sun Jan 17 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.0-0.13.rc7
- add patch to fix height of the status filters list

* Fri Jan 15 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.12.rc7
- add patch to use HTTP digest mode for Web UI authentication

* Thu Jan 14 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.11.rc7
- update to 2.1.0rc7

* Mon Jan 11 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.10.rc6
- update to 2.1.0rc6

* Mon Jan 11 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.9.rc5
- drop disable extra debug from gcc patch

* Mon Jan 11 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.8.rc5
- update to 2.1.0rc5
- drop nox patch

* Sat Jan 09 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.7.rc4
- disable geoip database and libnotify for the headless version
- add patch so nox doesn't require libQtGui.so.4
- correct previous date in changelog

* Sat Jan 09 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.6.rc4
- update to 2.1.0rc4
- build headless version as well

* Tue Jan 05 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.5.rc3
- update to 2.1.0rc3

* Sun Jan 03 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.4.rc2
- update to 2.1.0rc2

* Wed Dec 30 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.3.beta3
- update to 2.1.0beta3

* Wed Dec 23 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.2.beta1
- update to 2.1.0beta2

* Sun Dec 20 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.1.beta1
- update to 2.1.0beta1
- disable extra debugging to gcc patch

* Fri Dec 18 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.2-1
- update to 2.0.2
- add gcc patch to fix #548491

* Mon Dec 14 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-1
- update to 2.0.1
- clean up spec file

* Thu Dec 10 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-1
- update to 2.0.0

* Mon Dec 07 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.13.svn3058
- update to svn 3058 (RC6)

* Mon Dec 07 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.12.svn3054
- change requires qt4

* Mon Dec 07 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.11.svn3054
- update to svn 3054
- add Br: libnotify-devel

* Sun Dec 06 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.10.svn3043
- update to svn 3043

* Wed Dec 02 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.9.svn3027
- update to svn 3027

* Sun Nov 29 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.8.svn3011
- update to svn 3011

* Fri Nov 27 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.7.svn2985
- update to svn 2985

* Thu Nov 26 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.6.svn2979
- update to svn 2979

* Tue Nov 24 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.5.svn2930
- update to svn 2930

* Tue Nov 24 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.4.svn2927
- update to svn 2927

* Sun Nov 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-0.3.svn2885
- BR: qt4-devel, Requires: qt4 >= %%_qt4_version

* Sun Nov 22 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.2svn2885
- update to svn 2885

* Sun Nov 22 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.1svn2879
- update to svn 2879
- Drop Build requires  zziplib-devel and curl-devel

* Thu Nov 19 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.5.6-1
- update to 1.5.6

* Wed Nov 04 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.5-1
- update to 1.5.5

* Tue Oct 27 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.4-2
- rebuilt for qt 4.6

* Sun Oct 25 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.4-1
- update to 1.5.4
- drop flags patch

* Fri Oct 02 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.3-3
- bump spec due to cvs tagging error

* Fri Oct 02 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.3-2
- Rebuild for rb_libtorrent-0.14.6

* Thu Oct 01 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-1
- update to 1.5.3

* Tue Sep 22 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.2-1
- update to 1.5.2

* Thu Sep 10 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.1-2
- correct prep section package name

* Thu Sep 10 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.0-0.2.20090829svn
- add icons_qrc.patch

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.0-0.1.20090829svn
- update to svn 2578
- redo qbittorrent_flag patch (again :-( )

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.1-3
- redo qbittorrent_flag patch (again :-( )

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.1-2
- redo qbittorrent_flag patch

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.1-1
- update to 1.4.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.0-0.10.rc2
- rebuilt with new openssl

* Fri Aug 07 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.0-0.9.rc2
- correct prep section package name

* Fri Aug 07 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.0-0.8.rc2
- update to 1.4.0rc2

* Mon Aug 03 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.0-0.7.20090803svn
- update to svn 2417

* Sat Jul 25 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.6.20090725svn
- update to svn 2409

* Wed Jul 15 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.5.20090715svn
- update to svn 2385

* Tue Jun 23 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.4.20090429svn
- replace update-mime-database with update-desktop-database
- update scriplets to the latest guidelines
- clean up white space

* Thu Jun 4 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.3.20090429svn
- Rebuild against the new rb_libtorrent version 0.14.4

* Fri May 22 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.2.20090429svn
- rebuild against boost-1.39

* Thu Apr 30 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.1.20090429svn
- Correct version & release tag
- Update to svn 2341 

* Wed Apr 29 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-3.4.2340svn
- Rebuild against the new rb_libtorrent version 0.14.3

* Sun Apr 26 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-3.3.2340svn
- Fix command to generate tarball

* Sun Apr 26 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-3.2.2340svn
- Fixes peference UI bug and splash screen  (launchpad 366957)

* Sat Apr 25 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-3.1.1511bzr
- Update to bzr 1511 

* Thu Apr 9 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-2
- Remember to update Source in spec file 

* Thu Apr 9 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-1
- update to version 1.3.3

* Sat Mar 7 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-13
- Had problems with cvs commit

* Sat Mar 7 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-12
- update to version 1.3.2

* Wed Mar 4 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-11
- Remove qhostaddress.h.patch 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-9
- add Br glib2-devel

* Mon Feb 23 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-8
- Add patch to fix qt build error (Thanks for the fix Rex)

* Mon Feb 9 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-7
- add patch to remove flags from menu to conform to Fedora 
- packaging guidelines.

* Sun Feb 8 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-6
- add more changes for review  

* Sat Feb 7 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-5
- update to 1.3.1 and add more recommended changes for review

* Thu Feb 5 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-4
- add update-mime-database to the post & postun sections

* Thu Feb 5 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-3
- add recommended changes for review

* Wed Jan 14 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-2
- clean up spec file

* Wed Jan 14 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-1
- update version

* Tue Jan 6 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3bzr1436
- bzr build 1436

* Fri Nov 7 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.3bzr1303
- first bzr build
- remove libMagick++ dependency 

* Tue Nov 4 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-2
- add requires qbittorrent-release

* Tue Nov 4 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-1
- update version

* Thu Oct 9 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-5
- rebuild against the rebuilt rb_libtorrent package

* Thu Oct 9 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-4
- build with gmake & fix group tag 

* Wed Oct 8 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-3
- rebuild to fix destop file + icon

* Wed Oct 8 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-2
- rebuild

* Sun Apr 13 2008 - Leigh Scott <leigh123linux@googlemail.com> 
- Initial release
