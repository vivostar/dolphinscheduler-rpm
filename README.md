Build script to create RPMS for [dolphinscheduler](https://dolphinscheduler.apache.org).
==================================================================

[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

[![CN doc](https://img.shields.io/badge/文档-中文版-blue.svg)](README_zh_CN.md)
[![EN doc](https://img.shields.io/badge/document-English-blue.svg)](README.md)

## Features

Dolphinscheduler-rpm can build dolphinscheduler rpms
- Easy to deploy dolphinscheduler on cluster.
- Easy to manage dolphinscheduler by configuration management tools, such as [ambari](https://ambari.apache.org/), [puppet](https://www.puppet.com/) and [ansible](https://www.ansible.com/) and monitor dolphinscheduler services.

## How to Build

You should install rpm-build, make on your dev machine


```bash
# rockylinux-8
yum install -y make, rpm-build
```

```bash
# ubuntu-22.04
sudo apt install -y make, rpm
```
and then

```bash
make
```

## How to Use

Download the dolphinscheduler rpm files into local dictionary, and make local yum repo.

Before you deploy dolphinscheduler, you should deploy zookeeper and mysql first

If you want to install dolphinscheduler-master-server on a node, you should

```bash
# install jdk8
yum install java-1.8.0-openjdk-devel -y
# install dolphinscheduler-master-server
yum install -y dolphinscheduler-master-server dolphinscheduler-tools mysql-connector-j
ln -s /usr/share/java/mysql-connector-j.jar /usr/lib/dolphinscheduler/api-server/libs/
ln -s /usr/share/java/mysql-connector-j.jar /usr/lib/dolphinscheduler/master-server/libs/
```

Edit dolphinscheduler_env.sh
here is example:

```bash
#######################################
. /usr/lib/bigtop-utils/bigtop-detect-javahome
DATABASE=mysql
REGISTRY_ZOOKEEPER_CONNECT_STRING="localhost:2181"

# JAVA_HOME, will use it to start DolphinScheduler server
export JAVA_HOME=${JAVA_HOME:-/opt/java/openjdk}

# Database related configuration, set database type, username and password
export DATABASE=${DATABASE:-postgresql}
export SPRING_PROFILES_ACTIVE=${DATABASE}
export SPRING_DATASOURCE_URL="jdbc:mysql://localhost:3306/dev"
export SPRING_DATASOURCE_USERNAME="dev"
export SPRING_DATASOURCE_PASSWORD="devpass"
#######################################
```

start services

```bash
# init databases
cd /usr/lib/dolphinscheduler/tools/bin && bash -x upgrade-schema.sh
# service start
service dolphinscheduler-api-server start
service dolphinscheduler-master-server start
```

## Get Help

Welcomes everyone to contribute, and if you come accross any problems, please submit an issue.

## Thanks

DolphinScheduler is an excellent open-source project that is easy to use, with simple and convenient operation.

## License

Please refer to the [LICENSE](https://github.com/vivostar/dolphinscheduler-rpm/blob/master/LICENSE) file
