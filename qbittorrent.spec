#
# A simple rpm spec control script
#

Name:    qbittorrent-enhanced-edition
Summary: A enhanced bittorrent client built with QT
Version: 4.3.3.10
Release: 0
License: GPLv2+
URL:     https://github.com/c0re100/qBittorrent-Enhanced-Edition
Source0:  %{name}-%{version}.tar.gz

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

Requires: python3 GeoIP

%description
A Bittorrent client using rb_libtorrent and a Qt Graphical User Interface.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%package nox
Summary: A Headless Bittorrent Client

%description nox
A Headless Bittorrent client using rb_libtorrent.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%prep
%setup -q -n %{name}-%{version} -c

mv %{name}-%{version} build

pushd build
sed -i -e 's@Exec=qbittorrent %U@Exec=env TMPDIR=/var/tmp qbittorrent %U@g' dist/unix/org.qbittorrent.qBittorrent.desktop
sed -i -e 's#ExecStart=@EXPAND_BINDIR@/qbittorrent-nox#env TMPDIR=/var/tmp @EXPAND_BINDIR@/qbittorrent-nox#g' dist/unix/systemd/qbittorrent-nox@.service.in
cp README.md NEWS AUTHORS TODO Changelog COPYING ..
popd

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
%doc NEWS AUTHORS TODO Changelog
%{_bindir}/qbittorrent-nox
%{_unitdir}/qbittorrent-nox@.service
%{_mandir}/man1/qbittorrent-nox.1*

%changelog
* Wed Jan 20 2021 - c0re100 <corehusky@gmail.com> - v4.3.3.10
    - OTHER: Official Update (v4.3.3)
    - FEATURE: [Windows Installer] "Install with Debug Symbol File" Option
