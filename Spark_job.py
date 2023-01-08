from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import pyspark.sql.functions as f
import os 
import pandas as pd
# Adding the packages required to get data from S3  
os.environ["PYSPARK_SUBMIT_ARGS"] = "--packages com.amazonaws:aws-java-sdk-s3:1.12.196,org.apache.hadoop:hadoop-aws:3.3.1 pyspark-shell"
# Creating our Spark configuration
conf = SparkConf() \
    .setAppName('S3toSpark') \
    .setMaster('local[*]')

sc=SparkContext.getOrCreate(conf=conf)

# Configure the setting to read from the S3 bucket
accessKeyId=os.environ["AWS_ACCESSKEY_ID"]
secretAccessKey=os.environ["AWS_SECRET_KEY"]
hadoopConf = sc._jsc.hadoopConfiguration()
hadoopConf.set('fs.s3a.access.key', accessKeyId)
hadoopConf.set('fs.s3a.secret.key', secretAccessKey)
hadoopConf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') # Allows the package to authenticate with AWS

# Create our Spark session
spark=SparkSession(sc)
# Read from the AWS S3 bucket
df = spark.read.json("s3a://pinterestdata7b8c2d40-08c6-4eb4-8c96-2f0080c4653b/*.json") 
df1 = df.select(df["category"],df["unique_id"],df["title"],df["description"],df["tag_list"],df["follower_count"]).show()

spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

# clean data 
df = df.withColumn('follower_count', f.regexp_replace("follower_count", "User Info Error", "0"))
df = df.withColumn('follower_count', f.regexp_replace("follower_count", "k", "000"))
df = df.withColumn('follower_count', f.regexp_replace("follower_count", "M", "000000"))
df = df.withColumn('follower_count', f.col("follower_count").cast("Int"))
df = df.withColumn('tag_list', f.regexp_replace("tag_list", "N,o, ,T,a,g,s, ,A,v,a,i,l,a,b,l,e", "None"))
df = df.sort("category").show() #show dataframe 