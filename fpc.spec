# TODO:
# - check why it builds all static..
# - doesn't build on ppc/sparc :/ hgw why
Summary:	32-bit compiler for the i386 and m68k processors
Summary(pl):	32 bitowy kompilator dla procesorСw i386 i m68k
Summary(ru):	Свободный компилятор Pascal
Summary(uk):	В╕льний комп╕лятор Pascal
Name:		fpc
Version:	2.0.4
Release:	2
License:	GPL
Group:		Development/Languages
Source0:	ftp://ftp.freepascal.org/pub/fpc/dist/source-%{version}/%{name}build-%{version}.tar.gz
# Source0-md5:	1ff8b80d1f5f564983bb4e1550b8b53a
Source1:	ftp://ftp.freepascal.org/pub/fpc/dist/i386-linux-%{version}/%{name}-%{version}.i386-linux.tar
# Source1-md5:	d826aab69c98b9efe30398ff63e4c9d9
Source2:	ftp://ftp.freepascal.org/pub/fpc/dist/x86_64-linux-%{version}/%{name}-%{version}.x86_64-linux.tar
# Source2-md5:	3bbfe4c061ebd40502789eccef069d7c
Source3:	ftp://ftp.freepascal.org/pub/fpc/dist/powerpc-linux-%{version}/%{name}-%{version}.powerpc-linux.tar
# Source3-md5:	6ec5302fe446d94e5aaa1e159b0d65df
# no 2.0.4 binary for sparc, 2.0.0 only
Source4:	ftp://ftp.freepascal.org/pub/fpc/dist/sparc-linux-2.0.0/%{name}-2.0.0.sparc-linux.tar
# Source4-md5:	dd8925ce8ce93309456c3072e6e4d14d
Patch0:		%{name}-skip-dev-dot.patch
Patch1:		%{name}-makedocs.patch
Patch2:		%{name}-gdb65.patch
Patch3:		%{name}-avoid-RE.patch
URL:		http://www.freepascal.org/
BuildRequires:	binutils-static >= 3:2.17.50
BuildRequires:	gdb-lib
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	tetex-fonts-jknappen
BuildRequires:	tetex-format-pdflatex
BuildRequires:	tetex-makeindex
BuildRequires:	tetex-metafont
Requires:	binutils
Provides:	fpc-bootstrap
ExclusiveArch:	%{ix86} %{x8664} ppc sparc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free Pascal is a 32-bit compiler for the i386 and m68k processors.
Free Pascal is designed to be, as much as possible, source compatible
with Turbo Pascal 7.0 and Delphi 4 (although this goal is not yet
attained), but it also enhances these languages with elements like
function overloading. And, unlike these ancestors, it supports
multiple platforms.

%description -l pl
Free Pascal to 32 bitowy kompilator dla procesorСw i386 oraz m86k.
Free Pascal zostaЁ zaprojektowany by byФ (jak tylko to mo©liwe)
kompatybilnym z Turbo Pascal 7.0 oraz Delphi 4. Free Pascal rСwnie©
rozszerza te jЙzyki elementami takimi jak przeci╠©anie funkcji.

%description -l ru
FPC -- 32-битный компилятор Pascal, совместимый с Turbo Pascal 7.0 и
Delphi. Поставляется с RTL (библиотекой времени исполнения), FCL
(библиотекой свободных компонент), интерфейсами к gtk, ncurses, zlib,
mysql, postgres, ibase.

%description -l uk
FPC -- 32-б╕тний комп╕лятор Pascal, сум╕сний ╕з Turbo Pascal 7.0 та
Delphi. Постача╓ться ╕з RTL (б╕бл╕отекою часу виконання), FCL
(б╕бл╕отекою в╕льних компонент), ╕нтерфейсами до gtk, ncurses, zlib,
mysql, postgres, ibase.

%package src
Summary:	Free Pascal Compiler source files
Summary(pl):	Pliki ╪rСdЁowe kompilatora Free Pascal
Group:		Development
Requires:	%{name} = %{version}-%{release}
Provides:	fpcsrc

%description src
Free Pascal Compiler source files.

%description src -l pl
Pliki ╪rСdЁowe kompilatora Free Pascal.

%package examples
Summary:	Free Pascal Compiler exaple programs
Summary(pl):	PrzykЁadowe programy do kompilatora Free Pascal
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description examples
Free Pascal Compiler exaple programs.

%description examples -l pl
PrzykЁadowe programy do kompilatora Free Pascal.

%package doc
Summary:	Free Pascal Compiler documentation
Summary(pl):	Dokumentacja do kompilatora Free Pascal
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for fpc in PDF format.

%description doc -l pl
Dokumentacja do fpc w formacie PDF.

%prep
%setup -q -n %{name}build_%{version}_exp
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%ifarch %{ix86}
tar xf %{SOURCE1}
%define _bver %{version}
%define _bname 386
%endif
%ifarch %{x8664}
tar xf %{SOURCE2}
%define _bver %{version}
%define _bname x64
%endif
%ifarch ppc
tar xf %{SOURCE3}
%define _bver %{version}
%define _bname ppc
%endif
%ifarch sparc
tar xf %{SOURCE4}
%define _bver 2.0.0
%define _bname sparc
%endif

tar xf binary.*-linux.tar

mkdir bin
cd bin
for i in ../*.tar.gz ; do
	tar xzf $i
done
ln -sf `pwd`/lib/%{name}/%{_bver}/ppc* bin

%build
# save for fpc-src
install -d fpc-src
cp -af fpcsrc/* fpc-src

PP=`pwd`/bin/lib/%{name}/%{_bver}/ppc%{_bname}
NEWPP=`pwd`/fpcsrc/compiler/ppc%{_bname}
NEWFPDOC=`pwd`/fpcsrc/utils/fpdoc/fpdoc

# DO NOT PUT $RPM_OPT_FLAGS IN OPT, IT DOES NOT WORK - baggins
case "%{_build_cpu}" in
	i386,i486)
		OPTF="-OG2p1" ;;
	i586)
		OPTF="-OG2p2" ;;
	i686,athlon)
		OPTF="-Og2p3" ;;
	*)
		OPTF="-O2" ;;
esac

%{__make} -C fpcsrc compiler_cycle \
	OPT="$OPTF -Xs -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	PP="$PP" \
	FPC="$PP" \
	SMARTLINK=YES

%{__make} -C fpcsrc OPT="$OPTF -Xs -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	GDBLIBDIR=%{_libdir} \
	PP="$NEWPP" \
	FPC="$NEWPP" \
	DATA2INC=`pwd`/utils/data2inc \
	SMARTLINK=YES \
	rtl_clean rtl_smart \
	packages_base_smart \
	fcl_smart \
	fv_smart \
	packages_extra_smart \
	ide_all \
	utils_all

export save_size=10000
%{__make} -C fpcdocs \
	FPDOC=$NEWFPDOC \
	FPC="$NEWPP" \
	pdf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir},%{_datadir}/fpcsrc,%{_examplesdir}/fpc}

cp -af fpc-src/* $RPM_BUILD_ROOT%{_datadir}/fpcsrc

NEWPP=`pwd`/fpcsrc/compiler/ppc%{_bname}
FPCMAKE=`pwd`/fpcsrc/utils/fpcm/fpcmake
%{__make} -C fpcsrc \
	compiler_distinstall \
	rtl_distinstall \
	fcl_distinstall \
	fv_distinstall \
	packages_distinstall \
	ide_distinstall \
	utils_distinstall \
	PP="$NEWPP" \
	FPCMAKE="$FPCMAKE" \
	SMARTLINK=YES \
	INSTALL_PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_DOCDIR=$RPM_BUILD_ROOT%{_docdir} \
	INSTALL_MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	INSTALL_BASEDIR=$RPM_BUILD_ROOT%{_libdir}/%{name}/%{version} \
	INSTALL_EXAMPLEDIR=$RPM_BUILD_ROOT%{_examplesdir}/%{name} \
	INSTALL_MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	CODPATH=$RPM_BUILD_ROOT%{_libdir}/%{name}/lexyacc

%{__make} -C install/man installman \
	INSTALL_MANDIR=$RPM_BUILD_ROOT%{_mandir}

ln -sf %{_libdir}/%{name}/%{version}/ppc%{_bname} $RPM_BUILD_ROOT%{_bindir}

sh fpcsrc/compiler/utils/samplecfg %{_libdir}/%{name}/%{version} $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fpc.cfg
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/lexyacc
%{_libdir}/%{name}/%{version}/msg
%{_libdir}/%{name}/%{version}/units
%{_libdir}/%{name}/%{version}/ide
%{_libdir}/%{name}/lexyacc/*
%attr(755,root,root) %{_libdir}/%{name}/%{version}/ppc%{_bname}
%attr(755,root,root) %{_libdir}/%{name}/%{version}/samplecfg
%{_mandir}/man*/*

%files src
%defattr(644,root,root,755)
%{_datadir}/fpcsrc

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/fpc

%files doc
%defattr(644,root,root,755)
%doc fpcdocs/*.pdf
