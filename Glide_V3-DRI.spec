#
# _with_3dnow	- with 3Dnow! instructions
%define snapdate 20010309
Summary:	Glide runtime for 3Dfx Voodoo Banshee and Voodoo3 boards
Summary(pl):	Biblioteki Glide dla kart 3Dfx Voodoo Banshee oraz Voodoo3
Name:		Glide_V3-DRI
Version:	3.10.0
Release:	0.%{snapdate}.2
Epoch:		1
Group:		X11/Libraries
Group(de):	X11/Libraries
Group(es):	X11/Bibliotecas
Group(fr):	X11/Librairies
Group(pl):	X11/Biblioteki
License:	3dfx Glide General Public License, 3Dfx Interactive Inc.
URL:		http://glide.sourceforge.net/
Source0:	cvs://anonymous@cvs.glide.sourceforge.net:/cvsroot/glide/glide3x-%{snapdate}.tar.gz
Patch0:		glide-ia64.patch
Patch1:		glide-ac-workaround.patch
Patch2:		glide-h3.patch
Patch3:		glide-h5.patch
Vendor:		3dfx Interactive Inc.
Icon:		3dfx.gif
BuildRequires:	XFree86-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	Glide3-DRI

%description 
This library allows the user to use a 3dfx Interactive Voodoo Banshee
or Voodoo3 card under Linux with DRI support. The source support DRI
or non-DRI versions of Glide.

%description -l pl
Ta biblioteka pozwala u¿ytkownikowi na u¿ywanie kart 3dfx Interactive
Voodoo Banshee lub Voodoo3 pod Linux'em z DRI. Ta wersja zawiera
wsparcie dla wersji Glide z DRI i bez DRI.

%package devel
Summary:	Development headers for Glide 3.x
Summary(pl):	Pliki nag³ówkowe Glide 3.x
Group:		X11/Development/Libraries
Group(de):	X11/Entwicklung/Libraries
Group(fr):	X11/Development/Librairies
Group(pl):	X11/Programowanie/Biblioteki
Requires:	%{name} = %{version}
Provides:	Glide3-DRI-devel

%description devel
This package includes the headers files, documentation, and test files
necessary for developing applications that use the 3Dfx Interactive
Voodoo Banshee or Voodoo3 cards.

%description -l pl devel
Ten pakiet zawiera pliki nag³ówkowe, dokumentacje, oraz pliki tekstowe
wymagane przez aplikacje deweloperskie, które u¿ywaj± kart 3Dfx
Interactive Voodoo Banshe lub Voodoo3.

%package static
Summary:	Static library Glide 3.x
Summary(pl):	Statyczne biblioteki Glide 3.x
Group:		X11/Development/Libraries
Group(de):	X11/Entwicklung/Libraries
Group(fr):	X11/Development/Librairies
Group(pl):	X11/Programowanie/Biblioteki
Requires:	%{name} = %{version}
Provides:	Glide3-DRI-static

%description static
This package includes the static Glide3 library for Voodoo Banshee or
Voodoo3 cards.

%description -l pl static
Ten pakiet zawiera statyczne biblioteki Glide3 dla kart Voodoo Banshee
lub Voodoo3.

%prep
%setup -q -n glide3x-%{snapdate}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
rm -f missing
libtoolize --copy --force
aclocal
autoconf
automake -a -c
%configure \
	--enable-fx-dri-build \
	--enable-fx-glide-hw=h3 \
	--enable-fx-debug=no \
	%{?_with_3dnow:--enable-amd3d}

%{__make} -f makefile.autoconf all \
	GLIDE_DEBUG_GCFLAGS="%{rpmcflags} -fno-expensive-optimizations %{!?debug:-fomit-frame-pointer -ffast-math}" \
	GLIDE_DEBUG_GDEFS="%{!?debug:-DBIG_OPT} %{?debug:-DGDBG_INFO_ON -DGLIDE_DEBUG}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/glide3/tests

# something is recompiled - use GCFLAGS too
%{__make} -f makefile.autoconf install \
	GLIDE_DEBUG_GCFLAGS="%{rpmcflags} -fno-expensive-optimizations %{!?debug:-fomit-frame-pointer -ffast-math}" \
	GLIDE_DEBUG_GDEFS="%{!?debug:-DBIG_OPT} %{?debug:-DGDBG_INFO_ON -DGLIDE_DEBUG}" \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf libglide3.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglide3x_V3.so
ln -sf libglide3.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglide3x.so

# Install the examples and their source, no binaries
install h3/glide3/tests/makefile.distrib $RPM_BUILD_ROOT%{_examplesdir}/glide3/tests/makefile
install h3/glide3/tests/*.3df $RPM_BUILD_ROOT%{_examplesdir}/glide3/tests
install h3/glide3/tests/test??.c $RPM_BUILD_ROOT%{_examplesdir}/glide3/tests
install h3/glide3/tests/tldata.inc $RPM_BUILD_ROOT%{_examplesdir}/glide3/tests
install h3/glide3/tests/tlib.[ch] $RPM_BUILD_ROOT%{_examplesdir}/glide3/tests

gzip -9nf glide_license.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc glide_license.txt.gz
%attr(755,root,root) %{_libdir}/libglide3.so.*.*.*
%attr(755,root,root) %{_libdir}/libglide3x.so
%attr(755,root,root) %{_libdir}/libglide3x_V3.so

%files devel
%defattr(644,root,root,755)
#%doc docs/*.pdf
%{_examplesdir}/glide3
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/libglide3.so
%{_includedir}/glide3

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
