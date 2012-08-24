Name:       pristine-tar
Summary:    Regenerate pristine tarballs
Version:    1.25
Release:    0
Group:      Development/Tools/Building
License:    GPLv2
URL:        http://kitenet.net/~joey/code/pristine-tar/
Source0:    %{name}_%{version}.tar.gz
# Patches auto-generated by git-buildpackage:
Patch0:     0001-Fix-libbz2.so-version-numbers.patch
Patch1:     0002-openSUSE-HACK-add-upstream-bzip2-v1.0.6-sources.patch
Patch2:     0003-openSUSE-HACK-modify-Makefile-in-upstream-bzip2.patch
Patch3:     0004-openSUSE-HACK-enable-special-upstream-bzip2.patch
Requires:   gzip
Requires:   bzip2
Requires:   git
Requires:   perl-base
Requires:   xdelta
BuildRequires:  pkgconfig(zlib)
BuildRequires:  perl(ExtUtils::MakeMaker)
%if 0%{?suse_version}
BuildRequires:  fdupes
%endif
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
# 0001-Fix-libbz2.so-version-numbers.patch
%patch0 -p1
%if 0%{?suse_version}
# 0002-openSUSE-HACK-add-upstream-bzip2-v1.0.6-sources.patch
%patch1 -p1
# 0003-openSUSE-HACK-modify-Makefile-in-upstream-bzip2.patch
%patch2 -p1
# 0004-openSUSE-HACK-enable-special-upstream-bzip2.patch
%patch3 -p1
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix}

make %{?jobs:-j%jobs}



%install
rm -rf %{buildroot}

%make_install

find %{buildroot}/usr/lib/zgz/ -name '*.a' | xargs rm

# Run fdupes if building in openSUSE
%if 0%{?suse_version}
%fdupes -s %{buildroot}/usr/lib/zgz/
%endif


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

