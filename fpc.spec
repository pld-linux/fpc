# TODO:
# - repair ide build
#
# Conditional build:
%bcond_with	ide			# build with ide
%bcond_without	doc			# build without doc

Summary:	32-bit compiler for the i386 and m68k processors
Summary(pl.UTF-8):	32 bitowy kompilator dla procesorów i386 i m68k
Summary(ru.UTF-8):	Свободный компилятор Pascal
Summary(uk.UTF-8):	Вільний компілятор Pascal
Name:		fpc
Version:	2.4.4
Release:	0.1
License:	GPL
Group:		Development/Languages
Source0:	ftp://ftp.freepascal.org/pub/fpc/dist/%{version}/source/%{name}build-%{version}.tar.gz
# Source0-md5:	d069dfd3412bd0d26dcd1b81ac998305
Source1:	ftp://ftp.freepascal.org/pub/fpc/dist/%{version}/i386-linux/%{name}-%{version}.i386-linux.tar
# Source1-md5:	e761c4866ac4c8fcbe09f657f315ec32
Source2:	ftp://ftp.freepascal.org/pub/fpc/dist/%{version}/x86_64-linux/%{name}-%{version}.x86_64-linux.tar
# Source2-md5:	058e6cd765026748a2bd24c86f1ecf18
Source3:	ftp://ftp.freepascal.org/pub/fpc/dist/%{version}/powerpc-linux/%{name}-%{version}.powerpc-linux.tar
# Source3-md5:	cea93e5da48c45da3147236cba75dc76
Patch0:		%{name}-skip-dev-dot.patch
Patch1:		%{name}-fpdoc.patch
URL:		http://www.freepascal.org/
BuildRequires:	binutils-static >= 3:2.17.50
BuildRequires:	gdb-lib
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
%{?with_ide:BuildRequires:	readline-static}
BuildRequires:	rpmbuild(macros) >= 1.213
%{?with_doc:BuildRequires:	tetex-fonts-jknappen}
%{?with_doc:BuildRequires:	tetex-format-pdflatex}
%{?with_doc:BuildRequires:	tetex-makeindex}
%{?with_doc:BuildRequires:	tetex-metafont}
%{?with_doc:BuildRequires:	texlive-xetex}
Requires:	binutils
Provides:	fpc-bootstrap
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free Pascal is a 32-bit compiler for the i386 and m68k processors.
Free Pascal is designed to be, as much as possible, source compatible
with Turbo Pascal 7.0 and Delphi 4 (although this goal is not yet
attained), but it also enhances these languages with elements like
function overloading. And, unlike these ancestors, it supports
multiple platforms.

%description -l pl.UTF-8
Free Pascal to 32 bitowy kompilator dla procesorów i386 oraz m86k.
Free Pascal został zaprojektowany by być (jak tylko to możliwe)
kompatybilnym z Turbo Pascal 7.0 oraz Delphi 4. Free Pascal również
rozszerza te języki elementami takimi jak przeciążanie funkcji.

%description -l ru.UTF-8
FPC -- 32-битный компилятор Pascal, совместимый с Turbo Pascal 7.0 и
Delphi. Поставляется с RTL (библиотекой времени исполнения), FCL
(библиотекой свободных компонент), интерфейсами к gtk, ncurses, zlib,
mysql, postgres, ibase.

%description -l uk.UTF-8
FPC -- 32-бітний компілятор Pascal, сумісний із Turbo Pascal 7.0 та
Delphi. Постачається із RTL (бібліотекою часу виконання), FCL
(бібліотекою вільних компонент), інтерфейсами до gtk, ncurses, zlib,
mysql, postgres, ibase.

%package src
Summary:	Free Pascal Compiler source files
Summary(pl.UTF-8):	Pliki źródłowe kompilatora Free Pascal
Group:		Development
Requires:	%{name} = %{version}-%{release}
Provides:	fpcsrc

%description src
Free Pascal Compiler source files.

%description src -l pl.UTF-8
Pliki źródłowe kompilatora Free Pascal.

%package examples
Summary:	Free Pascal Compiler exaple programs
Summary(pl.UTF-8):	Przykładowe programy do kompilatora Free Pascal
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description examples
Free Pascal Compiler exaple programs.

%description examples -l pl.UTF-8
Przykładowe programy do kompilatora Free Pascal.

%package doc
Summary:	Free Pascal Compiler documentation
Summary(pl.UTF-8):	Dokumentacja do kompilatora Free Pascal
Group:		Documentation
# doesn't require base

%description doc
Documentation for fpc in PDF format.

%description doc -l pl.UTF-8
Dokumentacja do fpc w formacie PDF.

%prep
%setup -q -n %{name}build-%{version}
%patch0 -p1
%patch1 -p1

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
	i386) OPTF="-OG2p1" ;;
	i486) OPTF="-OG2p1" ;;
	i586) OPTF="-OG2p2" ;;
	i686) OPTF="-Og2p3" ;;
	athlon) OPTF="-Og2p3" ;;
	*) OPTF="-O2" ;;
esac

%{__make} -C fpcsrc compiler_cycle \
	OPT="$OPTF -Xs -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	PP="$PP" \
	FPC="$PP" \
	LINKSMART=YES

%{__make} -C fpcsrc OPT="$OPTF -Xs -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	GDBLIBDIR=%{_libdir} \
	PP="$NEWPP" \
	FPC="$NEWPP" \
	FPDOC=$NEWFPDOC \
	DATA2INC=`pwd`/utils/data2inc \
	LINKSMART=YES \
	NODOCS=YES \
	rtl_clean \
	packages_clean \
	utils_clean \
	%{?with_ide: ide_clean installer_clean} \
	rtl_all \
	packages_all \
	utils_all %{?with_ide:installer_all}

#	%{?with_ide:IDE=YES} \
%if %{with ide}
%{__make} -C fpcsrc/ide OPT="$OPTF -Xs -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	GDBLIBDIR=%{_libdir} \
	PP="$NEWPP" \
	FPC="$NEWPP" \
	FPDOC=$NEWFPDOC \
	DATA2INC=`pwd`/utils/data2inc \
	LINKSMART=YES \
	clean \
	default \
	gdb
%endif
#	%{?with_ide:installer_clean} \
#	%{?with_ide:installer_all}

%if %{with doc}
export save_size=10000
%{__make} -j1 -C fpcdocs \
	FPDOC=$NEWFPDOC \
	FPC="$NEWPP" \
	pdf
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir},%{_datadir}/fpcsrc,%{_examplesdir}/fpc}

cp -af fpc-src/* $RPM_BUILD_ROOT%{_datadir}/fpcsrc

NEWPP=`pwd`/fpcsrc/compiler/ppc%{_bname}
FPCMAKE=`pwd`/fpcsrc/utils/fpcm/fpcmake
%{__make} -j1 -C fpcsrc \
	compiler_distinstall \
	rtl_distinstall \
	packages_distinstall \
	%{?with_ide:ide_distinstall} \
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

%{__make} -j1 -C install/man installman \
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
%if %{with ide}
%{_libdir}/%{name}/%{version}/ide
%endif
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

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc fpcdocs/*.pdf
%endif
