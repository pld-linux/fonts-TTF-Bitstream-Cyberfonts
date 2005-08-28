#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
Summary:	Bitstream Cyberfonts True Type font
Summary(pl):	Font True Type Cyberfonts firmy Bitstream
%define		base_name		fonts-TTF-Bitstream-Cyberfonts
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	1.0
Release:	2%{?with_license_agreement:wla}
License:	Nondistributable but free (See Bitstream-Cyberfonts-licence.txt)
Group:		Fonts
%if %{with license_agreement}
# also at http://dl.sourceforge.net/corefonts/
Source0:	ftp://ftp.netscape.com/pub/communicator/extras/fonts/windows/Cyberbit.ZIP
# NoSource0-md5: 63a6f607ac5a78d34b67247b893faf5b
Source1:	ftp://ftp.netscape.com/pub/communicator/extras/fonts/windows/Cyberbase.ZIP
# NoSource1-md5: 63a6f607ac5a78d34b67247b893faf5b
Source2:	ftp://ftp.netscape.com/pub/communicator/extras/fonts/windows/CyberCJK.ZIP
# NoSource2-md5: 63a6f607ac5a78d34b67247b893faf5b
BuildRequires:	unzip
# we need the -installer package as otherwise can't make end-user
# package to work. see also comments in %%prep section.
BuildRequires:	%{base_name}-installer
Requires:	%{_fontsdir}/TTF
Requires(post,postun):	fontpostinst
%else
Source0:	license-installer.sh
Source1:	%{base_name}-licence.txt
Requires:	unzip
Requires:	rpm-build-tools
Requires:	wget
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Bitstream Cyberfonts True Type font.
%if %{without license_agreement}
License issues made us not to include inherent files into this package
by default. If you want to
create full working package please build it with one of the following
command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%description -l pl
Font True Type Cyberfonts firmy Bitstream.
%if %{without license_agreement}
Kwestie licencji zmusi³y nas do niedo³±czania do tego pakietu istotnych
plików. Je¶li chcesz stworzyæ
w pe³ni funkcjonalny pakiet, zbuduj go za pomoc± polecenia:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%prep
%if %{with license_agreement}
%setup -q -c -T
/usr/bin/unzip -L %{SOURCE0}
/usr/bin/unzip -L %{SOURCE1}
/usr/bin/unzip -L %{SOURCE2}
# ugly hack, to work with -installer package, when it may not fetch this file
# from CVS with builder (-nc, -ncs)
install %{_datadir}/%{base_name}/Bitstream-Cyberfonts-licence.txt .
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@LICENSE@,%{_datadir}/%{base_name}/Bitstream-Cyberfonts-licence.txt,
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{base_name}/Bitstream-Cyberfonts-licence.txt
%else
install -d $RPM_BUILD_ROOT%{ttffontsdir}
install *.ttf $RPM_BUILD_ROOT%{ttffontsdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with license_agreement}
%post
fontpostinst TTF

%postun
fontpostinst TTF

%else
%pre
echo "
If you accept the license enclosed in the file
%{_datadir}/%{base_name}/Bitstream-Cyberfonts-licence.txt
and want to install real fonts, then rebuild the package with the
following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
%endif

%files
%defattr(644,root,root,755)
%if %{with license_agreement}
%doc Bitstream-Cyberfonts-licence.txt
%{ttffontsdir}/*
%else
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%endif
