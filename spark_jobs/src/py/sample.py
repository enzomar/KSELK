import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0,org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0 pyspark-shell'

from ast import literal_eval

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("SSKafka") \
    .getOrCreate()
    
# default for startingOffsets is "latest", but "earliest" allows rewind for missed alerts    
dsraw = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "topic-test") \
  .option("startingOffsets", "earliest") \
  .load()

ds = dsraw.selectExpr("CAST(value AS STRING)")

print(type(dsraw))
print(type(ds))