# Legacy ROCm tracer + libroctx64. TheRock 10.0 still ships it;
# rocprofiler-sdk-roctx is the successor, but many consumers look
# for libroctx64 from this package.

Name:		roctracer
Version:	10.0.0
Release:	1
Summary:	ROCm tracer and ROCTx annotation library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-systems
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-10.0/roctracer.tar.gz#/roctracer-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	rocm-runtime-devel
BuildRequires:	python
BuildRequires:	python%{pyver}dist(cppheaderparser)

%description
libroctracer64 traces HSA/HIP API calls. libroctx64 provides the
ROCTx markers used by PyTorch Kineto and RCCL (torch.cuda.nvtx).

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers for roctracer and ROCTx.

%prep
%autosetup -n roctracer -p1

%build
export CXX=hipcc
export CC=clang
%cmake %{rocm_cmake_fhs} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%ninja_build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib ] && [ ! -d %{buildroot}%{_libdir}/libroctracer64.so ] && [ -e %{buildroot}/usr/lib/libroctracer64.so* ]; then
	mkdir -p %{buildroot}%{_libdir}
	mv %{buildroot}/usr/lib/libroctracer64.so* %{buildroot}%{_libdir}/ 2>/dev/null || true
	mv %{buildroot}/usr/lib/libroctx64.so* %{buildroot}%{_libdir}/ 2>/dev/null || true
	if [ -d %{buildroot}/usr/lib/roctracer ]; then
		mv %{buildroot}/usr/lib/roctracer %{buildroot}%{_libdir}/
	fi
	if [ -d %{buildroot}/usr/lib/cmake ]; then
		mkdir -p %{buildroot}%{_libdir}/cmake
		mv %{buildroot}/usr/lib/cmake/* %{buildroot}%{_libdir}/cmake/ 2>/dev/null || true
	fi
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libroctracer64.so.*
%{_libdir}/libroctx64.so.*
%{_libdir}/roctracer/
%exclude %{_docdir}/roctracer/LICENSE.md

%files devel
%{_includedir}/roctracer.h
%{_includedir}/roctracer_*.h
%{_includedir}/roctx.h
%{_libdir}/libroctracer64.so
%{_libdir}/libroctx64.so
