#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# unit tests (encoder-enabled szip required)
#
Summary:	NetCDF C++ library
Summary(pl.UTF-8):	Biblioteka NetCDF dla języka C++
Name:		netcdf-cxx4
Version:	4.3.1
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/%{name}-%{version}.tar.gz
# Source0-md5:	19cccc27a24fc9095ddbe84bf90ebc83
Patch0:		%{name}-link.patch
URL:		http://www.unidata.ucar.edu/packages/netcdf/
BuildRequires:	autoconf >= 2.66
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	netcdf-devel >= 4.6.0
BuildRequires:	texinfo
Requires:	netcdf >= 4.6.0
Obsoletes:	netcdf-c++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a library that provides an implementation of the
interface. The netCDF library also defines a machine-independent
format for representing scientific data. Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The netCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

This package contains C++ library.

%description -l pl.UTF-8
NetCDF (Network Common Data Form) jest interfejsem dostępu do danych
zorganizowanych w tablice. Biblioteka netCDF definiuje niezależny od
maszyny format reprezentowania danych naukowych. Interfejs oraz
biblioteka pozwalają na tworzenie, dostęp i współdzielenie danych.
NetCDF powstał w Unidata Program Center w Boulder, Colorado.

Ten pakiet zawiera bibliotekę dla języka C++.

%package devel
Summary:	Header files for netCDF C++ interface
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu netCDF dla języka C++
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	netcdf-devel >= 4.6.0
Obsoletes:	netcdf-c++-devel

%description devel
Header files for netCDF - C++ interface.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki netCDF - interfejs dla języka C++.

%package static
Summary:	NetCDF C++ static library
Summary(pl.UTF-8):	Biblioteka statyczna netCDF dla języka C++
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	netcdf-c++-static

%description static
Static version of netCDF C++ library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki netCDF dla języka C++.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} -j1 check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# bzip2 plugin packaged in base netcdf
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libh5bzip2.*
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnetcdf_c++4.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README.md RELEASE_NOTES.md
%attr(755,root,root) %{_libdir}/libnetcdf_c++4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdf_c++4.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ncxx4-config
%attr(755,root,root) %{_libdir}/libnetcdf_c++4.so
%{_includedir}/ncAtt.h
%{_includedir}/ncByte.h
%{_includedir}/ncChar.h
%{_includedir}/ncCheck.h
%{_includedir}/ncCompoundType.h
%{_includedir}/ncDim.h
%{_includedir}/ncDouble.h
%{_includedir}/ncEnumType.h
%{_includedir}/ncException.h
%{_includedir}/ncFile.h
%{_includedir}/ncFloat.h
%{_includedir}/ncGroup.h
%{_includedir}/ncGroupAtt.h
%{_includedir}/ncInt.h
%{_includedir}/ncInt64.h
%{_includedir}/ncOpaqueType.h
%{_includedir}/ncShort.h
%{_includedir}/ncString.h
%{_includedir}/ncType.h
%{_includedir}/ncUbyte.h
%{_includedir}/ncUint.h
%{_includedir}/ncUint64.h
%{_includedir}/ncUshort.h
%{_includedir}/ncVar.h
%{_includedir}/ncVarAtt.h
%{_includedir}/ncVlenType.h
%{_includedir}/netcdf
%{_pkgconfigdir}/netcdf-cxx4.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf_c++4.a
%endif
