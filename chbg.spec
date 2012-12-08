Summary:	Desktop background manager/changer/screensaver
Name:		chbg
Version:	2.0.1
Release:	15
License:	GPLv2+
Group:		Graphics
URL:		http://www.beebgames.com/sw/gtk-ports.html
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
%patch0 -p1 -b .composite
%patch1 -p1 -b .cflags
%patch2 -p0 -b .png
%patch3 -p1 -b .linkage

#needed by patch1 and patch3
autoreconf -i

%build
%configure2_5x \
    --with-intl-includes=%{_datadir}/gettext/intl \
    --x-libraries="-lz"

%make

%install
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
%{_bindir}/chbg
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man*/*
%attr(644,root,root) %config(noreplace,missingok) %{_sysconfdir}/chbgrc


%changelog
* Thu Sep 29 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.0.1-14mdv2012.0
+ Revision: 701828
- Patch2: add support for libpng15

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-13
+ Revision: 663366
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-12mdv2011.0
+ Revision: 603824
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-11mdv2010.1
+ Revision: 522357
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-10mdv2010.0
+ Revision: 413230
- rebuild

* Wed Mar 11 2009 Frederic Crozat <fcrozat@mandriva.com> 2.0.1-9mdv2009.1
+ Revision: 353831
- Update patch0 to fix Mdv bug #45277
- Patch1: ensure CFLAGS are used (generate correct debug packages now)

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 2.0.1-8mdv2009.1
+ Revision: 350231
- 2009.1 rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 2.0.1-7mdv2009.0
+ Revision: 264382
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Apr 30 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.0.1-6mdv2009.0
+ Revision: 199350
- new license policy
- decompress patch
- install icons into fd.o compiliant directory
- spec file clean

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2.0.1-5mdv2008.1
+ Revision: 148077
- drop old menu
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Aug 28 2007 Thierry Vignaud <tv@mandriva.org> 2.0.1-5mdv2008.0
+ Revision: 72932
- kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Adam Williamson <awilliamson@mandriva.org>
    - Import chbg



* Fri Sep 01 2006 Nicolas Lécureuil <neoclust@mandriva.org> 2.0.1-5mdv2007.0
- Fix xdg menu

* Wed Aug  2 2006 Götz Waschk <waschk@mandriva.org> 2.0.1-4mdv2007.0
- xdg menu

* Wed Jun 07 2006 Frederic Crozat <fcrozat@mandriva.com> 2.0.1-3mdv2007.0
- Patch0: use correct depth with composite

* Fri May 12 2006 Stefan van der Eijk <stefan@eijk.nu> 2.0.1-2mdk
- rebuild for sparc

* Fri Mar 10 2006 Götz Waschk <waschk@mandriva.org> 2.0.1-1mdk
- new URL
- drop extra translation files
- update file list
- drop patches
- new version

* Thu Mar  9 2006 Götz Waschk <waschk@mandriva.org> 2.0-2mdk
- fix rpmlint warnings about patches
- fix buildrequires

* Wed Mar 08 2006 Frederic Crozat <fcrozat@mandriva.com> 2.0-1mdk
- Release 2.0 (Cris Boylan), based on Mark Sherry's gtk2 port
- Patch4: fix i18n in non UTF8 locale
- Disable patch1 (not needed)

* Mon Aug 29 2005 Frederic Crozat <fcrozat@mandriva.com> 1.5-11mdk 
- Patch3: fix dithering

* Wed Mar 09 2005 Nicolas Lécureuil <neoclust@mandrake.org> 1.5-10mdk
- security fix for CAN-2004-1264

* Mon Nov 15 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.5-9mdk
- rebuild

* Wed Sep 03 2003 David Baudens <baudens@mandrakesoft.com> 1.5-8mdk
- Move in Configuration/Other

* Wed Jul 16 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.5-7mdk
- don't rm -rf $RPM_BUILD_ROOT in %%prep
- cosmetics
- be sure to link against libpng (P1)

* Fri Feb 14 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.5-6mdk
- rebuild

* Mon Jan 14 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.5-5mdk
- convert xpms to pngs

* Thu Jan 10 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.5-4mdk
- Patch0: fix embedding mode for GNOME control center

* Tue Jan  8 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.5-3mdk
- Fix wrong dependencies

* Fri Oct 12 2001  Lenny Cartier <lenny@mandrakesoft.com> 1.5-2mdk
- rebuild against libpng3

* Sun Aug 26 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.5-1mdk
- updated to 1.5

* Thu Jun 28 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.3-2mdk
- rebuild

* Wed Feb 28 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.3-1mdk
- upgraded by Alexander Skwar <ASkwar@Linux-Mandrake.com> :
	- New release
	- Uses gdk-pixbuf explicitely (or however that's spelled *G*)
	- Slimmed down Requires: line to only require what THIS package directly 
  	requires

* Mon Jan 08 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.2-2mdk 
- rebuild

* Wed Nov 22 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.2-1mdk
- updated to 1.2

* Thu Oct 12 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.1-1mdk
- used srpm from  Alexander Skwar <ASkwar@linux-mandrake.com> :
	First Mandrake version
