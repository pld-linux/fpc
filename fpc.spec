Summary:	32-bit compiler for the i386 and m68k processors
Summary(pl):	32 bitowy kompilator dla procesorów i386 i m68k
Name:		fpc
Version:	0.99.12
Release:	1
Copyright:	GPL
Group:		Development/Languages
Group(pl):	Programowanie/Jêzyki
Vendor:		Michael Van Canneyt <michael@tfdec1.fys.kuleuven.ac.be>
Source0:	ftp://gdzies.w.be/pub/fpc/%{name}-%{version}.ELF.tar.gz
Source1:	fpc-sample.cfg
URL:		http://www.freepascal.org/
ExclusiveArch:	%{ix86} m68k
Buildroot:	/tmp/%{name}-%{version}-root

%description
Free Pascal is a 32-bit compiler for the i386 and m68k processors.
Free Pascal is designed to be, as much as possible, source compatible with
Turbo Pascal 7.0 and Delphi 4 (although this goal is not yet attained),
but it also enhances these languages with elements like function
overloading. And, unlike these ancestors, it supports multiple platforms.

%description -l pl
Free Pascal to 32 bitowy kompilator dla procesorów i386 oraz m86k.
Free Pascal zosta³ zaprojektowany by byæ (jak tylko to mo¿liwe)
kompatybilnym z Turbo Pascal 7.0 oraz Delphi 4. Free Pascal równie¿
rozszerza te jêzyki elementami takimi jak prze³adowywanie funkcji.

%package doc
Summary:        Free Pascal Compiler documentation
Summary(pl):    Dokumentacja do kompilatora Free Pascal
Group:          Documentation
Group(pl):      Dokumentacja
Requires:       %{name} = %{version}

%description doc
Documentation for fpc HTML format.

%description -l pl doc
Dokumentacja do fpc w formacie HTML.

%prep
%setup -q
mkdir sources && cd sources && tar -xzf ../sources.tar.gz \
	      && tar -xzf ../libs.tar.gz && tar -xzf ../bins.tar.gz \
	      && mkdir ../doc && cd ../doc && tar -xzf ../docs.tar.gz && cd ..

%build
cd sources
cp base/{Makefile,makefile.fpc} .

# Currently we don't have these extenstions
mkdir -p fcl/linux && echo ".PHONY:	all install" > fcl/linux/Makefile
mkdir -p gtk       && echo ".PHONY:     all install" > gtk/Makefile
mkdir -p api       && echo ".PHONY:     all install" > api/Makefile
mkdir -p fv        && echo ".PHONY:     all install" > fv/Makefile
mkdir -p gdbint    && echo ".PHONY:     all install" > gdbint/Makefile
mkdir -p ide       && echo ".PHONY:     all install" > ide/Makefile

if [ "%{_target_cpu}" = "m68k" ]; then
	CPU=M68K
else
	CPU=I386
fi
make \
	OPT="$RPM_OPT_FLAGS" \
	RELEASE=1 \
	BASEINSTALLDIR=%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=%{_bindir} \
	PP="`pwd`/ppc386" \
	all

%install
rm -rf $RPM_BUILD_ROOT

install -d              $RPM_BUILD_ROOT/etc/
install %{SOURCE1}      $RPM_BUILD_ROOT/etc/ppc386.cfg

cd sources && make \
	PP="`pwd`/ppc386" \
	BASEINSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/%{name}/%{version} \
	BININSTALLDIR=$RPM_BUILD_ROOT%{_bindir} \
	install

ln -sf %{_libdir}/%{name}/%{version}/ppc386 $RPM_BUILD_ROOT%{_bindir}/ppc386
strip $RPM_BUILD_ROOT%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
GCCSPEC=`(gcc -v 2>&1)| head -n 1| awk '{ print $4 } '`
GCCDIR=`dirname $GCCSPEC`
echo "Found libgcc.a in $GCCDIR"
sed -e "s#\$GCCDIR#$GCCDIR#" /etc/ppc386.cfg > /etc/ppc386.cfg.new
sed -e "s#\$1#%{_libdir}/%{name}/%{version}#" /etc/ppc386.cfg.new > /etc/ppc386.cfg
rm -f /etc/ppc386.cfg.new

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%config %verify(not md5 size mtime) %{_sysconfdir}/ppc386.cfg
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%{_libdir}/%{name}/%{version}/msg
%{_libdir}/%{name}/%{version}/rtl
%attr(755,root,root) %{_libdir}/%{name}/%{version}/ppc386

%files doc
%defattr(644,root,root,755)
%doc doc/*
