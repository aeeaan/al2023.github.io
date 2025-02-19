%define _trivial .0
%define _buildid .2

# Note that the function of bootstrap is that it disables the test suite and whl
#   bcond_with bootstrap = tests enabled, package with whl created
%bcond_with bootstrap

%if 0%{?amzn}
%bcond_with tests
%endif

%global pypi_name wheel
%global python_wheelname %{pypi_name}-%{version}-py2.py3-none-any.whl
%global python_wheeldir %{_datadir}/python-wheels

Name:           python2-%{pypi_name}
Version:        0.34.2
Release:        1%{?dist}%{?_trivial}%{?_buildid}
Epoch:          1
Summary:        Built-package format for Python

License:        MIT
URL:            https://github.com/pypa/wheel
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

# Amazon Patches
# Fix CVE-2022-40898
# Patch from https://github.com/pypa/wheel/commit/88f02bc335d5404991e532e7f3b0fc80437bf4e0
Patch1000:      Fixed_potential_DoS_attack_via_WHEEL_INFO_RE.patch

%if ! %{with bootstrap}
# several tests compile extensions
# those tests are skipped if gcc is not found
BuildRequires:  gcc
%endif

%{?python_enable_dependency_generator}

%global _description \
A built-package format for Python.\
\
A wheel is a ZIP-format archive with a specially formatted filename and the\
.whl extension. It is designed to contain all the files for a PEP 376\
compatible install in a way that is very close to the on-disk format.

%description %{_description}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if ! %{with bootstrap}
%if %{with tests}
BuildRequires:  python2-pytest
%endif
%endif
%{?python_provide:%python_provide python2-%{pypi_name}}
Conflicts:      python-%{pypi_name} < %{version}-%{release}

%description -n python2-%{pypi_name} %{_description}

Python 2 version.

%if %{without bootstrap}
%package wheel
Summary:        The Python wheel module packaged as a wheel

%description wheel
A Python wheel of wheel to use with virtualenv.
%endif


%prep
%autosetup -n %{pypi_name}-%{version} -p1


%build
%py2_build

#%if %{without bootstrap}
#%py3_build_wheel
#%endif


%install
%py2_install
mv %{buildroot}%{_bindir}/%{pypi_name}{,-%{python2_version}}
ln -s %{pypi_name}-%{python2_version} %{buildroot}%{_bindir}/%{pypi_name}-2
#ln -s %{pypi_name}-2 %{buildroot}%{_bindir}/%{pypi_name}

%if %{without bootstrap}
mkdir -p %{buildroot}%{python_wheeldir}
install -p dist/%{python_wheelname} -t %{buildroot}%{python_wheeldir}

#remove unversioned file
rm %{buildroot}%{_bindir}/%{pypi_name}

%check
rm setup.cfg
%if %{with tests}
%if %{with python2}
PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-2 -v --ignore build
%endif
PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-3 -v --ignore build
%endif
%endif # with tests

%files -n python2-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{_bindir}/%{pypi_name}-2
%{_bindir}/%{pypi_name}-%{python2_version}
%{python2_sitelib}/%{pypi_name}*

%if %{without bootstrap}
%files wheel
%license LICENSE.txt
# we own the dir for simplicity
%dir %{python_wheeldir}/
%{python_wheeldir}/%{python_wheelname}
%endif

%changelog
* Wed Jul 31 2024 Joshua Rusch <jdr@unsend.cc> - 1:0.34.2-1.amzn2023.0.2
- Strip out python 3 builds

* Mon Nov 20 2023 Sai Harsha <ssuryad@amazon.com> - 1:0.34.2-1.amzn2.0.2
- Fix CVE-2022-40898

* Thu Apr 22 2021 Jian Zheng <zhejan@amazon.com> - 1:0.34.2-1
- Update to 0.34.2

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.33.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1:0.33.1-2
- Make /usr/bin/wheel Python 3

* Mon Feb 25 2019 Charalampos Stratakis <cstratak@redhat.com> - 1:0.33.1-1
- Update to 0.33.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 30 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.32.0-1
- Update to 0.32.0

* Wed Aug 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.31.1-3
- Create python-wheel-wheel package with the wheel of wheel

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:0.31.1-1
- Update to 0.31.1

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.30.0-3
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.30.0-2
- Bootstrap for Python 3.7

* Fri Feb 23 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:0.30.0-1
- Update to 0.30.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0a0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 29 2017 Tomas Orsava <torsava@redhat.com> - 0.30.0a0-8
- Switch macros to bcond's and make Python 2 optional to facilitate building
  the Python 2 and Python 3 modules

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0a0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0a0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-5
- Enable tests

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-4
- Rebuild for Python 3.6 without tests

* Tue Dec 06 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.30.0a0-3
- Add bootstrap method

* Mon Sep 19 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-2
- Use the python_provide macro

* Mon Sep 19 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-1
- Update to 0.30.0a0
- Added patch to remove keyrings.alt dependency

* Wed Aug 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.29.0-1
- Update to 0.29.0
- Cleanups and fixes

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 0.26.0-1
- Update to 0.26.0
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 13 2015 Slavek Kabrda <bkabrda@redhat.com> - 0.24.0-3
- Make spec buildable in EPEL 6, too.
- Remove additional sources added to upstream tarball.

* Sat Jan 03 2015 Matej Cepl <mcepl@redhat.com> - 0.24.0-2
- Make python3 conditional (switched off for RHEL-7; fixes #1131111).

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.24.0-1
- Update to 0.24.0
- Remove patches merged upstream

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-3
- Another rebuild with python 3.4

* Fri Apr 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-2
- Rebuild with python 3.4

* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.
