Summary:	Phosh - pure wayland shell for mobile devices
Summary(pl.UTF-8):	Phosh - oparta na czystym wayland powłoka dla urządzeń przenośnych
Name:		phosh
Version:	0.16.0
Release:	1
License:	GPL v3+
Group:		Applications
Source0:	https://download.gnome.org/sources/phosh/0.16/%{name}-%{version}.tar.xz
# Source0-md5:	76c01b7e873d29ac2bd3fae0871ee6c0
URL:		https://developer.puri.sm/Librem5/Software_Reference/Environments/Phosh.html
BuildRequires:	NetworkManager-devel >= 2:1.14
BuildRequires:	alsa-lib-devel
BuildRequires:	fribidi-devel
BuildRequires:	gcr-ui-devel >= 3.7.5
BuildRequires:	glib2-devel >= 1:2.62
BuildRequires:	gnome-desktop-devel >= 3.26
BuildRequires:	gobject-introspection-devel
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	libcallaudio-devel
BuildRequires:	libfeedback-devel
BuildRequires:	libhandy1-devel >= 1.2
BuildRequires:	libsecret-devel
BuildRequires:	meson >= 0.54.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.105
BuildRequires:	pulseaudio-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-devel >= 1:241
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel
BuildRequires:	upower-devel >= 0.99.1
# wayland-client
BuildRequires:	wayland-devel >= 1.14
BuildRequires:	wayland-protocols >= 1.12
BuildRequires:	xz
Requires:	NetworkManager >= 2:1.14
Requires:	gcr-ui >= 3.7.5
Requires:	glib2 >= 1:2.62
Requires:	gnome-desktop >= 3.26
Requires:	gtk+3 >= 3.22
Requires:	libhandy1 >= 1.2
Requires:	polkit >= 0.105
Requires:	pulseaudio >= 2.0
Requires:	systemd-libs >= 1:241
Requires:	upower >= 0.99.1
Requires:	wayland >= 1.14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Phosh is a pure wayland shell for mobile devices.

%description -l pl.UTF-8
Phosh to oparta na czystym wayland powłoka dla urządzeń przenośnych.

%prep
%setup -q

%build
%meson build \
	-Dcallui-i18n=true \
	-Dsystemd=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# unify
%{__mv} $RPM_BUILD_ROOT%{_localedir}/zh{_Hans,}_CN
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/es_ES

# phosn and call-ui domains
%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/phosh
%attr(755,root,root) %{_libexecdir}/phosh
%{systemduserunitdir}/sm.puri.Phosh.service
%{systemduserunitdir}/sm.puri.Phosh.target
%dir %{systemduserunitdir}/gnome-session@phosh.target.d
%{systemduserunitdir}/gnome-session@phosh.target.d/session.conf
%{_datadir}/glib-2.0/schemas/00_sm.puri.Phosh.gschema.override
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.enums.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.gschema.xml
%{_datadir}/gnome-session/sessions/phosh.session
%{_datadir}/phosh
%{_datadir}/wayland-sessions/phosh.desktop
%{_desktopdir}/sm.puri.Phosh.desktop
