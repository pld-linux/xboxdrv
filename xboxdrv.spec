Summary:	Xbox/Xbox360 USB Gamepad userspace driver
Name:		xboxdrv
Version:	0.8.5
Release:	2
License:	GPL v3
Group:		Applications
Source0:	http://pingus.seul.org/~grumbel/xboxdrv/%{name}-linux-%{version}.tar.bz2
# Source0-md5:	7f20b12361770bbff9414a7c6d522c25
Source1:	%{name}.service
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}.blacklist.conf
Source5:	org.seul.Xboxdrv.conf
URL:		http://pingus.seul.org/~grumbel/xboxdrv/
BuildRequires:	boost-devel
BuildRequires:	dbus-devel
BuildRequires:	glib2-devel
BuildRequires:	libusb-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	scons
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libX11-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	rc-scripts
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xboxdrv is a Xbox/Xbox360 gamepad driver for Linux that works in
userspace. It is an alternative to the xpad kernel driver and has
support for Xbox1 gamepads, Xbox360 USB gamepads and Xbox360 wireless
gamepads. The Xbox360 guitar and some Xbox1 dancemats might work too.
The Xbox 360 racing wheel is not supported, but shouldn't be to hard
to add if somebody is interested.

Some basic support for the Xbox360 Chatpad on USB controller is
provided, Chatpad on wireless ones is not supported. The headset is
not supported, but you can dump raw data from it.

This driver is only of interest if the xpad kernel driver doesn't work
for you or if you want more configurabity. If the xpad kernel driver
works for you there is no need to try this driver.

%prep
%setup -qn %{name}-linux-%{version}

%build
%scons \
	BUILD=custom

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{systemdunitdir}} \
	$RPM_BUILD_ROOT{/etc/sysconfig,/etc/rc.d/init.d,/etc/modprobe.d} \
	$RPM_BUILD_ROOT/etc/dbus-1/system.d

install -p xboxdrv $RPM_BUILD_ROOT%{_bindir}
install -p xboxdrvctl $RPM_BUILD_ROOT%{_bindir}

cp -p doc/xboxdrv.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/xboxdrv
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/xboxdrv.service
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/xboxdrv
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/modprobe.d/xboxdrv.blacklist.conf
cp -p install %{SOURCE5} $RPM_BUILD_ROOT/etc/dbus-1/system.d/org.seul.Xboxdrv.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add xboxdrv
%service xboxdrv restart
%systemd_post xboxdrv.service

%preun
%systemd_preun xboxdrv.service
if [ "$1" = "0" ]; then
	%service -q xboxdrv stop
	/sbin/chkconfig --del xboxdrv
fi

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS PROTOCOL README TODO
%doc doc/sensitivity.png doc/sensitivity.svg doc/xbox360-asciiart.txt
%doc examples
%attr(754,root,root) /etc/rc.d/init.d/xboxdrv
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xboxdrv
%{systemdunitdir}/xboxdrv.service
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/xboxdrv.blacklist.conf
/etc/dbus-1/system.d/org.seul.Xboxdrv.conf
%attr(755,root,root) %{_bindir}/xboxdrv
%attr(755,root,root) %{_bindir}/xboxdrvctl
%{_mandir}/man1/xboxdrv.1*
