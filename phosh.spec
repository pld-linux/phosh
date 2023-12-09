#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	Phosh - pure wayland shell for mobile devices
Summary(pl.UTF-8):	Phosh - oparta na czystym wayland powłoka dla urządzeń przenośnych
Name:		phosh
Version:	0.34.0
Release:	2
License:	GPL v3+
Group:		Applications
Source0:	https://download.gnome.org/sources/phosh/0.34/%{name}-%{version}.tar.xz
# Source0-md5:	f62f378e4c841b2e2ba867391ee543ed
URL:		https://developer.puri.sm/Librem5/Software_Reference/Environments/Phosh.html
BuildRequires:	NetworkManager-devel >= 2:1.14
BuildRequires:	alsa-lib-devel
BuildRequires:	evince-devel >= 3
BuildRequires:	evolution-data-server-devel >= 3.33.1
BuildRequires:	fribidi-devel
BuildRequires:	gcr-ui-devel >= 3.7.5
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.74
BuildRequires:	gnome-desktop-devel >= 43
BuildRequires:	gobject-introspection-devel
BuildRequires:	gsettings-desktop-schemas-devel >= 42
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	libcallaudio-devel >= 0.1
BuildRequires:	libfeedback-devel >= 0.2.0
BuildRequires:	libhandy1-devel >= 1.2
BuildRequires:	libsecret-devel
BuildRequires:	meson >= 0.54.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.105
BuildRequires:	pulseaudio-devel >= 2.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
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
Requires:	glib2 >= 1:2.74
Requires:	gnome-desktop >= 43
Requires:	gtk+3 >= 3.22
Requires:	libfeedback >= 0.2.0
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

%package devel
Summary:	Header file for Phosh plugins
Summary(pl.UTF-8):	Plik nagłówkowy do tworzenia wtyczek Phosha
Group:		Development/Libraries

%description devel
Header file for Phosh plugins.

%description devel -l pl.UTF-8
Plik nagłówkowy do tworzenia wtyczek Phosha.

%package apidocs
Summary:	API documentation for Phosh
Summary(pl.UTF-8):	Dokumentacja API Phosh
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Phosh.

%description apidocs -l pl.UTF-8
Dokumentacja API Phosh.

%prep
%setup -q

%build
%meson build \
	--libexecdir=%{_libexecdir}/phosh \
	-Dcallui-i18n=true \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dman=true \
	-Dsystemd=true \
	-Dtools=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/phosh-0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

# outdated file, zh_CN is more complete
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/zh_Hans_CN

# phosh and call-ui domains
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
%attr(755,root,root) %{_bindir}/phosh-session
%dir %{_libdir}/phosh
%dir %{_libdir}/phosh/plugins
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-calendar.so
%{_libdir}/phosh/plugins/calendar.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-emergency-info.so
%{_libdir}/phosh/plugins/emergency-info.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-launcher-box.so
%{_libdir}/phosh/plugins/launcher-box.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-ticket-box.so
%{_libdir}/phosh/plugins/ticket-box.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-upcoming-events.so
%{_libdir}/phosh/plugins/upcoming-events.plugin
%dir %{_libdir}/phosh/plugins/prefs
%attr(755,root,root) %{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-emergency-info.so
%attr(755,root,root) %{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-ticket-box.so
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/phosh
%endif
%attr(755,root,root) %{_libexecdir}/phosh/phosh
%attr(755,root,root) %{_libexecdir}/phosh/phosh-calendar-server
%{systemduserunitdir}/sm.puri.Phosh.service
%{systemduserunitdir}/sm.puri.Phosh.target
%dir %{systemduserunitdir}/gnome-session@phosh.target.d
%{systemduserunitdir}/gnome-session@phosh.target.d/session.conf
# FIXME: which package should own these dirs?
%dir %{_datadir}/xdg-desktop-portal
%dir %{_datadir}/xdg-desktop-portal/portals
%{_datadir}/xdg-desktop-portal/portals/phosh.portal
%{_datadir}/dbus-1/services/sm.puri.Phosh.CalendarServer.service
%{_datadir}/glib-2.0/schemas/00_sm.puri.Phosh.gschema.override
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.enums.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.gschema.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.plugins.launcher-box.gschema.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.plugins.ticket-box.gschema.xml
%{_datadir}/gnome-session/sessions/phosh.session
%{_datadir}/phosh
%{_datadir}/wayland-sessions/phosh.desktop
%{_datadir}/xdg-desktop-portal/phosh-portals.conf
%{_desktopdir}/sm.puri.Phosh.desktop
%{_iconsdir}/hicolor/symbolic/apps/sm.puri.Phosh-symbolic.svg
%{_mandir}/man1/phosh.1*
%{_mandir}/man1/phosh-session.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/phosh
%{_pkgconfigdir}/phosh-plugins.pc

%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/phosh-0
