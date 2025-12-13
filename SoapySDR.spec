%define _disable_lto %nil
%define major 0.8
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}
%bcond_without tests

Name:		SoapySDR
Version:	0.8.1
Release:	5
Summary:	A Vendor Neutral and Platform Independent SDR Support Library
License:	Boost
URL:		https://github.com/pothosware/SoapySDR
Source0:	https://github.com/pothosware/SoapySDR/archive/soapy-sdr-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	swig
BuildRequires:	doxygen
BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(numpy)

%description
SoapySDR is an open-source generalized C/C++ API and runtime library
for interfacing with Software-Defined Radio (SDR) devices.

%package -n python-%{name}
Summary:        Python Bindings for SoapySDR
%{?python_provide:%python_provide python-%{name}}

%description -n python-%{name}
SoapySDR is an open-source generalized C/C++ API and runtime library
for interfacing with Software-Defined Radio (SDR) devices.

%package -n %{libname}
Summary:        Development Files for SoapySDR
Requires:       %{name} = %{EVRD}

%description -n %{libname}
SoapySDR is an open-source generalized C/C++ API and runtime library
for interfacing with Software-Defined Radio (SDR) devices.

%package -n %{devname}
Summary:        Development Files for SoapySDR
Requires:       %{libname} = %{EVRD}

%description -n %{devname}
SoapySDR is an open-source generalized C/C++ API and runtime library
for interfacing with Software-Defined Radio (SDR) devices.

%prep
%autosetup -p1 -n %{name}-soapy-sdr-%{version}
sed -i 's!head-ref!HEAD!g' cmake/Modules/GetGitRevisionDescription.cmake.in

%build
export Python_ADDITIONAL_VERSIONS="%{python_version}"
export CFLAGS="%{optflags} -pthread"
export CXXFLAGS="%{optflags} -pthread"
%cmake \
	-DSOAPY_SDR_VERSION=%{version}-%{release} \
	-DPYTHON3_EXECUTABLE=%{__python} \
	-DBUILD_PYTHON3=ON \
	-G Ninja
%ninja_build

%install
%ninja_install -C build
mkdir -p %{buildroot}/%{_libdir}/%{name}/modules0.7

%if %{with tests}
%check
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
%ninja_test -C build
%endif

%files
%license LICENSE_1_0.txt
%{_bindir}/SoapySDRUtil
%{_mandir}/man1/*
%doc README.md
# for hardware support modules
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules0.7

%files -n %{libname}
%{_libdir}/libSoapySDR.so.%{major}*

%files -n python-%{name}
%license LICENSE_1_0.txt
%{python_sitearch}/SoapySDR.py
%{python_sitearch}/_SoapySDR.so

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/libSoapySDR.so
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_datadir}/cmake/%{name}
%{_datadir}/cmake/%{name}/*
