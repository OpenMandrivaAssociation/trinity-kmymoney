%bcond clang 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg kmymoney
%define tde_prefix /opt/trinity


# Required for Mageia >= 2: removes the ldflag '--no-undefined'
%define _disable_ld_no_undefined 1

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Version:	1.0.5
Release:	%{?tde_version:%{tde_version}_}3
Summary:	Personal finance manager for TDE
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/office/%{tarball_name}-%{tde_version}.tar.xz
Source1:		kmymoneytitlelabel.png
Source2:		%{name}-rpmlintrc

BuildSystem:  	cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DDOC_INSTALL_DIR=%{tde_prefix}/share/doc
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DLIB_INSTALL_DIR=%{tde_prefix}/%{_lib}
BuildOption:    -DPKGCONFIG_INSTALL_DIR=%{tde_prefix}/%{_lib}/pkgconfig
BuildOption:    -DSYSCONF_INSTALL_DIR=%{_sysconfdir}/trinity
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:  trinity-tde-cmake >= %{tde_version}
BuildRequires:	desktop-file-utils

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	libtool
BuildRequires:	fdupes

BuildRequires:	html2ps
BuildRequires:	recode

# OFX support
BuildRequires:  pkgconfig(libofx)

# OPENSP support
BuildRequires:	opensp-devel

# TQT3-sqlite3
BuildRequires:	%{_lib}tqt3-mt-sqlite3
Requires:		%{_lib}tqt3-mt-sqlite3

Requires:		%{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}

BuildRequires:  ghostscript
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

%description
KMyMoney is the Personal Finance Manager for TDE. It operates similar to
MS-Money and Quicken, supports different account types, categorisation of
expenses, QIF import/export, multiple currencies and initial online banking
support.

%files
%defattr(-,root,root,-)
%{tde_prefix}/bin/kmymoney
%{tde_prefix}/bin/kmymoney2
%{tde_prefix}/share/applications/tde/kmymoney2.desktop
%{tde_prefix}/share/mimelnk/application/x-kmymoney2.desktop
%{tde_prefix}/share/servicetypes/kmymoneyimporterplugin.desktop
%{tde_prefix}/share/servicetypes/kmymoneyplugin.desktop
%{tde_prefix}/%{_lib}/*.so.*
%{tde_prefix}/%{_lib}/trinity/kmm_ofximport.la
%{tde_prefix}/%{_lib}/trinity/kmm_ofximport.so

##########

%package common
Summary:		KMyMoney architecture independent files
Group:			Applications/Utilities
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description common
This package contains architecture independent files needed for KMyMoney to
run properly. It also provides KMyMoney documentation. Therefore, unless you
have '%{name}' package installed, you will hardly find this package useful.

%files common -f kmymoney2.lang
%defattr(-,root,root,-)
%{tde_prefix}/share/apps/kmymoney2/
%{tde_prefix}/share/config.kcfg/kmymoney2.kcfg
%{tde_prefix}/share/icons/hicolor/*/*/*.png
%{tde_prefix}/share/icons/locolor/*/*/*.png
%{tde_prefix}/share/doc/tde/HTML/en/kmymoney2/
%{tde_prefix}/share/man/man1/kmymoney2.*
%{tde_prefix}/share/apps/kmm_ofximport/
%{tde_prefix}/share/services/kmm_ofximport.desktop

##########

%package devel
Summary:		KMyMoney development files
Group:			Development/Libraries
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package contains development files needed for KMyMoney plugins.

%files devel
%defattr(-,root,root,-)
%{tde_prefix}/include/tde/kmymoney/
%{tde_prefix}/%{_lib}/libkmm_kdchart.la
%{tde_prefix}/%{_lib}/libkmm_mymoney.la
%{tde_prefix}/%{_lib}/libkmm_plugin.la
%{tde_prefix}/%{_lib}/*.so
%{_libdir}/tqt3/plugins/designer/libkmymoney.la
%{_libdir}/tqt3/plugins/designer/libkmymoney.so

%prep -a
%__install -m644 %{SOURCE1} kmymoney2/widgets/


%conf -p
unset QTDIR QTLIB QTINC
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
%find_lang kmymoney2

# Links duplicate files
%fdupes "%{?buildroot}%{tde_prefix}/share"

