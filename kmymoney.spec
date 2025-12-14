%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kmymoney
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# Required for Mageia >= 2: removes the ldflag '--no-undefined'
%define _disable_ld_no_undefined 1

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.0.5
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Personal finance manager for TDE
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/office/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:		kmymoneytitlelabel.png
Source2:		%{name}-rpmlintrc

BuildSystem:  	cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DCMAKE_SKIP_INSTALL_RPATH=OFF
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_RPATH="%{tde_libdir}"
BuildOption:    -DCMAKE_INSTALL_PREFIX="%{tde_prefix}"
BuildOption:    -DBIN_INSTALL_DIR="%{tde_bindir}"
BuildOption:    -DDOC_INSTALL_DIR="%{tde_docdir}"
BuildOption:    -DINCLUDE_INSTALL_DIR="%{tde_tdeincludedir}"
BuildOption:    -DLIB_INSTALL_DIR="%{tde_libdir}"
BuildOption:    -DPKGCONFIG_INSTALL_DIR="%{tde_libdir}/pkgconfig"
BuildOption:    -DSYSCONF_INSTALL_DIR="%{_sysconfdir}/trinity"
BuildOption:    -DSHARE_INSTALL_PREFIX="%{tde_datadir}"
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
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
BuildRequires:	libtqt3-mt-sqlite3
Requires:		libtqt3-mt-sqlite3

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
%{tde_bindir}/kmymoney
%{tde_bindir}/kmymoney2
%{tde_tdeappdir}/kmymoney2.desktop
%{tde_datadir}/mimelnk/application/x-kmymoney2.desktop
%{tde_datadir}/servicetypes/kmymoneyimporterplugin.desktop
%{tde_datadir}/servicetypes/kmymoneyplugin.desktop
%{tde_libdir}/*.so.*
%{tde_tdelibdir}/kmm_ofximport.la
%{tde_tdelibdir}/kmm_ofximport.so

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
%{tde_datadir}/apps/kmymoney2/
%{tde_datadir}/config.kcfg/kmymoney2.kcfg
%{tde_datadir}/icons/hicolor/*/*/*.png
#%dir %{tde_datadir}/icons/Tango/
#%dir %{tde_datadir}/icons/Tango/*/
#%dir %{tde_datadir}/icons/Tango/*/*/
#%{tde_datadir}/icons/Tango/*/*/*.png
#%{tde_datadir}/icons/Tango/scalable/*.svgz
%{tde_datadir}/icons/locolor/*/*/*.png
#%dir %{tde_datadir}/icons/oxygen/
#%dir %{tde_datadir}/icons/oxygen/*/
#%dir %{tde_datadir}/icons/oxygen/*/*/
#%{tde_datadir}/icons/oxygen/*/*/*.png
#%{tde_datadir}/icons/oxygen/scalable/*.svgz
%{tde_tdedocdir}/HTML/en/kmymoney2/
%{tde_mandir}/man1/kmymoney2.*
%{tde_datadir}/apps/kmm_ofximport/
%{tde_datadir}/services/kmm_ofximport.desktop

##########

%package devel
Summary:		KMyMoney development files
Group:			Development/Libraries
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package contains development files needed for KMyMoney plugins.

%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/kmymoney/
%{tde_libdir}/libkmm_kdchart.la
%{tde_libdir}/libkmm_mymoney.la
%{tde_libdir}/libkmm_plugin.la
%{tde_libdir}/*.so
%{_libdir}/tqt3/plugins/designer/libkmymoney.la
%{_libdir}/tqt3/plugins/designer/libkmymoney.so

%prep -a
%__install -m644 %{SOURCE1} kmymoney2/widgets/


%conf -p
unset QTDIR QTLIB QTINC
export PATH="%{tde_bindir}:${PATH}"


%install -a
%find_lang kmymoney2

# Links duplicate files
%fdupes "%{?buildroot}%{tde_datadir}"

