# TODO: 
# - check why it builds all static..
Summary:	32-bit compiler for the i386 and m68k processors
Summary(pl):	32 bitowy kompilator dla procesorСw i386 i m68k
Summary(ru):	Свободный компилятор Pascal
Summary(uk):	В╕льний комп╕лятор Pascal
Name:		fpc
Version:	2.0.0
Release:	1
License:	GPL
Group:		Development/Languages
Vendor:		Michael Van Canneyt <michael@tfdec1.fys.kuleuven.ac.be>
Source0:	http://switch.dl.sourceforge.net/sourceforge/freepascal/%{name}-%{version}.source.tar.gz
# Source0-md5:	3f9c64d0146a3631f6963fd7477776d1
Source1:	http://dl.sourceforge.net/freepascal/fpc-%{version}.i386-linux.tar
# Source1-md5:	5f0a5fba632a811dcfdafe0ff80476a3
Source2:	http://dl.sourceforge.net/freepascal/fpc-%{version}.x86_64-linux.tar
# Source2-md5:	36270de604c6b5ad3af8aaa08143e88f
Source3:	http://dl.sourceforge.net/freepascal/fpc-%{version}.powerpc-linux.tar
# Source3-md5:	7019384e09411902e530dfe55d4ff145
Source4:	http://dl.sourceforge.net/freepascal/%{name}-%{version}.sparc-linux.tar
# Source4-md5:	dd8925ce8ce93309456c3072e6e4d14d
URL:		http://www.freepascal.org/
BuildRequires:	ncurses-devel
BuildRequires:	gpm-devel
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	tetex-fonts-jknappen
BuildRequires:	tetex-format-pdflatex
BuildRequires:	tetex-metafont
Requires:	binutils
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
FPC -- 32-битный компилятор Pascal, совместимый с Turbo Pascal 7.0 и Delphi.
Поставляется с RTL (библиотекой времени исполнения), FCL (библиотекой свободных
компонент), интерфейсами к gtk, ncurses, zlib, mysql, postgres, ibase.

%description -l uk
FPC -- 32-б╕тний комп╕лятор Pascal, сум╕сний ╕з Turbo Pascal 7.0 та Delphi.
Постача╓ться ╕з RTL (б╕бл╕отекою часу виконання), FCL (б╕бл╕отекою в╕льних
компонент), ╕нтерфейсами до gtk, ncurses, zlib, mysql, postgres, ibase.

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
%setup -q -n %{name}
%ifarch %{ix86}
tar xf %{SOURCE1}
%define _bname 386
%endif
%ifarch %{x8664}
tar xf %{SOURCE2}
%define _bname x64
%endif
%ifarch ppc
tar xf %{SOURCE3}
%define _bname ppc
%endif
%ifarch sparc
tar xf %{SOURCE4}
%define _bname sparc
%endif

tar xf binary.*-linux.tar

mkdir bin
cd bin
for i in ../*.tar.gz ; do
	tar xzf $i
done
ln -sf `pwd`/lib/%{name}/%{version}/ppc* bin

%build
PP=`pwd`/bin/lib/%{name}/%{version}/ppc%{_bname}
NEWPP=`pwd`/compiler/ppc%{_bname}
NEWFPDOC=`pwd`/utils/fpdoc/fpdoc

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

%{__make} compiler_cycle \
	OPT="$OPTF -Xs -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	PP="$PP" \
	FPC="$PP" \
	SMARTLINK=YES

%{__make} OPT="$OPTF -Xs -n" \
	RELEASE="1" \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
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
%{__make} -C docs pdf \
	FPDOC=$NEWFPDOC \
	FPC="$NEWPP"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir},%{_examplesdir}/fpc}

NEWPP=`pwd`/compiler/ppc%{_bname}
FPCMAKE=`pwd`/utils/fpcm/fpcmake
%{__make} \
	compiler_distinstall \
	rtl_distinstall \
	fcl_distinstall \
	fv_distinstall \
	packages_distinstall \
	ide_distinstall \
	utils_distinstall \
	man_install \
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

ln -sf %{_libdir}/%{name}/%{version}/ppc%{_bname} $RPM_BUILD_ROOT%{_bindir}

sh compiler/utils/samplecfg %{_libdir}/%{name}/%{version} $RPM_BUILD_ROOT%{_sysconfdir}

cp -f install/doc/faq.htm faq.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%doc faq.html install/doc/{copying*,*.txt} ide/readme.ide
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/fpc.cfg
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

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/fpc

%files doc
%defattr(644,root,root,755)
%doc docs/*.pdf
