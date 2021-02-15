%define _disable_lto %nil
Name:           SoapySDR
Version:        0.7.2
Release:        1
Summary:        A Vendor Neutral and Platform Independent SDR Support Library

License:        Boost
URL:            https://github.com/pothosware/%{name}
Source0:	https://github.com/pothosware/SoapySDR/archive/soapy-sdr-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  swig
BuildRequires:  doxygen
BuildRequires:	python-devel
BuildRequires:	python-numpy

%description
SoapySDR is an open-source generalized C/C++ API and runtime library
for interfacing with Software-Defined Radio (SDR) devices.

%package -n python-%{name}
Summary:        Python Bindings for SoapySDR
%{?python_provide:%python_provide python-%{name}}

%description -n python-%{name}
SoapySDR is an open-source generalized C/C++ API and runtime library
for interfacing with Software-Defined Radio (SDR) devices.

%package -n %{name}-devel
Summary:        Development Files for SoapySDR
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n %{name}-devel
SoapySDR is an open-source generalized C/C++ API and runtime library
for interfacing with Software-Defined Radio (SDR) devices.

%prep
%autosetup -p1 -n %{name}-soapy-sdr-%{version}
sed -i 's!head-ref!HEAD!g' cmake/Modules/GetGitRevisionDescription.cmake.in

%build
export Python_ADDITIONAL_VERSIONS="%{python_version}"
export CFLAGS="%{optflags} -pthread"
export CXXFLAGS="%{optflags} -pthread"
%cmake -DUSE_PYTHON_CONFIG=ON -DPYTHON3_EXECUTABLE=%{__python} -DBUILD_PYTHON3=ON
%make_build LIBS="-pthread"

%install
%make_install -C build
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/%{name}/modules0.7

%check
ctest -V %{?_smp_mflags}

%files
%license LICENSE_1_0.txt
%{_bindir}/SoapySDRUtil
%{_libdir}/libSoapySDR.so.0.7*
%{_mandir}/man1/*
%doc README.md
# for hardware support modules
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules0.7

%files -n python-%{name}
%license LICENSE_1_0.txt
%{python_sitearch}/SoapySDR.py
%{python_sitearch}/_SoapySDR.so
%{python_sitearch}/__pycache__/SoapySDR.cpython-*.opt-1.pyc
%{python_sitearch}/__pycache__/SoapySDR.cpython-*.pyc

%files -n %{name}-devel
%{_includedir}/%{name}
%{_libdir}/libSoapySDR.so
%{_libdir}/pkgconfig/*
%dir %{_datadir}/cmake/%{name}
%{_datadir}/cmake/%{name}/*
