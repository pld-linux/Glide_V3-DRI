Summary:	Glide runtime for 3Dfx Voodoo Banshee and Voodoo3 boards
Name:		Glide_V3-DRI
Version:	3.10
Release:	6
Group:		Libraries
Copyright:	3dfx Glide General Public License, 3Dfx Interactive Inc.
URL:		http://www.3dfx.com	
Source:		Glide3.10.tar.gz
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

%prep
%setup -q -c
chmod +x swlibs/include/make/ostype

%build
export FX_GLIDE_HW=h3
make -f makefile.linux CNODEBUG="$RPM_OPT_FLAGS -fomit-frame-pointer \
	-funroll-loops -fexpensive-optimizations -ffast-math -DBIG_OPT"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/glide3,%{_libdir}}
install -d $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/{tests,texus/{lib,cmd,examples}}

install -s h3/lib/libglide3.so.3.10 $RPM_BUILD_ROOT%{_libdir}/libglide3.so.3.10
ln -s libglide3.so.3 $RPM_BUILD_ROOT%{_libdir}/libglide3.so
ln -s libglide3.so.3 $RPM_BUILD_ROOT%{_libdir}/libglide3x_V3.so
ln -s libglide3x_V3.so $RPM_BUILD_ROOT%{_libdir}/libglide3x.so

install -s swlibs/lib/libtexus.so.1.1 $RPM_BUILD_ROOT%{_libdir}
ln -s libtexus.so.1 $RPM_BUILD_ROOT%{_libdir}/libtexus.so

install swlibs/include/3dfx.h $RPM_BUILD_ROOT%{_includedir}/glide3
install h3/include/glide.h $RPM_BUILD_ROOT%{_includedir}/glide3
install h3/include/glidesys.h $RPM_BUILD_ROOT%{_includedir}/glide3
install h3/include/glideutl.h $RPM_BUILD_ROOT%{_includedir}/glide3
install h3/include/sst1vid.h $RPM_BUILD_ROOT%{_includedir}/glide3
install swlibs/include/linutil.h $RPM_BUILD_ROOT%{_includedir}/glide3
install swlibs/include/texus.h $RPM_BUILD_ROOT%{_includedir}/glide3

# Install the examples and their source, no binaries
install h3/glide3/tests/makefile.distrib $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests/makefile
install h3/glide3/tests/*.3df $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests
install h3/glide3/tests/test??.c $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests
install h3/glide3/tests/tldata.inc $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests
install h3/glide3/tests/tlib.[ch] $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/tests

# Install the texture tools
install swlibs/texus/makefile.distrib $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/texus/makefile
install swlibs/texus/lib/makefile.distrib $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/texus/lib/makefile
install swlibs/texus/cmd/makefile.distrib $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/texus/cmd/makefile
install swlibs/texus/examples/makefile.distrib $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/texus/examples/makefile
install swlibs/texus/lib/*.c $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/texus/lib
install swlibs/texus/lib/texusint.h $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/texus/lib
install swlibs/texus/cmd/*.c $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/texus/cmd
install swlibs/texus/examples/*.c $RPM_BUILD_ROOT%{_prefix}/src/examples/glide3/texus/examples

gzip -9nf glide_license.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc glide_license.txt.gz
%attr(755,root,root) %{_libdir}/libglide3.so.3.10
%attr(755,root,root) %{_libdir}/libglide3.so
%attr(755,root,root) %{_libdir}/libglide3x.so
%attr(755,root,root) %{_libdir}/libglide3x_V3.so
%attr(755,root,root) %{_libdir}/libtexus.so.1.1
%attr(755,root,root) %{_libdir}/libtexus.so

%files devel
%defattr(644,root,root,755)
%doc docs/*.pdf
%{_prefix}/src/examples/glide3
%{_includedir}/glide3
