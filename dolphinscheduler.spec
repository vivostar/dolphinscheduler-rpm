%define debug_package %{nil}
# define _unpackaged_files_terminate_build 0
# disable repacking jars
%define __os_install_post %{nil}
%define services alert-server api-server master-server worker-server standalone-server
%global initd_dir %{_sysconfdir}/rc.d/init.d

Name:       dolphinscheduler
Version:    %{VERSION}
Release:    1%{?dist}
Summary:    modern data workflow orchestration platform 
Group:      Applications/Internet
License:    Apache 2.0
URL:        https://dolphinscheduler.apache.org/
Source0:     apache-%{name}-%{version}-bin.tar.gz
BuildRoot:  %{_tmppath}/apache-%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Packager:   Shuaipeng Lee <lishuaipeng651@gmail.com>

Requires: bigtop-utils >= 0.7

AutoReqProv: no

%description
Apache DolphinScheduler is the modern data workflow orchestration platform with powerful user interface, dedicated to solving complex task dependencies in the data pipeline and providing various types of jobs available `out of the box`

%package        alert-server
Summary:        dolphinscheduler alert server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    alert-server
dolphinscheduler alert server

%package        api-server
Summary:        dolphinscheduler api server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    api-server
dolphinscheduler api server

%package        bin
Summary:        dolphinscheduler original bin
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    bin
dolphinscheduler original bin

%package        master-server
Summary:        dolphinscheduler master server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}, %{name}-ui = %{version}-%{release}, %{name}-api-server = %{version}-%{release}

%description    master-server
dolphinscheduler master server

%package        standalone-server
Summary:        dolphinscheduler standalone server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}, %{name}-ui = %{version}-%{release}

%description    standalone-server
dolphinscheduler standalone server

%package        tools
Summary:        dolphinscheduler tools
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}, %{name}-bin = %{version}-%{release}

%description    tools
dolphinscheduler tools

%package        ui
Summary:        dolphinscheduler ui
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    ui
dolphinscheduler ui

%package        worker-server
Summary:        dolphinscheduler worker server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    worker-server
dolphinscheduler worker server

%prep
%setup -q -n apache-%{name}-%{version}-bin

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m 0755 %{buildroot}
%{__install} -d -m 0755 %{buildroot}/usr/lib/%{name}
%{__install} -d -m 0755 %{buildroot}/var/lib/%{name}
%{__install} -d -m 0755 %{buildroot}/var/log/%{name}
%{__install} -d -m 0755 %{buildroot}/var/run/%{name}

%{__cp} -rp alert-server %{buildroot}/usr/lib/%{name}
%{__cp} -rp api-server %{buildroot}/usr/lib/%{name}
%{__cp} -rp bin %{buildroot}/usr/lib/%{name}
%{__cp} -rp master-server %{buildroot}/usr/lib/%{name}
%{__cp} -rp standalone-server %{buildroot}/usr/lib/%{name}
%{__cp} -rp tools %{buildroot}/usr/lib/%{name}
%{__cp} -rp ui %{buildroot}/usr/lib/%{name}
%{__cp} -rp worker-server %{buildroot}/usr/lib/%{name}

%{__install} -d %{buildroot}/etc/%{name}/alert-server
%{__install} -d %{buildroot}/etc/%{name}/api-server
%{__install} -d %{buildroot}/etc/%{name}/master-server
%{__install} -d %{buildroot}/etc/%{name}/standalone-server
%{__install} -d %{buildroot}/etc/%{name}/worker-server
%{__install} -d %{buildroot}/etc/%{name}/tools

# create relative symlink
ln -s -r %{buildroot}/usr/lib/%{name}/alert-server/conf      %{buildroot}/etc/%{name}/alert-server
ln -s -r %{buildroot}/usr/lib/%{name}/api-server/conf        %{buildroot}/etc/%{name}/api-server 
ln -s -r %{buildroot}/usr/lib/%{name}/master-server/conf     %{buildroot}/etc/%{name}/master-server
ln -s -r %{buildroot}/usr/lib/%{name}/standalone-server/conf %{buildroot}/etc/%{name}/standalone-server   
ln -s -r %{buildroot}/usr/lib/%{name}/worker-server/conf     %{buildroot}/etc/%{name}/worker-server    
ln -s -r %{buildroot}/usr/lib/%{name}/tools/conf             %{buildroot}/etc/%{name}/tools

# Generate the init.d scripts
%{__install} -d -m 0755 %{buildroot}/%{initd_dir}

for service in %{services}
do
  bash %{_sourcedir}/init.d.tmpl %{_sourcedir}/%{name}-${service}.svc rpm %{buildroot}/%{initd_dir}/%{name}-${service}
done
      

%pre
if ! /usr/bin/id dolphinscheduler &>/dev/null; then
    /usr/sbin/useradd -r -d /var/lib/dolphinscheduler -s /bin/sh -c "dolphinscheduler" dolphinscheduler || \
        %logmsg "Unexpected error adding user \"dolphinscheduler\". Aborting installation."
    # /sbin/usermod -a -G hadoop dolphinscheduler
fi

%post
systemctl daemon-reload

%preun

%postun
systemctl daemon-reload
if [ $1 -eq 0 ]; then
    /usr/sbin/userdel dolphinscheduler || %logmsg "User \"dolphinscheduler\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files 
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/var/lib/dolphinscheduler
/var/log/dolphinscheduler
/var/run/dolphinscheduler

%files alert-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/usr/lib/dolphinscheduler/alert-server
/etc/dolphinscheduler/alert-server/conf
%defattr(-,root,root,-)
%{initd_dir}/%{name}-alert-server

%files api-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/usr/lib/dolphinscheduler/api-server
/etc/dolphinscheduler/api-server/conf
%defattr(-,root,root,-)
%{initd_dir}/%{name}-api-server

%files bin
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/usr/lib/dolphinscheduler/bin

%files master-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/usr/lib/dolphinscheduler/master-server
/etc/dolphinscheduler/master-server/conf
%defattr(-,root,root,-)
%{initd_dir}/%{name}-master-server

%files standalone-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/usr/lib/dolphinscheduler/standalone-server
/etc/dolphinscheduler/standalone-server/conf
%defattr(-,root,root,-)
%{initd_dir}/%{name}-standalone-server

%files tools
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/usr/lib/dolphinscheduler/tools
/etc/dolphinscheduler/tools/conf

%files ui
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/usr/lib/dolphinscheduler/ui

%files worker-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
/usr/lib/dolphinscheduler/worker-server
/etc/dolphinscheduler/worker-server/conf
%defattr(-,root,root,-)
%{initd_dir}/%{name}-worker-server
