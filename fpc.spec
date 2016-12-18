#
# Conditional build:
%bcond_without	ide	# FPC IDE
%bcond_without	doc	# documentation

Summary:	Free Pascal - 32-bit Pascal compiler
Summary(pl.UTF-8):	Free Pascal - 32-bitowy kompilator języka Pascal
Summary(ru.UTF-8):	Свободный компилятор Pascal
Summary(uk.UTF-8):	Вільний компілятор Pascal
Name:		fpc
Version:	3.0.0
Release:	5
License:	GPL v2+
Group:		Development/Languages
Source0:	ftp://ftp.freepascal.org/pub/fpc/dist/%{version}/source/%{name}build-%{version}.tar.gz
# Source0-md5:	bb7d17ef5c7c007466368262c0779cb7
Source1:	ftp://ftp.freepascal.org/pub/fpc/dist/%{version}/i386-linux/%{name}-%{version}.i386-linux.tar
# Source1-md5:	41e0bcb7c11b7edf311142079ba2defa
Source2:	ftp://ftp.freepascal.org/pub/fpc/dist/%{version}/x86_64-linux/%{name}-%{version}.x86_64-linux.tar
# Source2-md5:	db2ae45b0d1846e01b61ba52f03e60b2
Patch0:		%{name}-skip-dev-dot.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-gdb.patch
Patch3:		fpc-r32374.patch
Patch4:		fpcdocs-r1260.patch
Patch5:		fpc-man.patch
URL:		http://www.freepascal.org/
BuildRequires:	binutils-devel >= 3:2.17.50
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.213
%if %{with ide}
BuildRequires:	babeltrace-devel
BuildRequires:	expat-devel
BuildRequires:	gdb-lib >= 7.2-7
BuildRequires:	guile-devel
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	libselinux-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%endif
%if %{with doc}
BuildRequires:	tetex-fonts-jknappen
BuildRequires:	tetex-format-pdflatex
BuildRequires:	tetex-makeindex
BuildRequires:	tetex-metafont
BuildRequires:	texlive-xetex
%endif
Requires:	binutils
Provides:	fpc-bootstrap
ExclusiveArch:	%{ix86} %{x8664}
# TODO:
# %{arm} ftp://ftp.freepascal.org/pub/fpc/dist/3.0.0/arm-linux/fpc-3.0.0.arm-linux-raspberry1wq.tar
# ppc64 ftp://ftp.freepascal.org/pub/fpc/dist/3.0.0/powerpc64-linux/fpc-3.0.0.powerpc64-linux.tar
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free Pascal is a 32-bit Pascal compiler. Free Pascal is designed to
be, as much as possible, source compatible with Turbo Pascal 7.0 and
Delphi 4 (although this goal is not yet attained), but it also
enhances these languages with elements like function overloading. And,
unlike these ancestors, it supports multiple platforms.

%description -l pl.UTF-8
Free Pascal to 32-bitowy kompilator języka Pascal. Free Pascal został
zaprojektowany by być (na ile to tylko możliwe) kompatybilnym z Turbo
Pascalem 7.0 oraz Delphi 4. Free Pascal również rozszerza te języki
elementami takimi jak przeciążanie funkcji.

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

%package ide
Summary:	Free Pascal IDE (integrated development environment)
Summary(pl.UTF-8):	Zintegrowane środowisko programistyczne (IDE) Free Pascala
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description ide
Free Pascal IDE (integrated development environment).

%description ide -l pl.UTF-8
Zintegrowane środowisko programistyczne (IDE) Free Pascala.

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
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p1

%ifarch %{ix86}
tar xf %{SOURCE1}
%define _bver %{version}
%define _bname 386
%define _barch i386
%endif
%ifarch %{x8664}
tar xf %{SOURCE2}
%define _bver %{version}
%define _bname x64
%define _barch x86_64
%endif
%ifarch %{arm}
%define _bver %{version}
%define _bname arm
%define _barch arm
%endif
%ifarch ppc
%define _bver ?
%define _bname ppc
%define _barch powerpc
%endif
%ifarch ppc64
%define _bver %{version}
%define _bname ppc64
%define _barch powerpc64
%endif
%ifarch sparc sparcv9
%define _bver ?
%define _bname sparc
%define _barch sparc
%endif

cd %{name}-%{version}.%{_barch}-linux
tar xf binary.*-linux.tar
cd ..

mkdir bin
cd bin
for i in ../%{name}-%{version}.%{_barch}-linux/*.tar.gz ; do
	tar xzf $i
done
ln -sf `pwd`/lib/%{name}/%{_bver}/ppc* bin
cd ..

find fpcsrc -name Makefile -o -name fpcmake.ini -o -name fpmkunit.pp | \
	xargs %{__sed} -i -e 's|/usr/lib/|%{_libdir}/|g'

# remove precompiled objects from fpc-src
%{__rm} fpcsrc/rtl/palmos/m68k/{libcrt.a,*.o}

# save for fpc-src
install -d fpc-src
cp -af fpcsrc/* fpc-src
rm -r fpc-src/{ide,tests}

%if 0%{?debug:1}
find fpcsrc -name Makefile | xargs %{__sed} -i -e 's/-Xs//'
%endif

%build
# use ld.bfd
[ -d our-ld ] || install -d our-ld
ln -sf %{_bindir}/ld.bfd our-ld/ld
export PATH=$(pwd)/our-ld:$PATH

PP=`pwd`/bin/lib/%{name}/%{_bver}/ppc%{_bname}
NEWPP=`pwd`/fpcsrc/compiler/ppc%{_bname}
NEWFPDOC=`pwd`/fpcsrc/utils/fpdoc/bin/%{_barch}-linux/fpdoc
DATA2INC=`pwd`/fpcsrc/utils/bin/%{_barch}-linux/data2inc

# DO NOT PUT $RPM_OPT_FLAGS IN OPT, IT DOES NOT WORK - baggins
case "%{_build_cpu}" in
	i386|i486) OPTF="-OG2p1" ;;
	i586) OPTF="-OG2p2" ;;
	i686|athlon|pentium3|pentium4|x86_64|amd64|ia32e) OPTF="-Og2p3" ;;
	*) OPTF="-O2" ;;
esac

%{__make} -C fpcsrc compiler_cycle \
	OPT="$OPTF %{!?debug:-Xs} -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	DATA2INC="$DATA2INC" \
	PP="$PP" \
	FPC="$PP" \
	LINKSMART=YES

%{__make} -C fpcsrc OPT="$OPTF %{!?debug:-Xs} -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	GDBLIBDIR=%{_libdir} \
	DATA2INC="$DATA2INC" \
	PP="$NEWPP" \
	FPC="$NEWPP" \
	FPDOC=$NEWFPDOC \
	LINKSMART=YES \
	NODOCS=YES \
	rtl_clean \
	packages_clean \
	utils_clean \
	%{?with_ide: ide_clean installer_clean} \
	rtl_all \
	packages_all \
	utils_all %{?with_ide:ide_all installer_all}

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
FPCMAKE=`pwd`/fpcsrc/utils/fpcm/bin/%{_barch}-linux/fpcmake
%{__make} -j1 -C fpcsrc \
	compiler_distinstall \
	rtl_distinstall \
	packages_distinstall \
	%{?with_ide:ide_distinstall} \
	utils_distinstall \
	PP="$NEWPP" \
	FPCMAKE="$FPCMAKE" \
	SMARTLINK=YES \
	FPCDIR=%{_libdir}/%{name}/%{version} \
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

ln -sf ../%{_lib}/%{name}/%{version}/ppc%{_bname} $RPM_BUILD_ROOT%{_bindir}

ln -sf %{_bindir}/ld.bfd $RPM_BUILD_ROOT%{_libdir}/%{name}/%{version}/ld

sh fpc-src/compiler/utils/samplecfg $RPM_BUILD_ROOT%{_libdir}/%{name}/%{version} $RPM_BUILD_ROOT%{_sysconfdir}
%{__sed} -i -e "s,$RPM_BUILD_ROOT,,g" $RPM_BUILD_ROOT%{_sysconfdir}/{*.cfg,fppkg/default}

%if "%{_lib}" != "lib"
%{__mv} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/lexyacc $RPM_BUILD_ROOT%{_libdir}/%{name}
%endif

# Fix examples, make seems to ignore INSTALL_EXAMPLEDIR
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/* $RPM_BUILD_ROOT%{_examplesdir}/fpc/

%ifnarch %{ix86}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/ppc386.1
%endif
%ifnarch %{arm}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/ppcarm.1
%endif
%ifnarch ppc ppc64
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/ppcppc.1
%endif
%ifnarch sparc sparcv9
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/ppcsparc.1
%endif
%ifnarch %{x8664}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/ppcx64.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bin2obj
%attr(755,root,root) %{_bindir}/chmcmd
%attr(755,root,root) %{_bindir}/chmls
%attr(755,root,root) %{_bindir}/cldrparser
%attr(755,root,root) %{_bindir}/data2inc
%attr(755,root,root) %{_bindir}/delp
%attr(755,root,root) %{_bindir}/fd2pascal
%attr(755,root,root) %{_bindir}/fpc*
%attr(755,root,root) %{_bindir}/fpdoc
%attr(755,root,root) %{_bindir}/fppkg
%attr(755,root,root) %{_bindir}/fprcp
%attr(755,root,root) %{_bindir}/grab_vcsa
%attr(755,root,root) %{_bindir}/h2pas
%attr(755,root,root) %{_bindir}/h2paspp
%attr(755,root,root) %{_bindir}/instantfpc
%attr(755,root,root) %{_bindir}/makeskel
%attr(755,root,root) %{_bindir}/mkarmins
%attr(755,root,root) %{_bindir}/mkinsadd
%attr(755,root,root) %{_bindir}/mkx86ins
%attr(755,root,root) %{_bindir}/pas2fpm
%attr(755,root,root) %{_bindir}/pas2jni
%attr(755,root,root) %{_bindir}/pas2ut
%attr(755,root,root) %{_bindir}/plex
%attr(755,root,root) %{_bindir}/postw32
%attr(755,root,root) %{_bindir}/ppc%{_bname}
%attr(755,root,root) %{_bindir}/ppdep
%attr(755,root,root) %{_bindir}/ppudump
%attr(755,root,root) %{_bindir}/ppufiles
%attr(755,root,root) %{_bindir}/ppumove
%attr(755,root,root) %{_bindir}/ptop
%attr(755,root,root) %{_bindir}/pyacc
%attr(755,root,root) %{_bindir}/rmcvsdir
%attr(755,root,root) %{_bindir}/rstconv
%attr(755,root,root) %{_bindir}/unihelper
%attr(755,root,root) %{_bindir}/unitdiff
# TODO: move the below files to data dir
# - JSON resources(?)
%{_bindir}/makeskel.rsj
%{_bindir}/ptop.rsj
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fpc.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fppkg.cfg
%dir %{_sysconfdir}/fppkg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fppkg/default
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/lexyacc
%{_libdir}/%{name}/%{version}/msg
%{_libdir}/%{name}/%{version}/units
%{_libdir}/%{name}/%{version}/fpmkinst
%{_libdir}/%{name}/lexyacc/*
%attr(755,root,root) %{_libdir}/%{name}/%{version}/ld
%attr(755,root,root) %{_libdir}/%{name}/%{version}/ppc%{_bname}
%attr(755,root,root) %{_libdir}/%{name}/%{version}/samplecfg
%{_mandir}/man1/bin2obj.1*
%{_mandir}/man1/chmcmd.1*
%{_mandir}/man1/chmls.1*
%{_mandir}/man1/data2inc.1*
%{_mandir}/man1/delp.1*
%{_mandir}/man1/fd2pascal.1*
%{_mandir}/man1/fp.1*
%{_mandir}/man1/fpc*.1*
%{_mandir}/man1/fpdoc.1*
%{_mandir}/man1/fppkg.1*
%{_mandir}/man1/fprcp.1*
%{_mandir}/man1/grab_vcsa.1*
%{_mandir}/man1/h2pas.1*
%{_mandir}/man1/h2paspp.1*
%{_mandir}/man1/makeskel.1*
%{_mandir}/man1/pas2fpm.1*
%{_mandir}/man1/pas2jni.1*
%{_mandir}/man1/pas2ut.1*
%{_mandir}/man1/plex.1*
%{_mandir}/man1/postw32.1*
%ifarch ppc64
%{_mandir}/man1/ppcppc.1*
%else
%{_mandir}/man1/ppc%{_bname}.1*
%endif
%{_mandir}/man1/ppdep.1*
%{_mandir}/man1/ppudump.1*
%{_mandir}/man1/ppufiles.1*
%{_mandir}/man1/ppumove.1*
%{_mandir}/man1/ptop.1*
%{_mandir}/man1/pyacc.1*
%{_mandir}/man1/rmcvsdir.1*
%{_mandir}/man1/rstconv.1*
%{_mandir}/man1/unitdiff.1*
%{_mandir}/man5/fpc.cfg.5*
%{_mandir}/man5/fpcmake.5*
%{_mandir}/man5/ptop.cfg.5*

%if %{with ide}
%files ide
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fp
# TODO: move the below files to data dir
# - ANSI art file used by fp binary
%{_bindir}/fp.ans
# - IDE command templates
%{_bindir}/cvsco.tdf
%{_bindir}/cvsdiff.tdf
%{_bindir}/cvsup.tdf
%{_bindir}/grep.tdf
%{_bindir}/tpgrep.tdf
# - Pascal code skeletons
%{_bindir}/gplprog.pt
%{_bindir}/gplunit.pt
%{_bindir}/program.pt
%{_bindir}/unit.pt
%{_libdir}/%{name}/%{version}/ide
%endif

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
