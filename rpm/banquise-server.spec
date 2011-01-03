Name:		banquise-server
Version:	0.5
Release:	8%{?dist}
License:	GPLv3
Group:		System
Summary:	Server of banquise package system
URL:		http://www.lefred.be
Packager:	Frederic Descamps
Source0:	%{name}-%{version}.tgz
Source1:	%{name}.conf
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	python, yum, Django, Django-south, MySQL-python, mod_python   
%if 0%{?fedora} > 1
Requires:       django-dajax python24-django-dajaxice
%else
Patch0:         views.centos.patch
Patch1:         django1.1_views.patch
Requires:       python-uuid, python-json
Requires:       python27-django-dajax python27-django-dajaxice
%endif


%description
Sever part of the banquise project

%prep
%setup  
%if 0%{?fedora} > 1
%else
%patch0
%patch1
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
mkdir -p $RPM_BUILD_ROOT/var/www/banquise/
install -m 644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf
cp -rv * $RPM_BUILD_ROOT/var/www/banquise/
cp -rv settings_example.py $RPM_BUILD_ROOT/var/www/banquise/settings.py
cp -rv urls_example.py $RPM_BUILD_ROOT/var/www/banquise/urls.py
rm -rf $RPM_BUILD_ROOT/var/www/banquise/rpm


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/var/www/banquise/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) /var/www/banquise/settings.py
%config(noreplace) /var/www/banquise/urls.py


%changelog
* Tue Dec 28 2010 - Frederic Descamps <lefred@inuits.be> 0.5-8
- version 0.5-8 draft of history package added 
* Mon Nov 15 2010 - Frederic Descamps <lefred@inuits.be> 0.5-7
- version 0.5-7 git version and django 1.1.x support
* Thu Apr 15 2010 - Frederic Descamps <lefred@inuits.be> 0.5-6
- version 0.5-6 adding missing table in migration
* Thu Feb 18 2010 - Frederic Descamps <lefred@inuits.be> 0.5-5
- version 0.5-5 metabug info added and memory usage optimized
* Thu Feb 18 2010 - Frederic Descamps <lefred@inuits.be> 0.5-4
- version 0.5-4 adding metadata
* Mon Feb 15 2010 - Frederic Descamps <lefred@inuits.be> 0.5-3
- package for 0.5 - new package, some bugs were resolved in banquise
* Fri Feb 12 2010 - Frederic Descamps <lefred@inuits.be> 0.5-2
- package for 0.5 - keep configurtation
* Thu Feb 11 2010 - Frederic Descamps <lefred@inuits.be> 0.5-1 
- package for 0.5 - fedora specific package
* Tue Jan 12 2010 - Frederic Descamps <lefred@inuits.be> 0.4-2 
- package for 0.4 - fedora specific package
* Mon Jan 11 2010 - Frederic Descamps <lefred@inuits.be> 0.4-1 
- package for 0.4 - adding repo and install new packages
* Sun Jan 10 2010 - Frederic Descamps <lefred@inuits.be> 0.3-1 
- package for 0.3
* Sun Jan 10 2010 - Frederic Descamps <lefred@inuits.be> 0.2-1 
- package for 0.2
* Sat Jan 09 2010 - Frederic Descamps <lefred@inuits.be> 0.1-1 
- Initial build
