为 [dolphinscheduler](https://dolphinscheduler.apache.org) 构建rpm包
==================================================================

[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

[![CN doc](https://img.shields.io/badge/文档-中文版-blue.svg)](README_zh_CN.md)
[![EN doc](https://img.shields.io/badge/document-English-blue.svg)](README.md)

## Features

Dolphinscheduler-rpm 可以构建rpm包
- 方便dolphinscheduler部署在集群上
- 方便与配置管理工具集成，如 [ambari](https://ambari.apache.org/)， [puppet](https://www.puppet.com/) ， [ansible](https://www.ansible.com/) ，并且管理dolphinscheduler后台服务

## How to Build

在你的开发的机器上安装make，与rpm-build


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

下载rpm包到本地目录，并构建yum repo，在你部署之前，确保安装了zookeeper与mysql.
下面演示怎么部署dolphinscheduler-master-server

```bash
# install jdk8
yum install java-1.8.0-openjdk-devel -y
# install dolphinscheduler-master-server
yum install -y dolphinscheduler-master-server dolphinscheduler-tools mysql-connector-j
ln -s /usr/share/java/mysql-connector-j.jar /usr/lib/dolphinscheduler/api-server/libs/
ln -s /usr/share/java/mysql-connector-j.jar /usr/lib/dolphinscheduler/master-server/libs/
```

编辑 dolphinscheduler_env.sh

```bash
#######################################
. /usr/lib/bigtop-utils/bigtop-detect-javahome
DATABASE=mysql
REGISTRY_ZOOKEEPER_CONNECT_STRING="172.18.0.2:2181"

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

开启服务

```bash
# 初始化数据库
cd /usr/lib/dolphinscheduler/tools/bin && bash -x upgrade-schema.sh
# 启动服务
service dolphinscheduler-api-server start
service dolphinscheduler-master-server start
```

## Get Help

欢迎大家前来提交贡献，如果你遇到任何问题，请提交issue

## Thanks

DolphinScheduler是非常棒的开源软件，方便了大数据服务的使用，软件架构清晰，文档齐全，部署运维也方便

## License

请参考 [LICENSE](https://github.com/vivostar/dolphinscheduler-rpm/blob/master/LICENSE) 
