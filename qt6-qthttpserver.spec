%global qt_module qthttpserver

#global unstable 1
%if 0%{?unstable}
%global prerelease rc2
%endif

%global examples 1

Summary: Qt6 - httpserver component
Name:    qt6-%{qt_module}
Version: 6.4.3
Release: 2%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://qt.io
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtbase-private-devel
#libQt6Core.so.6(Qt_5_PRIVATE_API)(64bit)
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtwebsockets-devel

%description
Qt HTTP Server provides building blocks for embedding a lightweight HTTP server
based on RFC 2616 in an application. There are classes for the messages sent and
received, and for the various parts of an HTTP server.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1


%build
%cmake_qt6 -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install


## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%files
%license LICENSES/*
%{_qt6_libdir}/libQt6HttpServer.so.6*

%files devel
%{_qt6_headerdir}/QtHttpServer/
%{_qt6_libdir}/libQt6HttpServer.so
%{_qt6_libdir}/libQt6HttpServer.prl
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtHttpServerTestsConfig.cmake
%dir %{_qt6_libdir}/cmake/Qt6HttpServer/
%{_qt6_libdir}/cmake/Qt6HttpServer/*.cmake
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_httpserver*.pri
%{_qt6_libdir}/pkgconfig/*.pc
%{_qt6_datadir}/modules/*.json
%{_qt6_libdir}/metatypes/*.json

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif


%changelog
