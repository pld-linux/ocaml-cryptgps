#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Ocaml Blowfish, DES, and 3DES implementation
Summary(pl.UTF-8):	Implementacja Blowfish, DES, and 3DES w Ocamlu
Name:		ocaml-cryptgps
Version:	0.2.1
Release:	5
License:	MIT/X11
Group:		Libraries
Source0:	http://download.camlcity.org/download/cryptgps-%{version}.tar.gz
# Source0-md5:	656afb40fa681079296551b546cb02df
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library implements the symmetric cryptographic algorithms
Blowfish, DES, and 3DES. The algorithms are written in O'Caml,
i.e. this is not a binding to some C library, but the implementation
itself. 
This package contains files needed to run bytecode executables using
cryptgps library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki cryptgps.

%package devel
Summary:	Ocaml Blowfish, DES, and 3DES implementation - development part
Summary(pl.UTF-8):	Implementacja Blowfish, DES, and 3DES w Ocamlu - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml

%description devel
This library implements the symmetric cryptographic algorithms
Blowfish, DES, and 3DES. The algorithms are written in O'Caml,
i.e. this is not a binding to some C library, but the implementation
itself. 
This package contains files needed to develop OCaml programs using
cryptgps library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki cryptgps.

%prep
%setup -q -n cryptgps

%build
%{__make} all %{?with_ocaml_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{,site-lib/}cryptgps

install *.cm[ix] $RPM_BUILD_ROOT%{_libdir}/ocaml/cryptgps
%if %{with ocaml_opt}
install *.cmxa *.a $RPM_BUILD_ROOT%{_libdir}/ocaml/cryptgps
%endif

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cryptgps
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cryptgps/META <<EOF
requires = "bigarray"
version = "%{version}"
directory = "+cryptgps"
archive(byte) = "cryptgps.cma"
archive(native) = "cryptgps.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE *.mli
%dir %{_libdir}/ocaml/cryptgps
%{_libdir}/ocaml/cryptgps/*.cm[xi]
%if %{with ocaml_opt}
%{_libdir}/ocaml/cryptgps/*.a
%{_libdir}/ocaml/cryptgps/*.cmxa
%endif
%{_libdir}/ocaml/site-lib/cryptgps
