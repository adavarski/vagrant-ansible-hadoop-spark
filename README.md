# Hadoop + Spark
 Hadoop cluster with Spark (vagrant + ansible)
 - Spark job for counting words with 2 and more vowels https://github.com/adavarski/vagrant-ansible-hadoop-spark/blob/master/cluster/playbooks/files/calc.py

# Steps to create a cluster

 -   Clone the repository
 -   cd cluster/
 -   vagrant up
 -   sh install_getfiles.sh
 -   ansible-playbook -i inventory/vagrant-4hosts.inv playbooks/hadoop.yml
 -   ssh -i ~/.vagrant.d/insecure_private_key vagrant@192.168.50.[11:13]
     1.Add swapfile:
     $ sudo fallocate -l 2G /swapfile
     $ sudo chmod 600 /swapfile
     $ sudo mkswap /swapfile
     $ sudo swapon /swapfile
     $ sudo swapon -s
     2. Define slaves in etc/hadoop/slaves on master
     vagrant@hadoopmaster:/usr/local/hadoop-2.9.1$ cat etc/hadoop/slaves 
     192.168.50.11
     192.168.50.12
     3.Setup RM port 
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

# How to test Hadoop cluster

 -   Prepare hdfs: bin/hdfs namenode -format
 -   Cleate input dir for data: bin/hdfs dfs -mkdir /in
 -   Put some info in it: bin/hdfs dfs -copyFromLocal /home/vagrant/books/* /in
 -   Run example: bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.9.1.jar wordcount /in /out
 -   See results: bin/hdfs dfs -ls /out
 -   Remove results: bin/hdfs dfs -rm -R /out

# How to test Spark cluster

 -   vm# spark-shell
 -   ss# var input = spark.read.textFile("/in/somefile.txt")
 -   ss# input.filter(line => line.length()>0).count()
