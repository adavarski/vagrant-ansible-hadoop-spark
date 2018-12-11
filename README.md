# Hadoop + Spark
 Creating Hadoop cluster with Spark (Using vagrant + ansible)
 - Presentation / Documentation: https://adavarski.github.io/vagrant-ansible-hadoop-spark/
 - Based on this outdated repository (https://github.com/cybermaster/hadoop-spark-vagrant-ansible)
 - Check Vagrantfile and inventory/vagrant-4hosts.inv and make needed changes (there are .ORIG files for 4host: 1 master, 3 workers and 1 client. Used 1 master, 1 worker and 1 client in this example )

 

# Steps to create a cluster
```
 -   Clone the repository
 -   cd cluster/
 -   vagrant up
 -   sh install_getfiles.sh
 -   ansible-playbook -i inventory/vagrant-4hosts.inv playbooks/hadoop.yml
 -   ssh -i ~/.vagrant.d/insecure_private_key vagrant@192.168.50.[11:13]
     ```
     1.Add swapfile to all hosts:
     $ sudo fallocate -l 2G /swapfile
     $ sudo chmod 600 /swapfile
     $ sudo mkswap /swapfile
     $ sudo swapon /swapfile
     $ sudo swapon -s
     
     2. Define slaves in etc/hadoop/slaves on master
     vagrant@hadoopmaster:/usr/local/hadoop-2.9.1$ cat etc/hadoop/slaves 
     192.168.50.11
     192.168.50.12
     
     3.Setup RM port on master
     vagrant@hadoopmaster:/usr/local/hadoop-2.9.1$ diff etc/hadoop/yarn-env.sh etc/hadoop/yarn-env.sh.ORIG
     107c107
     < YARN_OPTS="$YARN_OPTS -Djava.net.preferIPv4Stack=true"
     ---
     > 
     vagrant@hadoopmaster:/usr/local/hadoop-2.9.1$ diff ./etc/hadoop/yarn-site.xml.ORIG ./etc/hadoop/yarn-site.xml
     34c34
     <                        <value>hadoopmaster:8088</value>
     ---
     >                        <value>0.0.0.0:8088</value>

 -   vm# cd $HADOOP_INSTALL
 -   vm# sbin/start-all.sh
 
 ```
# Our architecture

https://github.com/adavarski/vagrant-ansible-hadoop-spark/blob/master/docs/images/net01.png

# How to test Hadoop cluster

 -   Prepare hdfs: bin/hdfs namenode -format
 -   Cleate input dir for data: bin/hdfs dfs -mkdir /in
 -   Put some info in it: bin/hdfs dfs -copyFromLocal /home/vagrant/books/* /in
 -   Run example: bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.9.1.jar wordcount /in /out
 -   See results: bin/hdfs dfs -ls /out
 -   Remove results: bin/hdfs dfs -rm -R /out
 
 You can see the cluster at work in browser (http://192.168.50.11:8088/cluster/apps)

# How to test Spark cluster (in Scala)

 -   vm# spark-shell
 -   ss# var input = spark.read.textFile("/in/somefile.txt")
 -   ss# input.filter(line => line.length()>0).count()
 
 Spark webUI: http://192.168.50.11:4040/jobs/
 
 # TEST TASK
 
Spark job for counting words with 2 and more vowels https://github.com/adavarski/vagrant-ansible-hadoop-spark/blob/master/cluster/playbooks/files/calc.py

Calculate words with 2 and more vowels in an online book
```
Getting a book
1. We can't get online resource and put in cluster. So let's download it in temporary file
vm# pyspark
>>> import urllib2
>>> response = urllib2.urlopen("http://www.gutenberg.org/files/36/36-0.txt") 
>>> data = response.read()
>>> f_ = open("/tmp/test.txt","w")
>>> f_.write(data)
>>> f_.close()

2. Put the book in hdfs
>>> from subprocess import PIPE, Popen
>>> put = Popen(["hadoop", "fs", "-put", "/tmp/test.txt", "/in/sample.txt"], stdin=PIPE, bufsize=-1)
>>> put.communicate()

3. Prepare parsers and function
>>> from pyspark.sql.functions import *
>>> import re
>>> strlen = spark.udf.register("stringLengthString", lambda x: len(x))
>>> p = re.compile("[^EUIOAeuioaуеыаоэяию]")
>>> strvowels = spark.udf.register("stringVowels", lambda x: p.sub("",x.lower()))

4. Starting task
>>> textFile = spark.read.text("/in/sample.txt")
>>> textFile.select(explode(split(textFile.value,"\s+"))).where("stringLengthString(stringVowels(col)) >= 2").count()
            
5. Executing as a spark job
spark-submit  ~/calc.py

$ cat cluster/playbooks/files/calc.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyspark import SparkContext
from pyspark.sql.session import *
from pyspark.sql.functions import *
from subprocess import PIPE, Popen
import re
import urllib2

print "Creating task"
spark = SparkSession.builder.appName("test").getOrCreate()

print "Getting file"
response = urllib2.urlopen("http://www.gutenberg.org/files/36/36-0.txt")
data = response.read()
f_ = open("/tmp/test.txt","w")
f_.write(data)
f_.close()

print "Saving file to HDFS"
put = Popen(["hadoop", "fs", "-put", "/tmp/test.txt", "/in/sample.txt"], stdin=PIPE, bufsize=-1)
put.communicate()

print "Parsing"
strlen = spark.udf.register("stringLengthString", lambda x: len(x))
p = re.compile("[^EUIOAeuioaУЕЫАОЭЯИЮЁуеыаоэяиюё]")
strvowels = spark.udf.register("stringVowels", lambda x: p.sub("",x.lower()))
textFile = spark.read.text("/in/sample.txt")
result = textFile.select(explode(split(textFile.value,"\s+"))).where("stringLengthString(stringVowels(col)) >= 2").count()

print "RESULT:",result
```


### Usefull links:
```
How to Install and Set Up a 3-Node Hadoop Cluster https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/
Настройка маленького кластера Hadoop 2.2.0 с нуля https://habr.com/post/206196/
Hadoop-Spark-vagrant-ansible https://github.com/cybermaster/hadoop-spark-vagrant-ansible
Your cluster http://192.168.50.11:8088/cluster/apps
Install, Configure, and Run Spark on Top of a Hadoop YARN Cluster https://www.linode.com/docs/databases/hadoop/install-configure-run-spark-on-top-of-hadoop-yarn-cluster/
```


