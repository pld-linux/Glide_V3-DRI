%define snapdate 20001102
Summary:	Glide runtime for 3Dfx Voodoo Banshee and Voodoo3 boards
Name:		Glide_V3-DRI
Version:	3.10
Release:	20001102.1
Group:		Libraries
Copyright:	3dfx Glide General Public License, 3Dfx Interactive Inc.
URL:		http://www.3dfx.com	
Source:		Glide3-CVS-%{snapdate}.tar.bz2
Vendor:		3dfx Interactive Inc.
Icon:		3dfx.gif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description 
This library allows the user to use a 3dfx Interactive Voodoo Banshee
or Voodoo3 card under Linux with DRI support. The source support DRI
or non-DRI versions of Glide.

%package devel
Summary:	Development headers for Glide 3.x
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package includes the headers files, documentation, and test files
necessary for developing applications that use the 3Dfx Interactive
Voodoo Banshe or Voodoo3 cards.

%package static
Summary:	Static library Glide 3.x
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description static
This package includes the static Glide3 library.

%prep
%setup -q -n Glide3

%build
mv chores.3dfx chores.3dfx.bak
echo "#!/bin/bash" > chores.3dfx
cat chores.3dfx.bak >> chores.3dfx
chmod 755 chores.3dfx

CFLAGS="$RPM_OPT_FLAGS"
CXXFLAGS="$RPM_OPT_FLAGS"
GLIDE_DEBUG_GCFLAGS="$RPM_OPT_FLAGS"
export CFLAGS CXXFLAGS GLIDE_DEBUG_GCFLAGS
mv -f swlibs/include/make/makefile.autoconf.bottom swlibs/include/make/makefile.autoconf.bottom.bak
sed "s,GLIDE_DEBUG_GCFLAGS = -O6 -m486,GLIDE_DEBUG_GCFLAGS = $RPM_OPT_FLAGS," swlibs/include/make/makefile.autoconf.bottom.bak > swlibs/include/make/makefile.autoconf.bottom
./chores.3dfx \
	--clean \
	--generate \
	--configure="--enable-fx-dri-build --enable-fx-glide-hw=h3" \
	--build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/glide3/tests

make -C build -f makefile.autoconf install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s libglide3.so.*.*.* $RPM_BUILD_ROOT%{_libdir}/libglide3x_V3.so
ln -s libglide3.so.*.*.* $RPM_BUILD_ROOT%{_libdir}/libglide3x.so

# Install the examples and their source, no binaries
install h3/glide3/tests/makefile.distrib $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests/makefile
install h3/glide3/tests/*.3df $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests
install h3/glide3/tests/test??.c $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests
install h3/glide3/tests/tldata.inc $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests
install h3/glide3/tests/tlib.[ch] $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests

gzip -9nf glide_license.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc glide_license.txt.gz
%attr(755,root,root) %{_libdir}/libglide3.so.*.*.*
%attr(755,root,root) %{_libdir}/libglide3.so
%attr(755,root,root) %{_libdir}/libglide3x.so
%attr(755,root,root) %{_libdir}/libglide3x_V3.so

%files devel
%defattr(644,root,root,755)
#%doc docs/*.pdf
%{_prefix}/src/examples/glide3
%{_includedir}/glide3

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
