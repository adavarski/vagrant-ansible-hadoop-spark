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

