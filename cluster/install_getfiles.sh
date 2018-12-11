#!/bin/sh
wget -c http://apache-mirror.rbc.ru/pub/apache/hadoop/common/hadoop-2.9.1/hadoop-2.9.1.tar.gz
wget -c http://mirror.linux-ia64.org/apache/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
mv hadoop*.tar.gz playbooks/files/
mv spark*tgz playbooks/files/
