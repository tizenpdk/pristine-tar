Name:       pristine-tar
Summary:    Regenerate pristine tarballs
Version:    1.34
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
Patch4:     0005-pristine-gz-obey-the-XDELTA_PROGRAM-build-parameter.patch
#Patch5:     0006-Add-.gbp.conf.patch
Patch6:     0007-Use-posix-tar-format-by-default.patch
Patch7:     0008-Mangle-PAX-headers-when-using-posix-tar-format.patch
Patch8:     0009-HACK-workaround-for-some-broken-pristine-tar-branche.patch
Requires:   tar
Requires:   gzip
Requires:   bzip2
%if 0%{?suse_version} >= 1210
Recommends: pbzip2
%else
Requires:   pbzip2
%endif
Requires:   git
%if 0%{?suse_version}
Requires:   perl-base
%else
Requires:   perl
%endif
%if 0%{?fedora} || 0%{?centos_ver} >= 7
Requires:   xdelta
%else
Requires:   xdelta3
%endif
BuildRequires:  pkgconfig(zlib)

%if 0%{?suse_version} >= 1320
#BuildRequires:  perl(ExtUtils::MakeMaker)
%else
BuildRequires:  perl(ExtUtils::MakeMaker)
%endif
%if 0%{?suse_version}
BuildRequires:  fdupes
%endif

# Need to define these manually because otherwise rpmbuild makes the package
# provide libbz2.so which breaks building of other tools
AutoProv:   no
Provides: tizen-pristine-tar = 20160517
Provides: perl(Pristine::Tar)
Provides: perl(Pristine::Tar::Delta)
Provides: perl(Pristine::Tar::Delta::Tarball)
Provides: perl(Pristine::Tar::Formats)


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
# 0002-openSUSE-HACK-add-upstream-bzip2-v1.0.6-sources.patch
%if 0%{?suse_version} && 0%{?suse_version} < 1220
%patch1 -p1
%endif
# 0003-openSUSE-HACK-modify-Makefile-in-upstream-bzip2.patch
%if 0%{?suse_version} && 0%{?suse_version} < 1220
%patch2 -p1
%endif
# 0004-openSUSE-HACK-enable-special-upstream-bzip2.patch
%if 0%{?suse_version} && 0%{?suse_version} < 1220
%patch3 -p1
%endif
# 0005-pristine-gz-obey-the-XDELTA_PROGRAM-build-parameter.patch
%patch4 -p1
# 0006-Add-.gbp.conf.patch
#%patch5 -p1
# 0007-Use-posix-tar-format-by-default.patch
%patch6 -p1
# 0008-Mangle-PAX-headers-when-using-posix-tar-format.patch
%patch7 -p1
# 0009-HACK-workaround-for-some-broken-pristine-tar-branche.patch
%patch8 -p1

%build
%if 0%{?fedora} || 0%{?centos_ver} >= 7
%define makemaker_extraopts XDELTA_PROGRAM=xdelta
%endif
perl Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix} %{?makemaker_extraopts}

make %{?jobs:-j%jobs}



%install
rm -rf %{buildroot}
%make_install

find %{buildroot}/usr/lib/pristine-tar/ -name '*.a' | xargs rm

# Run fdupes if building in openSUSE
%if 0%{?suse_version}
%fdupes -s %{buildroot}/usr/lib/pristine-tar/
%endif



%files
%defattr(-,root,root,-)
%{_bindir}/*
/usr/lib/pristine-tar
%{perl_vendorlib}/*
%{perl_archlib}/*
%{_mandir}/man1/*.gz
%doc debian/changelog debian/copyright delta-format.txt TODO GPL
%exclude %{perl_vendorarch}

