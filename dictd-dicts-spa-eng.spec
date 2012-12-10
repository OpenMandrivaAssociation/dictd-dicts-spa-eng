%define lang_from	spa
%define lang_to		eng
%define namesuffix	%{lang_from}-%{lang_to}
%define license		GPL
%define summary_prefix	Spanish - English
%define descr_prefix	%{summary_prefix}
%define src		ftp://ftp.dict.org/pub/dict/pre/www.freedict.de/20050319/%{lang_from}-%{lang_to}.tar.gz
%define dict_filename	%{namesuffix}
%define conf_file	%{_sysconfdir}/dictd.conf.d/%{name}

%define summ_desc_suf	Freedict dictionary for dictd

%define summary		%{summary_prefix} %{summ_desc_suf}
%define descr		%{descr_prefix} %{summ_desc_suf}
%define name		dictd-dicts-%{namesuffix}
%define version         0.1.0
%define release         %mkrel 15
%define group           Databases

%define __dictzip       %(which dictzip)
%define dictd_name      dictd
%define dictd_version   1.10.1-4

Summary:	%{summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	%{license}
Group:		%{group}
Source:		%{src}
URL:		http://www.freedict.de
Provides:	dictd-dicts-freedict-%{namesuffix}, dictd-dicts-%{namesuffix}
Obsoletes:	dictd-dicts-freedict-%{namesuffix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
BuildRequires:	%{dictd_name}-utils >= %{dictd_version}
Provides:	dictd-dictionary = %version-%release, dictd-dictionaries = %version-%release
Requires:	%{dictd_name}-server >= %{dictd_version}
Requires(post):	%{dictd_name}-server >= %dictd_version
Requires(postun):	%{dictd_name}-server >= %dictd_version

%description
%{descr}

%prep
%setup -c -q

%build
# dictzip the dict dictionary file, if it's not yet zipped
if ls *.dict >/dev/null 2>&1; then
	dictzip *.dict
fi

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_datadir}/dict
cp %{dict_filename}*dict* %{buildroot}%{_datadir}/dict
cp %{dict_filename}*index* %{buildroot}%{_datadir}/dict
%{__mkdir_p} %{buildroot}%{_sysconfdir}/dictd.conf.d
printf "database %%-10s\t{ data \"%{_datadir}/dict/%{dict_filename}.dict.dz\"\n" %{dict_filename} >> %{buildroot}%{conf_file}
printf "\t\t\t  index \"%{_datadir}/dict/%{dict_filename}.index\" }\n" >> %{buildroot}%{conf_file}

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/update-dictd.conf
echo "Restarting dictd-server, because configuration has been changed..."
service dictd-server reload

%postun
# XXX: control of package erasure ordering is only in rpm >= 4.4.8,
# this is a hack to not fail removal if dictd-server disappeared under our feet
if [ -x %{_sbindir}/update-dictd.conf ]; then
  %{_sbindir}/update-dictd.conf
  echo "Restarting dictd-server, because configuration has been changed..."
  service dictd-server reload
fi

%files
%defattr(644, root, root)
%{_datadir}/dict/%{dict_filename}*dict*
%{_datadir}/dict/%{dict_filename}*index*
%config		%conf_file




%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-15mdv2011.0
+ Revision: 617772
- the mass rebuild of 2010.0 packages

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 0.1.0-14mdv2010.0
+ Revision: 428219
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.1.0-13mdv2009.0
+ Revision: 244259
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.1.0-11mdv2008.1
+ Revision: 136364
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Dec 22 2006 Gustavo De Nardin <gustavodn@mandriva.com> 0.1.0-11mdv2007.0
+ Revision: 101185
- make use of update-dictd.conf scheme, introduced by dictd-1.10.1-4
- bump release of all dictd-dicts-* to 11, for proper upgrades
- BuildRequires only dictd-utils, for dictzip, not full dictd
- versioned provides of meta packages, for proper upgrades
- Requires only dictd-server, not full dictd
- Requires(post/postun) for proper order in install and removal
- introduce a hack to avoid being unremovable if dictd-server is removed
  before, even though the Requires(postun)
- Imported into SVN repo

