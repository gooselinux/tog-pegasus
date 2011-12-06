#
#
#               OpenPegasus (Red Hat release) RPM .spec file
#
#  tog-pegasus.spec
#
#   Copyright (c) 2000 - 2006, 
#     The Open Group; Hewlett-Packard Development Company, L.P.;
#     IBM Corp.;  BMC Software; Tivoli Systems.
#     Licensed under the "Open Group Pegasus Open Source" license 
#     shipped with this software.
#
#  Upstream tog-pegasus.spec file modified for Red Hat build -
#  April 2006, Jason Vas Dias <jvdias@redhat.com>, Red Hat Inc.
#

%{?!LINUX_VERSION: 		%define LINUX_VERSION  %{?dist}}
#
%{?!PEGASUS_BUILD_TEST_RPM:   	%define PEGASUS_BUILD_TEST_RPM        0}
# do "rpmbuild --define 'PEGASUS_BUILD_TEST_RPM 1'" to build test RPM.
#
%{?!NOCLEAN:     		%define NOCLEAN 0}
# ^- 1: don't do %clean
%{?!NODEBUGINFO: 		%define NODEBUGINFO 0}
# ^- 1: don't generate debuginfo or strip binaries
%if %{NODEBUGINFO}
%define debug_package   %{nil}
%endif
%define srcname    	pegasus
%define pegasus_gid	65
%define pegasus_uid	66

%define multilib        0
%define bsx             ''
%ifarch %{ix86} x86_64 ppc ppc64 s390 s390x sparcv9 sparc64
%define multilib        1
%define bsx             -32
%ifarch x86_64 ppc64 s390x sparc64
%define bsx             -64 
%endif
%endif

Version: 		2.9.1
Release: 		5%{?dist}
Epoch:   		2
#
Summary:   		OpenPegasus WBEM Services for Linux
Name:      		tog-pegasus
Group:     		System Environment/Daemons
URL:       		http://www.openpegasus.org
#
License:   		MIT
#
BuildRoot: 		%{_tmppath}/%{name}-%{version}-%{release}-%{_target_cpu}-%(%{__id} -u -n)
#
Source:			http://www.openpegasus.org/uploads/40/18361/pegasus-%{version}.tar.gz
#  1: Description of security enhacements
Source1:        	README.RedHat.Security
#  2: Script for setting SSL certificates - used in init script when cimserver is started for the first time
Source2:		genOpenPegasusSSLCerts
#  3: Script for managing and avoiding multilib problems
Source3:		pegasus_arch_alternatives
#  4: Makefile used instead of upstream Makefile
Source4:		RedHat.OpenPegasus.Makefile
#  5: Description of SSL settings
Source5:		README.RedHat.SSL
#
#  0: Still not fixed by http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5008
#     Changes to the init script to make it LSB compliant
Patch0:			pegasus-2.9.0-initscript.patch
#  1: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5011
#     Removing insecure -rpath
Patch1:			pegasus-2.9.0-no-rpath.patch
#  2: Adding -fPIE
Patch2:			pegasus-2.7.0-PIE.patch
#  3: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5016
#     Configuration variables
Patch3:			pegasus-2.9.0-redhat-config.patch
#  4: don't see how http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5099 fixed it
#     Changing provider dir to the directory we use
Patch4:			pegasus-2.9.0-cmpi-provider-lib.patch
#  5: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5010
#     We distinguish between local and remote user and behave adequately (will be upstream once)
Patch5:			pegasus-2.9.0-local-or-remote-auth.patch
#  6: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5012
#     Modifies pam rules to use access cofiguration file and local/remote differences
Patch6:			pegasus-2.5.1-pam-wbem.patch
#  7: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5006
#     Modifies Makefile for the tests
Patch7:			pegasus-2.9.0-fix_tests.patch
#  9: Adds cimuser binary to admin commands
Patch9:			pegasus-2.6.0-cimuser.patch
# 11: Disables privilege separation feature
Patch11:		pegasus-2.9.0-no_privilege_separation.patch
# 12: Removes snmp tests, which we don't want to perform
Patch12:		pegasus-2.7.0-no_snmp_tests.patch
# 13: Changes to make package compile on sparc
Patch13:                pegasus-2.9.0-sparc.patch
# 15: SSL fix
Patch15:		pegasus-2.9.0-openssl.patch
# 16: Fixes "getpagesize" build error
Patch16:		pegasus-2.9.1-getpagesize.patch
# 17: Fixes memory leak (backported from upstream accepted patch)
Patch17:		pegasus-2.9.1-memleak.patch
#
Conflicts: 		openwbem
Provides: 		tog-pegasus-cimserver
#
BuildRequires:      	bash, sed, grep, coreutils, procps, gcc, gcc-c++
BuildRequires:      	imake, libstdc++, make, pam-devel
BuildRequires:      	openssl-devel >= 0.9.8b, e2fsprogs
BuildRequires:		net-snmp-devel
#
Requires:           	bash, sed, grep, coreutils, procps, openssl >= 0.9.8b, pam
Requires:          	chkconfig, sysvinit
Requires:           	e2fsprogs, bind-utils, net-tools
Requires(post):     	bash, sed, grep, coreutils, procps, openssl >= 0.9.8b, pam
Requires(post):    	chkconfig, sysvinit
Requires(post):     	e2fsprogs, bind-utils, net-tools
Requires(pre):      	bash, sed, grep, coreutils, procps, openssl >= 0.9.8b, pam
Requires(pre):     	chkconfig, sysvinit
Requires(pre):      	e2fsprogs, bind-utils, net-tools
Requires(postun):   	bash, sed, grep, coreutils, procps, openssl >= 0.9.8b, pam
Requires(postun):  	chkconfig, sysvinit
Requires(postun):   	e2fsprogs, bind-utils, net-tools
Requires:		net-snmp

%description
OpenPegasus WBEM Services for Linux enables management solutions that deliver
increased control of enterprise resources. WBEM is a platform and resource
independent DMTF standard that defines a common information model and
communication protocol for monitoring and controlling resources from diverse
sources.

%package devel
Summary: 		The OpenPegasus Software Development Kit
Group: 			Systems Management/Base
Requires:               tog-pegasus >= %{version}-%{release}
Obsoletes: 		tog-pegasus-sdk
Requires:		make, gcc, gcc-c++
Requires(preun): 	make

%description devel
The OpenPegasus WBEM Services for Linux SDK is the developer's kit for the
OpenPegasus WBEM Services for Linux release. It provides Linux C++ developers
with the WBEM files required to build WBEM Clients and Providers. It also
supports C provider developers via the CMPI interface.

%if %{PEGASUS_BUILD_TEST_RPM}
%package test
Summary: 		The OpenPegasus Tests
Group: 			Systems Management/Base
Requires:               tog-pegasus >= %{version}-%{release}, make

%description test
The OpenPegasus WBEM tests for the OpenPegasus %{version} Linux rpm.
%endif

%prep
%setup -q -n %{srcname}
%patch1 -p1 -b .no-rpath
%patch2 -p1 -b .PIE
%patch3 -p1 -b .redhat-config
%patch4 -p1 -b .cmpi-provider-lib
%patch6 -p1 -b .pam-wbem
%patch7 -p1 -b .fix-tests
%patch9 -p1 -b .cimuser
%patch11 -p1 -b .no_privilege_separation
%patch12 -p1 -b .no_snmp_tests
%patch5 -p1 -b .local-or-remote-auth
%patch13 -p1 -b .sparc
%patch15 -p1 -b .openssl
%patch0 -p1 -b .initscript
%patch16 -p1 -b .getpagesize
%patch17 -p1 -b .memleak
find . -name 'CVS' -exec /bin/rm -rf '{}' ';' >/dev/null 2>&1 ||:;

%build
rm -rf ${RPM_BUILD_ROOT} || :;
cp -fp %SOURCE1 doc
cp -fp %SOURCE2 rpm
cp -fp %SOURCE4 .;
cp -fp %SOURCE5 doc

export RPM_ARCH_LIB=%{_lib}
export RPM_ARCH=%{_target_cpu}
export RPM_BUILD_DIR=`pwd`
export RPM_ARCH=`uname -i`
export RPM_OPT_FLAGS=`rpm -q rpm --qf '%{OPTFLAGS}'`
%ifarch ia64
  export PEGASUS_PLATFORM=LINUX_IA64_GNU
%else
  %ifarch x86_64
    export PEGASUS_PLATFORM=LINUX_X86_64_GNU
  %else
    %ifarch ppc
      export PEGASUS_PLATFORM=LINUX_PPC_GNU
    %else
      %ifarch ppc64
        export PEGASUS_PLATFORM=LINUX_PPC64_GNU
      %else
        %ifarch s390
          export PEGASUS_PLATFORM=LINUX_ZSERIES_GNU
        %else
          %ifarch s390x
            export PEGASUS_PLATFORM=LINUX_ZSERIES64_GNU
          %else
            %ifarch sparcv9
              export PEGASUS_PLATFORM=LINUX_SPARCV9_GNU
            %else
              %ifarch sparc64
                export PEGASUS_PLATFORM=LINUX_SPARC64_GNU
              %else
                export PEGASUS_PLATFORM=LINUX_IX86_GNU
              %endif
            %endif
          %endif
        %endif
      %endif
    %endif
  %endif
%endif
export PEGASUS_ROOT=${RPM_BUILD_DIR}
export PEGASUS_HOME=${PEGASUS_ROOT}/build
export PEGASUS_ARCH_LIB=${RPM_ARCH_LIB}
export PEGASUS_ENVVAR_FILE=${PEGASUS_ROOT}/env_var_Linux.status
export PEGASUS_EXTRA_C_FLAGS="${RPM_OPT_FLAGS} -Wno-unused"
export PEGASUS_EXTRA_CXX_FLAGS=${PEGASUS_EXTRA_C_FLAGS}
export PEGASUS_EXTRA_PROGRAM_LINK_FLAGS="-pie -Wl,-z,relro,-z,now,-z,nodlopen,-z,noexecstack"
export OPENSSL_HOME=/usr
export OPENSSL_BIN=/usr/bin
export SYS_INCLUDES=-I/usr/kerberos/include
export LD_LIBRARY_PATH=${PEGASUS_HOME}/lib
export PATH=${PEGASUS_HOME}/bin:${PATH}

make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release create_ProductVersionFile
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release create_CommonProductDirectoriesInclude
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release create_ConfigProductDirectoriesInclude
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release depend
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release all
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release repository
%if %{PEGASUS_BUILD_TEST_RPM}
    make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.ReleaseTest -s create_repository
%endif

%install
export RPM_ARCH_LIB=%{_lib}
export RPM_ARCH=%{_target_cpu}
export BSX=%{bsx}
export RPM_BUILD_DIR=`pwd`
export RPM_ARCH=`uname -i`
export RPM_OPT_FLAGS=`rpm -q rpm --qf '%{OPTFLAGS}'`
%ifarch ia64
  export PEGASUS_PLATFORM=LINUX_IA64_GNU
%else
  %ifarch x86_64
    export PEGASUS_PLATFORM=LINUX_X86_64_GNU
  %else
    %ifarch ppc
      export PEGASUS_PLATFORM=LINUX_PPC_GNU
    %else
      %ifarch ppc64
        export PEGASUS_PLATFORM=LINUX_PPC64_GNU
      %else
        %ifarch s390
          export PEGASUS_PLATFORM=LINUX_ZSERIES_GNU
        %else
          %ifarch s390x
            export PEGASUS_PLATFORM=LINUX_ZSERIES64_GNU
          %else
            %ifarch sparcv9
              export PEGASUS_PLATFORM=LINUX_SPARCV9_GNU
            %else
              %ifarch sparc64
                export PEGASUS_PLATFORM=LINUX_SPARC64_GNU
              %else
                export PEGASUS_PLATFORM=LINUX_IX86_GNU
              %endif
            %endif
          %endif
        %endif
      %endif
    %endif
  %endif
%endif
export PEGASUS_ROOT=${RPM_BUILD_DIR}
export PEGASUS_HOME=${PEGASUS_ROOT}/build
export PEGASUS_ARCH_LIB=${RPM_ARCH_LIB}
export PEGASUS_ENVVAR_FILE=${PEGASUS_ROOT}/env_var_Linux.status
export PEGASUS_EXTRA_C_FLAGS="${RPM_OPT_FLAGS} -Wno-unused"
export PEGASUS_EXTRA_CXX_FLAGS=${PEGASUS_EXTRA_C_FLAGS}
export PEGASUS_EXTRA_PROGRAM_LINK_FLAGS="-pie -Wl,-z,relro,-z,now,-z,nodlopen,-z,noexecstack"
export OPENSSL_HOME=/usr
export OPENSSL_BIN=/usr/bin
export SYS_INCLUDES=-I/usr/kerberos/include
export LD_LIBRARY_PATH=${PEGASUS_HOME}/lib
export PATH=${PEGASUS_HOME}/bin:${PATH}

make -f RedHat.OpenPegasus.Makefile install prefix=$RPM_BUILD_ROOT libdir=%{_libdir} root_user=%(%{__id} -u -n) pegasus_user=%(%{__id} -u -n)
%if %{PEGASUS_BUILD_TEST_RPM}
    make -f %{SOURCE4} install_tests prefix=${RPM_BUILD_ROOT} root_user=%(%{__id} -u -n) pegasus_user=%(%{__id} -u -n)    
%endif

%if %{multilib}
    %{SOURCE3} --list '%ghost' | grep 'bin/' > ghost_arch_binaries;
    %{SOURCE3} --list '%ghost' | grep 'mak/' > ghost_arch_devel;
    %{SOURCE3} --list '%ghost' | grep 'test/'> ghost_arch_test;
    cp -fp %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/Pegasus/scripts;
%else
    touch ghost_arch_binaries;
    touch ghost_arch_devel;
    touch ghost_arch_test;
%endif
%if %{NODEBUGINFO}
    /usr/lib/rpm/brp-compress;
    exit 0;
%endif

:;


%files -f ghost_arch_binaries
%defattr(0750, root, pegasus, 0750)
%if !%{NODEBUGINFO}
%exclude /usr/lib/debug
%endif
%defattr(0755, root, pegasus, 0750)
/usr/%{_lib}/*
/usr/share/Pegasus/scripts
%defattr(0750, root, pegasus, 0750)
/usr/sbin/*
%attr(0755, root, pegasus) /usr/sbin/cimauth
%attr(0755, root, pegasus) /usr/sbin/cimconfig
%attr(0755, root, pegasus) /usr/sbin/cimprovagt
%attr(0755, root, pegasus) /usr/sbin/cimserver
%attr(0755, root, pegasus) /usr/sbin/cimuser
%attr(0755, root, pegasus) /usr/sbin/repupgrade
/usr/bin/*
%attr(0755, root, pegasus) /usr/bin/cimmof
%attr(0755, root, pegasus) /usr/bin/cimmofl
%attr(0755, root, pegasus) /usr/bin/cimprovider
%attr(0755, root, pegasus) /usr/bin/osinfo
%attr(0755, root, pegasus) /usr/bin/wbemexec
%attr(0755, root, pegasus) %config(noreplace) /etc/rc.d/init.d/tog-pegasus
%defattr(0640, root, pegasus, 0750)
%dir   /etc/Pegasus
%ghost %config(noreplace) /etc/Pegasus/cimserver_current.conf
%ghost %config(noreplace) /etc/Pegasus/cimserver_planned.conf
%config(noreplace) /etc/Pegasus/access.conf
%config(noreplace) /etc/pam.d/wbem
%ghost /etc/Pegasus/ssl.cnf
%ghost /etc/Pegasus/client.pem
%ghost /etc/Pegasus/server.pem
%ghost /etc/Pegasus/file.pem
%ghost /etc/Pegasus/cimserver_trust
%ghost /etc/Pegasus/indication_trust
%ghost /etc/Pegasus/crl
%dir /var/lib/Pegasus
%verify(not md5 size mtime mode group) /var/lib/Pegasus/repository
/var/lib/Pegasus/cache
%dir /var/lib/Pegasus/log
%ghost %verify(not md5 size mtime) /var/lib/Pegasus/log/install.log
%ghost %verify(not md5 size mtime) /var/lib/Pegasus/cache/trace/cimserver.trc
%dir   %attr(1750,root,pegasus) /var/run/tog-pegasus
%ghost /var/run/tog-pegasus/cimserver.pid
%ghost /var/run/tog-pegasus/cimserver_start.lock
%ghost %attr(1640,root,pegasus) /var/run/tog-pegasus/cimxml.socket
%defattr(0644, root, pegasus, 0755)
%dir /usr/share/Pegasus
/usr/share/Pegasus/mof
/usr/share/man/man8/*
/usr/share/man/man1/*
%doc doc/license.txt doc/Admin_Guide_Release.pdf doc/PegasusSSLGuidelines.htm doc/SecurityGuidelinesForDevelopers.html doc/README.RedHat.Security src/Clients/repupgrade/doc/repupgrade.html doc/README.RedHat.SSL


%files devel -f ghost_arch_devel
%defattr(0644,root,pegasus,0755)
/usr/include/Pegasus
/usr/share/Pegasus/samples
/usr/share/Pegasus/html

%if %{PEGASUS_BUILD_TEST_RPM}
%files test -f ghost_arch_test
%defattr(0644,root,pegasus,0755)
%dir /usr/share/Pegasus/test
/usr/share/Pegasus/test/Makefile%{bsx}
/usr/share/Pegasus/test/mak
%verify(not md5 size mtime) /var/lib/Pegasus/testrepository
%defattr(0750,root,pegasus,0755)
/usr/share/Pegasus/test/bin
/usr/share/Pegasus/test/lib
%endif

%clean
%if !%{NOCLEAN}
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf $RPM_BUILD_ROOT;
[ "${RPM_BUILD_DIR}" != "/" ] && rm -rf ${RPM_BUILD_DIR}/%{srcname};
%endif

%pre
if [ $1 -eq 1 ]; then
#  first install: create the 'pegasus' user and group:
   /usr/sbin/groupadd -g %{pegasus_gid} -f -r pegasus >/dev/null 2>&1 || :;
   /usr/sbin/useradd -u %{pegasus_uid} -r -N -M -g pegasus -s /sbin/nologin -d /var/lib/Pegasus \
     	 		   -c "tog-pegasus OpenPegasus WBEM/CIM services" pegasus >/dev/null 2>&1 || :;
elif [ $1 -gt 1 ]; then
   if [ -d /var/lib/Pegasus/repository ]; then
	if [ -d /var/lib/Pegasus/prev_repository ]; then
	   mv /var/lib/Pegasus/prev_repository /var/lib/Pegasus/prev_repository_`date '+%Y-%m-%d-%s.%N'`.rpmsave;
	fi;
	mv /var/lib/Pegasus/repository /var/lib/Pegasus/prev_repository;
   fi
fi
:;

%post
ldconfig;
chkconfig --add tog-pegasus;
if [ $1 -ge 1 ]; then	
   echo `date` >>  /var/lib/Pegasus/log/install.log 2>&1 || :;
%if %{multilib}
    %{_datadir}/Pegasus/scripts/pegasus_arch_alternatives || :;
%endif
   if [ $1 -gt 1 ]; then
      if [ -d /var/lib/Pegasus/prev_repository ]; then
      #  The user's old repository was moved to /var/lib/Pegasus/prev_repository, which 
      #  now must be upgraded to the new repository in /var/lib/Pegasus/repository:
	 /usr/sbin/repupgrade 2>> /var/lib/Pegasus/log/install.log || :;
         mv /var/lib/Pegasus/prev_repository /var/lib/Pegasus/prev_repository_`date '+%Y-%m-%d-%s.%N'`.rpmsave;
      fi;
      /sbin/service tog-pegasus condrestart >/dev/null 2>&1 || :;
   fi;
fi
:;

%preun
if [ $1 -eq 0 ]; then
   /sbin/service tog-pegasus stop >/dev/null 2>&1 || :;
   /sbin/chkconfig --del tog-pegasus >/dev/null 2>&1 || :;
%if %{multilib}
   if [ "$1" -eq 0 ]; then
      /usr/sbin/alternatives --remove pegasus /usr/sbin/cimserver-64 >/dev/null 2>&1 || :;
      /usr/sbin/alternatives --remove pegasus /usr/sbin/cimserver-32 >/dev/null 2>&1 || :;
   fi
%endif
fi
:;

%postun -p /sbin/ldconfig

%post devel
if [ $1 -ge 0 ]; then
    %{_datadir}/Pegasus/scripts/pegasus_arch_alternatives devel || :;
fi
:;

%preun devel
if [ $1 -eq 0 ] ; then
   make --directory /usr/share/Pegasus/samples -s clean >/dev/null 2>&1 || :;
%if %{multilib}
   /usr/sbin/alternatives --remove pegasus-devel %{_datadir}/Pegasus/samples/mak/config.mak-64 >/dev/null 2>&1 || :;
   /usr/sbin/alternatives --remove pegasus-devel %{_datadir}/Pegasus/samples/mak/config.mak-32 >/dev/null 2>&1 || :;
%endif
fi
:;

%if %{PEGASUS_BUILD_TEST_RPM}
%if %{multilib}
%post test
if [ $1 -ge 0 ]; then
   %{_datadir}/Pegasus/scripts/pegasus_arch_alternatives test || :;
fi
:;

%preun test
if [ $1 -eq 0 ]; then
%if %{multilib}
   /usr/sbin/alternatives --remove pegasus-test %{_datadir}/Pegasus/test/Makefile-64 >/dev/null 2>&1 || :;
   /usr/sbin/alternatives --remove pegasus-test %{_datadir}/Pegasus/test/Makefile-32 >/dev/null 2>&1 || :;
%endif
fi
:;
%endif
%endif


%changelog
* Thu Jul 15 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.1-5
- Add cimsub to the pegasus_arch_alternatives script

* Thu Jun 17 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.1-4
- Mark files in /var/lib/Pegasus as noverify in spec file

* Tue May 25 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.1-3
- Fix memory leak

* Thu Apr 22 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.1-2
- Fix initscript permissions

* Thu Jan 14 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.1-1
- Update to upstream version 2.9.1
- Add patch/source descriptions to the spec file

* Wed Nov 25 2009 Dennis Gregorovic <dgregor@redhat.com> - 2:2.9.0-8.1
- Rebuilt for RHEL 6

* Mon Nov  2 2009 Vitezlsav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-8
- Fix wrong multilib flag for ix86 arch

* Wed Sep 23 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-7
- Fix initscript
  Resolves: #523370

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 2:2.9.0-6
- Use password-auth common PAM configuration instead of system-auth

* Wed Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 2:2.9.0-5
- rebuilt with new openssl

* Wed Aug 19 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-4
- Fix Source (but I'm afraid it's not very persistent and it will
  not work again after some time)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-2
- Fix Group

* Mon Jun 16 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-1
- Update to upstream version 2.9.0
- Remove redhat-lsb requires
- Add README.RedHat.SSL

* Thu Apr 16 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.2-8
- Replace useradd '-n' option by '-N' ('-n' is obsolete)
  Resolves: #495729

* Tue Mar  3 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.2-7
- Add noreplace to config files

* Sat Feb 28 2009 Caolán McNamara <caolanm@redhat.com> - 2:2.7.2-6
- fix elif

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Dennis Gilmore < dennis@ausil.us> - 2:2.7.2-4
- apply sparc fixes

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 2:2.7.2-3
- rebuild with new openssl

* Tue Nov 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.2-2
- Fix local or remote auth patch to work correctly with new code base
  Related: #459217

* Thu Nov  6 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.2-1
- Update to upstream version 2.7.2
  (remove patches added in 2.7.1-1 - they're upstream now)
- Enable out-of-process providers
  Resolves: #455109

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2.7.1-2
- fix license tag

* Tue Jul 15 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.1-1
- Update to upstream version 2.7.1
- Fix setElementAt() doesn't copy value of CMPI_char parameter
  Resolves: #454589
- Fix CMPI MI factories that return errors are unsupported
  Resolves: #454590
- Fix HTTP 401 responses lack Content-Length headers
  Resolves: #454591

* Tue Jul  1 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-9
- Add SNMP indication handler to package
  Resolves: #452930

* Tue Jun  3 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-8
- Add cimsub to package
  Resolves: #447823

* Thu May 15 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-7
- Rebuild

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-6
- Rebuild

* Mon Jan 21 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-5
- No snmp tests in Test RPM

* Thu Jan 10 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-4
- Fix Test RPM

* Wed Dec  5 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-3
- Rebuild

* Fri Nov 23 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-2
- Fix OpenPegasus SRPM fails to build Test RPM 
  Resolves: #391961

* Mon Nov 19 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-1
- Update to upstream version 2.7.0
- Unhide some cmpi classes, package cmpi C++ headers
- Fix multiarch conflicts
  Resolves: #343311
- Add libcmpiCppImpl.so (symlink to libcmpiCppImpl.so.1)
  Resolves: #366871

* Tue Oct  9 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.6.1-2
- Fix files permissions
  Resolves: #200906

* Thu Aug 30 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.6.1-1
- Update to 2.6.1
- Fix wrong init script (#245339)

* Wed Mar 28 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.6.0-2
- Update changelog
- Build with Open Pegasus' Makefiles, istall with Red Hats (Mark Hamzy)

* Mon Feb 26 2007 Mark Hamzy <hamzy@us.ibm.com> - 2:2.6.0-1
- Upgrade to upstream version 2.6.0

* Mon Dec  4 2006 Nalin Dahyabhai <nalin@redhat.com> - 2:2.5.2-3
- change requires: tog-pegasus to prereq: tog-pegasus so that the pegasus
  user and group will exist when we go to lay down files for tog-pegasus-devel
  (#218305)
- prereq the current version of openssl so that the right versions of
  libssl and libcrypto will be available in %%post (possible for #208949)

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 2:2.5.2-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Thu Jul 27 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.2-1.fc6
- Upgrade to upstream version 2.5.2
- fix bug 198185
- fix bug 200246

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:2.5.1-10.FC6.1
- rebuild

* Fri Jul 07 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.4.1-10
- More upstream 2.5.2_APPROVED bug fixes:
  o 4629: Pegasus freezes when it is unable to send out completely, the results of a request
  o 5073: Class Names on Reference, ReferenceNames, Assoc, AssocNames returned lower case
  o 5090: cimserver crash on a request after attempting to unload idle CMPI providers
  o 5180: OperationAggregate deleted in _enqueueResponse while member mutex held

* Fri Jun 09 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-8
- Fix bug 192754: remove multilib conflicts
- More upstream 2.5.2_APPROVED bug fixes:
  o 5119: memory leak in CMPI implementation
  o 5115: fix SetConfig_EnvVar comments

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-6
- Apply upstream patches for latest 2.5.2_APPROVED bugs:
  o 5046: cimprovider timeout needs to be increased
  o 5047: cimmof timeout needs to be increased
  o 5048: Invalid Pointer in CIMOperationRequestEncoder code
  o 5049: Unnecessary dependency on experimental headers
  o 5051: Improved handling of OOP indication provide module failures
  o 5053: reserveCapacity method may cause size overflow
  o 5059: XMLWriter does not escape '>' in strings
  o 5072: Potential race condition with OOP response chunks
  o 5083: CIMRequestMessage buildResponse() should be const
- Fix bug 193121: restore world read access to libraries   

* Tue May 02 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-4
- fix bug 190432: %%exclude /usr/lib/debug from RPM
- fix upstream OpenPegasus '2.5.2_APPROVED' bugs, applying upstream patches:
  o 4955 : Bogus Description property for OperatingSystem provider
  o 4956 : reserveCapacity method may cause size overflow on invalid input
  o 4968 : CMPI provider up-calls cause failure with out-of-process
  o 4978 : snmpDeliverTrap_netsnmp::_createSession function is not thread safe
  o 4983 : Memory leak in OOP indication generation
  o 4984 : Forked process hangs in system call
  o 4986 : Adding automated test for snmpIndication Handler
  (  http://cvs.opengroup.org/bugzilla/show_bug.cgi?id=? )
- apply upstream update to 'pegasus-2.5.1-warnings.patch' 

* Mon Apr 17 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-3
- Fix repupgrade (make it use correct paths)

* Fri Apr 14 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-2
- Apply patches for the two '2.5.2_APPROVED' upstream bugzillas 
  4934(4943) and 4945 :
  (http://cvs.opengroup.org/bugzilla/buglist.cgi?bug_id=4943%%2C4945)
- Fix the PATH_MAX and MAXHOSTNAMELEN issues (again)

* Thu Apr 06 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-1
- Upgrade to version 2.5.1 (including new upstream .spec file).

* Tue Mar  7 2006 Bill Nottingham <notting@redhat.com> - 2:2.5-9
- use an assigned uid/gid, do not loop over user ids looking for a free one

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:2.5-6.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-6
- restore SSLv23_method SSL support now that bug 173399 is fixed
- rebuild for new gcc, glibc, glibc-kernheaders
- PAMBasicAuthenticatorUnix.cpp includes no longer include syslog.h: add
- /usr/bin/install now decides to fail if chown fails - set $INSTALL_USER, $INSTALL_GROUP

* Thu Dec 15 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-5
- fix bug 175434 : deal with pegasus uid/gid already existing
  on first install

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 2:2.5-4.1
- rebuilt

* Wed Nov 16 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-4
- fix bug 173401: SSL support broken by openssl-0.9.7g -> 0.9.8a upgrade 

* Wed Nov 09 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-3
- Rebuild for new openssl dependencies
- Enable CMPI support for sblim-cmpi-base with ENABLE_CQL=true

* Mon Oct 31 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-2
- Add /usr/lib/cmpi alternate providerLibDir for sblim-cmpi-base Fedora Extras pkg
- Fix bug 171124: use numeric ids for pegasus user/group
- guidelines: do not remove pegasus user/group in %%postun.

* Fri Oct 14 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Fri Sep 30 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-1
- Implemented new 'make install' target.
- Re-wrote tog-pegasus.spec file from scratch.
- Ported BZ 167986 authentication code and BZ 167164 + BZ 167165 fixes from RHEL-4

* Wed Sep 28 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-0
- Initial build.
