%define Summary ChBg - Desktop background manager/changer/screensaver
Summary:	%Summary
Name:		chbg
Version:	2.0.1
Release:	%mkrel 5
Source0:	http://www.beebgames.com/sw/%{name}-%{version}.tar.bz2
Source1:	%{name}_16x16.png
Source2:	%{name}_32x32.png
Source3:	%{name}_48x48.png
# (fc) 2.0.1-3mdv use correct depth with composite
Patch0: 	chbg-2.0.1-composite.patch.bz2
URL:		http://www.beebgames.com/sw/gtk-ports.html
License:	GPL
Group:		Graphics
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel

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
%configure2_5x --with-intl-includes=%{_datadir}/gettext/intl \
    --x-libraries="-lz"

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# install icons
mkdir -p %buildroot{%{_miconsdir},%{_iconsdir},%{_liconsdir}}
install -m 644 %{SOURCE1} %buildroot%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE2} %buildroot%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE3} %buildroot%{_liconsdir}/%{name}.png

# menu stuff
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=ChBg
Comment=%Summary
Exec=%{name}
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Other;Settings;
EOF


# touch the default sysconfig file so that it can be included
mkdir -p %buildroot%{_sysconfdir}
touch %buildroot%{_sysconfdir}/chbgrc

%{find_lang} %{name}

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog README THANKS TODO chbgrc.sample xscreensaver*txt 
%{_bindir}/chbg
%_datadir/applications/mandriva*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man*/*
%attr(644,root,root) %config(noreplace,missingok) %{_sysconfdir}/chbgrc
