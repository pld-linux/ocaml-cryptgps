#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Ocaml Blowfish, DES, and 3DES implementation
Summary(pl.UTF-8):	Implementacja Blowfish, DES, and 3DES w Ocamlu
Name:		ocaml-cryptgps
Version:	0.2.1
Release:	6
License:	MIT
Group:		Libraries
Source0:	http://download.camlcity.org/download/cryptgps-%{version}.tar.gz
# Source0-md5:	656afb40fa681079296551b546cb02df
Patch0:		%{name}-bytes.patch
URL:		http://projects.camlcity.org/projects/cryptgps.html
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
Conflicts:	ocaml-cryptgps-devel < 0.2.1-6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
This library implements the symmetric cryptographic algorithms
Blowfish, DES, and 3DES. The algorithms are written in O'Caml,
i.e. this is not a binding to some C library, but the implementation
itself. 

This package contains files needed to run bytecode executables using
cryptgps library.

%description -l pl.UTF-8
Biblioteka implementuje algorytmy szyfrów symetrycznych Blowfish, DES
oraz 3DES. Algorytmy zostały napisane w OCamlu, więc nie jest to
wiązanie do biblioteki w C, ale sama implementacja.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki cryptgps.

%package devel
Summary:	Ocaml Blowfish, DES, and 3DES implementation - development part
Summary(pl.UTF-8):	Implementacja Blowfish, DES, and 3DES w Ocamlu - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
cryptgps library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki cryptgps.

%prep
%setup -q -n cryptgps
%patch0 -p1

%build
%{__make} all %{?with_ocaml_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/cryptgps

cp -p META *.cm[ai] *.mli $RPM_BUILD_ROOT%{_libdir}/ocaml/cryptgps
%if %{with ocaml_opt}
cp -p *.cmx* *.a $RPM_BUILD_ROOT%{_libdir}/ocaml/cryptgps
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%dir %{_libdir}/ocaml/cryptgps
%{_libdir}/ocaml/cryptgps/META
%{_libdir}/ocaml/cryptgps/*.cma

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/cryptgps/*.cmi
%{_libdir}/ocaml/cryptgps/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/cryptgps/*.a
%{_libdir}/ocaml/cryptgps/*.cmx
%{_libdir}/ocaml/cryptgps/*.cmxa
%endif
