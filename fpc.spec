Summary:	32-bit compiler for the i386 and m68k processors
Summary(pl):	32 bitowy kompilator dla procesorów i386 i m68k
Name:		fpc
Version:	1.00
Release:	1
License:	GPL
Group:		Development/Languages
Group(pl):	Programowanie/Jêzyki
Vendor:		Michael Van Canneyt <michael@tfdec1.fys.kuleuven.ac.be>
Source0:	ftp://ftp.freepascal.org/pub/fpc/dist/Linux/%{name}-%{version}.ELF.tar
Source1:	fpc-sample.cfg
URL:		http://www.freepascal.org/
ExclusiveArch:	%{ix86} m68k
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free Pascal is a 32-bit compiler for the i386 and m68k processors.
Free Pascal is designed to be, as much as possible, source compatible
with Turbo Pascal 7.0 and Delphi 4 (although this goal is not yet
attained), but it also enhances these languages with elements like
function overloading. And, unlike these ancestors, it supports
multiple platforms.

%description -l pl
Free Pascal to 32 bitowy kompilator dla procesorów i386 oraz m86k.
Free Pascal zosta³ zaprojektowany by byæ (jak tylko to mo¿liwe)
kompatybilnym z Turbo Pascal 7.0 oraz Delphi 4. Free Pascal równie¿
rozszerza te jêzyki elementami takimi jak prze³adowywanie funkcji.

%package examples
Summary:	Free Pascal Compiler exaple programs
Summary(pl):	Przyk³adowe programy do kompilatora Free Pascal
Group:		Documentation
Group(pl):	Dokumentacja
Requires:	%{name} = %{version}

%description examples
Free Pascal Compiler exaple programs.

%description -l pl examples
Przyk³adowe programy do kompilatora Free Pascal.

%package doc
Summary:	Free Pascal Compiler documentation
Summary(pl):	Dokumentacja do kompilatora Free Pascal
Group:		Documentation
Group(pl):	Dokumentacja
Requires:	%{name} = %{version}

%description doc
Documentation for fpc in PDF format.

%description -l pl doc
Dokumentacja do fpc w formacie PDF.

%prep
%setup -q -c
tar xf sources.tar
tar xf binary.tar

for i in *.tar.gz ; do
	tar xzf $i
done

mkdir -p src/%{name}-%{version}/doc
mv doc/%{name}-%{version}/* src/%{name}-%{version}/doc
mkdir -p src/%{name}-%{version}/man && echo ".PHONY:	all install installman" > src/%{name}-%{version}/man/Makefile

%build
PP=`pwd`/lib/fpc/%{version}/ppc386

if [ "%{_target_cpu}" = "m68k" ]; then
	CPU=M68K
else
	CPU=I386
fi

# DO NOT PUT $RPM_OPT_FLAGS IN OPT, IT DOES NOT WORK - baggins
%{__make} -C src/%{name}-%{version} \
	OPT="-O2" \
	RELEASE=1 \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	PP="$PP" \
	all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir},%{_examplesdir}/fpc}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ppc386.cfg

PP=`pwd`/src/fpc-%{version}/compiler/ppc386
make -C src/%{name}-%{version} \
	PREFIXINSTALLDIR=$RPM_BUILD_ROOT%{_prefix} \
	PP="$PP" \
	install

cp -a man/* $RPM_BUILD_ROOT%{_mandir}
cp -a src/%{name}-%{version}/doc/examples/* $RPM_BUILD_ROOT%{_examplesdir}/fpc

ln -sf ../lib/%{name}/%{version}/ppc386 $RPM_BUILD_ROOT%{_bindir}/ppc386

strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/*
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/%{name}/%{version}/ppc386

gzip -9nf src/%{name}-%{version}/doc/{copying*,*.txt} \
	$RPM_BUILD_ROOT%{_mandir}/man*/*

mv -f src/%{name}-%{version}/doc/faq.htm src/%{name}-%{version}/doc/faq.html

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
GCCSPEC=`(gcc -v 2>&1)| head -n 1| awk '{ print $4 } '`
GCCDIR=`dirname $GCCSPEC`
echo "Found libgcc.a in $GCCDIR"
sed -e "s#\$GCCDIR#$GCCDIR#" %{_sysconfdir}/ppc386.cfg > %{_sysconfdir}/ppc386.cfg.new
sed -e "s#\$1#%{_libdir}/%{name}/%{version}#" %{_sysconfdir}/ppc386.cfg.new > %{_sysconfdir}/ppc386.cfg
rm -f %{_sysconfdir}/ppc386.cfg.new

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%doc src/%{name}-%{version}/doc/{copying*,*.txt}.gz
%doc src/%{name}-%{version}/doc/faq.html
%config %verify(not md5 size mtime) %{_sysconfdir}/ppc386.cfg
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/lexyacc
%{_libdir}/%{name}/%{version}/msg
%{_libdir}/%{name}/%{version}/units
%{_libdir}/%{name}/lexyacc/*
%attr(755,root,root) %{_libdir}/%{name}/%{version}/ppc386
%attr(755,root,root) %{_libdir}/%{name}/%{version}/samplecfg
%{_mandir}/man*/*

%files examples
%defattr(644,root,root,755)
%doc %{_examplesdir}/fpc

%files doc
%defattr(644,root,root,755)
%doc src/%{name}-%{version}/doc/*.pdf
