Name:           nova-db-clean
Version:        0.1
Release:        1
Summary:        Cleanup tool for OpenStack Nova Service
Group:          Development/Languages/Python
License:        GNU LGPL v2.1
URL:            http://www.griddynamics.com/openstack
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       python-nova

%description
This package contains simple script to cleanup database.
It removes records of deleted data.

%prep
%setup -q -n %{name}-%{version}

%install
rm -rf %{buildroot}
install -p -D -m 755 nova-db-clean.py %{buildroot}%{_sysconfdir}/cron.daily/nova-db-clean

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/cron.daily/nova-db-clean
%doc README

%changelog
