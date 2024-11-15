# TODO: system libcall-ui (when it's ready to use system-wide)?
#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	Phosh - pure wayland shell for mobile devices
Summary(pl.UTF-8):	Phosh - oparta na czystym wayland powłoka dla urządzeń przenośnych
Name:		phosh
Version:	0.43.0
Release:	1
License:	GPL v3+
Group:		Applications
Source0:	https://download.gnome.org/sources/phosh/0.43/%{name}-%{version}.tar.xz
# Source0-md5:	7ad054e712c2c97a6b4107d085e12084
URL:		https://developer.puri.sm/Librem5/Software_Reference/Environments/Phosh.html
BuildRequires:	NetworkManager-devel >= 2:1.14
BuildRequires:	alsa-lib-devel
BuildRequires:	evince-devel >= 3
BuildRequires:	evolution-data-server-devel >= 3.33.1
BuildRequires:	fribidi-devel
BuildRequires:	gcr-ui-devel >= 3.7.5
BuildRequires:	gettext-tools
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.76
BuildRequires:	gmobile-devel >= 0.1.0
BuildRequires:	gnome-bluetooth3-devel >= 46.0
# >= 45 when released
BuildRequires:	gnome-desktop-devel >= 43
BuildRequires:	gobject-introspection-devel
BuildRequires:	gsettings-desktop-schemas-devel >= 47
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	json-glib-devel >= 1.6.2
BuildRequires:	libcallaudio-devel >= 0.1
BuildRequires:	libfeedback-devel >= 0.4.0
BuildRequires:	libhandy1-devel >= 1.2
BuildRequires:	libsecret-devel
BuildRequires:	libsoup3-devel >= 3.0
BuildRequires:	meson >= 1.0.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.122
BuildRequires:	pulseaudio-devel >= 13
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
# or libelogind >= 241
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
Requires:	glib2 >= 1:2.76
Requires:	gmobile >= 0.1.0
Requires:	gnome-desktop >= 43
Requires:	gtk+3 >= 3.22
Requires:	json-glib >= 1.6.2
Requires:	libfeedback >= 0.4.0
Requires:	libhandy1 >= 1.2
Requires:	polkit >= 0.122
Requires:	pulseaudio >= 13
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
	--default-library=shared \
	--libexecdir=%{_libexecdir}/phosh \
	-Dcallui-i18n=true \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dman=true \
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
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/phosh-session
%dir %{_libdir}/phosh
%dir %{_libdir}/phosh/plugins
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-caffeine-quick-setting.so
%{_libdir}/phosh/plugins/caffeine-quick-setting.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-calendar.so
%{_libdir}/phosh/plugins/calendar.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-dark-mode-quick-setting.so
%{_libdir}/phosh/plugins/dark-mode-quick-setting.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-emergency-info.so
%{_libdir}/phosh/plugins/emergency-info.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-launcher-box.so
%{_libdir}/phosh/plugins/launcher-box.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-mobile-data-quick-setting.so
%{_libdir}/phosh/plugins/mobile-data-quick-setting.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-night-light-quick-setting.so
%{_libdir}/phosh/plugins/night-light-quick-setting.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-pomodoro-quick-setting.so
%{_libdir}/phosh/plugins/pomodoro-quick-setting.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-simple-custom-quick-setting.so
%{_libdir}/phosh/plugins/simple-custom-quick-setting.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-ticket-box.so
%{_libdir}/phosh/plugins/ticket-box.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-upcoming-events.so
%{_libdir}/phosh/plugins/upcoming-events.plugin
%attr(755,root,root) %{_libdir}/phosh/plugins/libphosh-plugin-wifi-hotspot-quick-setting.so
%{_libdir}/phosh/plugins/wifi-hotspot-quick-setting.plugin
%dir %{_libdir}/phosh/plugins/prefs
%attr(755,root,root) %{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-emergency-info.so
%attr(755,root,root) %{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-pomodoro-quick-setting.so
%attr(755,root,root) %{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-ticket-box.so
%attr(755,root,root) %{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-upcoming-events.so
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
%{_datadir}/glib-2.0/schemas/00_mobi.Phosh.gschema.override
%{_datadir}/glib-2.0/schemas/mobi.phosh.plugins.pomodoro.gschema.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.enums.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.gschema.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.plugins.launcher-box.gschema.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.plugins.ticket-box.gschema.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.plugins.upcoming-events.gschema.xml
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
%{_pkgconfigdir}/phosh-settings.pc

%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/phosh-0
