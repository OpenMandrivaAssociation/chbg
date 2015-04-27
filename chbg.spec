Summary:	Desktop background manager/changer/screensaver
Name:		chbg
Version:	2.0.1
Release:	26
License:	GPLv2+
Group:		Graphics
Url:		http://www.beebgames.com/sw/gtk-ports.html
Source0:	http://www.beebgames.com/sw/%{name}-%{version}.tar.bz2
Source1:	%{name}_16x16.png
Source2:	%{name}_32x32.png
Source3:	%{name}_48x48.png
# (fc) 2.0.1-3mdv use correct colormap / depth 
Patch0:		chbg-2.0.1-colormap.patch
# (fc) 2.0.1-9mdv fix CFLAGS
Patch1:		chbg-2.0.1-cflags.patch
Patch2:		chbg-2.0.1-libpng1.5.patch
Patch3:		chbg-2.0.1-linkage.patch
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(gtk+-2.0)

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
%apply_patches
#needed by patch1 and patch3
autoreconf -i

%build
export CC=gxx
export CXX=g++

%configure \
	--with-intl-includes=%{_datadir}/gettext/intl \
    --x-libraries="-lz"

%make

%install
%makeinstall_std

# install icons
install -p -m644 %{SOURCE1} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -p -m644 %{SOURCE2} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -p -m644 %{SOURCE3} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# menu stuff
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=ChBg
Comment=Desktop background manager/changer/screensaver
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

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog README THANKS TODO chbgrc.sample xscreensaver*txt 
%config(noreplace,missingok) %{_sysconfdir}/chbgrc
%{_bindir}/chbg
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man*/*
