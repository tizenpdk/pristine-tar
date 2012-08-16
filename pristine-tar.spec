Name:       pristine-tar
Summary:    Regenerate pristine tarballs
Version:    1.25
Release:    0
Group:      Development/Tools/Building
License:    GPLv2
URL:        http://kitenet.net/~joey/code/pristine-tar/
Source0:    %{name}_%{version}.tar.gz
Requires:   gzip
Requires:   bzip2
Requires:   git
Requires:   perl-base
Requires:   xdelta
BuildRequires:  pkgconfig(zlib)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  fdupes
AutoProv:   no


%description
pristine-tar can regenerate a pristine upstream tarball using only a small
binary delta file and a copy of the source which can be a revision control
checkout.

The package also includes a pristine-gz command, which can regenerate a
pristine .gz file, and a pristine-bz2 for .bz2 files.

The delta file is designed to be checked into revision control along-side the
source code, thus allowing the original tarball to be extracted from revision
control.



%prep
%setup -q -n %{name}

%build
perl Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix}

make %{?jobs:-j%jobs}



%install
rm -rf %{buildroot}

%make_install

find %{buildroot}/usr/lib/zgz/ -name '*.a' | xargs rm
%fdupes -s %{buildroot}/usr/lib/zgz/


%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir /usr/lib/zgz/
/usr/lib/zgz/*
%{perl_vendorlib}/*
%{perl_archlib}/*
%{_mandir}/man1/*.gz
%doc debian/changelog debian/copyright delta-format.txt TODO GPL
%exclude %{perl_vendorarch}

