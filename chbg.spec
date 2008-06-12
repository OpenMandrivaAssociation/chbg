%define Summary ChBg - Desktop background manager/changer/screensaver
Summary:	Desktop background manager/changer/screensaver
Name:		chbg
Version:	2.0.1
Release:	%mkrel 6
License:	GPLv2+
Group:		Graphics
URL:		http://www.beebgames.com/sw/gtk-ports.html
Source0:	http://www.beebgames.com/sw/%{name}-%{version}.tar.bz2
Source1:	%{name}_16x16.png
Source2:	%{name}_32x32.png
Source3:	%{name}_48x48.png
# (fc) 2.0.1-3mdv use correct depth with composite
Patch0:		chbg-2.0.1-composite.patch
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ChBg is for changing desktop backgrounds in a given period. It can
render images with 10 modes (such as tiled, centered, scaled, etc.). It
uses gdk_pixbuf-2.0 for loading images, so it supports
many image formats. 
ChBg has a windowed setup program, is able to load setup files, 
can be used as slideshow picture previewer in its own window or as a
desktop background, and can be used as screensaver or as an xscreensaver
hack. It has a dialog for fast previewing of pictures and very usable
thumbnail previews.

%prep
%setup -q
%patch0 -p1 -b .composite

%build
%configure2_5x \
    --with-intl-includes=%{_datadir}/gettext/intl \
    --x-libraries="-lz"

%make

%install
rm -rf %{buildroot}

%makeinstall_std

# install icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# menu stuff
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=ChBg
Comment=%{Summary}
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Other;Settings;
EOF


# touch the default sysconfig file so that it can be included
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/chbgrc

%{find_lang} %{name}

%if %mdkversion < 200900
%post
%{update_menus}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_icon_cache hicolor
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog README THANKS TODO chbgrc.sample xscreensaver*txt 
%{_bindir}/chbg
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man*/*
%attr(644,root,root) %config(noreplace,missingok) %{_sysconfdir}/chbgrc
