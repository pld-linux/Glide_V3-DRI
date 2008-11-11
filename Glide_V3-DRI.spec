%define snapdate 20010309
Summary:	Glide runtime for 3Dfx Voodoo Banshee and Voodoo3 boards
Summary(ko.UTF-8):	3Dfx 부두 벤쉬/3 비디오카드용 Glide 런타임 라이브러리
Summary(pl.UTF-8):	Biblioteki Glide dla kart 3Dfx Voodoo Banshee oraz Voodoo3
Name:		Glide_V3-DRI
Version:	3.10.0
Release:	0.%{snapdate}.14
Epoch:		1
License:	3dfx Glide General Public License, 3Dfx Interactive Inc.
Group:		X11/Libraries
Source0:	cvs://anonymous@cvs.glide.sourceforge.net:/cvsroot/glide/glide3x-%{snapdate}.tar.gz
# Source0-md5:	42a8e093221b2360ec96191ae0e13ce0
Patch0:		glide-ia64.patch
Patch1:		glide-ac-workaround.patch
Patch2:		glide-h3.patch
Patch3:		glide-h5.patch
Patch4:		glide-am16.patch
Patch5:		glide-gcc33.patch
Patch6:		glide-ioctl.patch
Patch7:		glide-morearchs.patch
Patch8:		glide-gcc34.patch
Patch9:	glide-no_redefine_macro.patch
URL:		http://glide.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXxf86dga-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Provides:	Glide3-DRI
Obsoletes:	Glide_V5-DRI
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows the user to use a 3dfx Interactive Voodoo Banshee
or Voodoo3 card under Linux with DRI support. The source support DRI
or non-DRI versions of Glide.

%description -l pl.UTF-8
Ta biblioteka pozwala użytkownikowi na używanie kart 3dfx Interactive
Voodoo Banshee lub Voodoo3 pod Linuksem z DRI. Ta wersja zawiera
wsparcie dla wersji Glide z DRI i bez DRI.

%package devel
Summary:	Development headers for Glide 3.x
Summary(pl.UTF-8):	Pliki nagłówkowe Glide 3.x
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	Glide3-DRI-devel
Obsoletes:	Glide_V5-DRI-devel

%description devel
This package includes the headers files, documentation, and test files
necessary for developing applications that use the 3Dfx Interactive
Voodoo Banshee or Voodoo3 cards.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe, dokumentacje, oraz pliki tekstowe
wymagane przez aplikacje deweloperskie, które używają kart 3Dfx
Interactive Voodoo Banshe lub Voodoo3.

%package static
Summary:	Static library Glide 3.x
Summary(pl.UTF-8):	Statyczne biblioteki Glide 3.x
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	Glide3-DRI-static
Obsoletes:	Glide_V5-DRI-static

%description static
This package includes the static Glide3 library for Voodoo Banshee or
Voodoo3 cards.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczne biblioteki Glide3 dla kart Voodoo Banshee
lub Voodoo3.

%prep
%setup -q -n glide3x-%{snapdate}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake} -i
%configure \
	--enable-fx-dri-build \
	--enable-fx-glide-hw=h3 \
	--enable-fx-debug=no \
%ifarch i586 i686 athlon pentium3 pentium4
	--enable-amd3d
%endif

%{__make} -f makefile.autoconf all \
	GLIDE_DEBUG_GCFLAGS="%{rpmcflags} -fno-expensive-optimizations %{!?debug:-fomit-frame-pointer -ffast-math}" \
	GLIDE_DEBUG_GDEFS="%{!?debug:-DBIG_OPT} %{?debug:-DGDBG_INFO_ON -DGLIDE_DEBUG}" \
	LINK_LIBS="-L/usr/X11R6/%{_lib} -lX11 -lXext -lXxf86dga -lXxf86vm -lm"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/tests

# something is recompiled - use GCFLAGS too
%{__make} -f makefile.autoconf install \
	GLIDE_DEBUG_GCFLAGS="%{rpmcflags} -fno-expensive-optimizations %{!?debug:-fomit-frame-pointer -ffast-math}" \
	GLIDE_DEBUG_GDEFS="%{!?debug:-DBIG_OPT} %{?debug:-DGDBG_INFO_ON -DGLIDE_DEBUG}" \
	LINK_LIBS="-L/usr/X11R6/%{_lib} -lX11 -lXext -lXxf86dga -lXxf86vm -lm" \
	DESTDIR=$RPM_BUILD_ROOT

# used by tdfx_dri.so from XFree86
ln -sf libglide3.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglide3-v3.so
# used by ???
ln -sf libglide3.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglide3x_V3.so
ln -sf libglide3.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglide3x.so

# Install the examples and their source, no binaries
install h3/glide3/tests/makefile.distrib $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/tests/makefile
install h3/glide3/tests/*.3df $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/tests
install h3/glide3/tests/test??.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/tests
install h3/glide3/tests/tldata.inc $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/tests
install h3/glide3/tests/tlib.[ch] $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/tests
gzip -9nf $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/tests/*.3df

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc glide_license.txt
%attr(755,root,root) %{_libdir}/libglide3.so.*.*.*
%attr(755,root,root) %{_libdir}/libglide3-v3.so
%attr(755,root,root) %{_libdir}/libglide3x.so
%attr(755,root,root) %{_libdir}/libglide3x_V3.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglide3.so
%{_libdir}/lib*.la
%{_includedir}/glide3
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
