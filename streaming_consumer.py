from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import col,from_json,max,min
import os
import pyspark.sql.functions as f
from json import loads
os.environ["PYSPARK_SUBMIT_ARGS"] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.3,org.postgresql:postgresql:42.5.0 streaming_consumer.py pyspark-shell'
password = os.environ["PGADMIN4_PASSWORD"]
kafka_topic_name = "MyFirstKafkaTopic"
kafka_bootstrap_servers = 'localhost:9092'

spark = SparkSession \
    .builder \
    .appName("Kafka")   \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

data_df = spark \
    .readStream \
    .format("Kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic_name) \
    .option("startingOffsets","earliest")  \
    .load()



def foreach_batch_function(df, epoch_id):
    df = df.withColumn('follower_count', f.regexp_replace("follower_count", "User Info Error", "0"))
    df = df.withColumn('follower_count', f.regexp_replace("follower_count", "k", "000"))
    df = df.withColumn('follower_count', f.regexp_replace("follower_count", "M", "000000"))
    df = df.withColumn('follower_count', f.col("follower_count").cast("Int"))
    df = df.withColumn('tag_list', f.regexp_replace("tag_list", "N,o, ,T,a,g,s, ,A,v,a,i,l,a,b,l,e", "None"))
    maxValueA = df.agg(max("follower_count")).collect()[0][0]
    #df.select(("*")).write.format("console").mode("append").save()
    df.write \
        .format("jdbc") \
        .mode("append")   \
        .option("url", "jdbc:postgresql://localhost:5432/pinterest_streaming") \
        .option("dbtable", "experimental_data_1") \
        .option("user", "postgres") \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .save()
    #print(f"{maxValueA} is max follower count")
    
schema = StructType([
        StructField("category",StringType(),True),
        StructField("index",StringType(), True),
        StructField("unique_id",StringType(), True),
        StructField("title",StringType(), True),
        StructField("description",StringType(), True),
        StructField("follower_count",StringType(), True),
        StructField("tag_list",StringType(), True),
        StructField("is_image_or_video",StringType(), True),
        StructField("image_src",StringType(), True),
        StructField("downloaded",StringType(), True),
        StructField("save_location",StringType(), True),
    ])


#data_df.select(data_df("value"))
#data_df.writeStream.foreachBatch(foreach_batch_function).start().awaitTermination()
data_df = data_df.selectExpr("CAST (value as STRING)")
data_df = data_df.withColumn("value",from_json(col("value"),schema)).select(col("value.*")) 
#data_df.writeStream.format("console").outputMode("update").start().awaitTermination()
data_df.writeStream.foreachBatch(foreach_batch_function).start().awaitTermination()