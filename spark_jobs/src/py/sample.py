''''
Taken from: 
https://mtpatter.github.io/bilao/notebooks/html/01-spark-struct-stream-kafka.html

note that the jar file 
org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1
Is aligned to teh current spark version 3.0.1
'''

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 pyspark-shell'

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

# print(type(dsraw))
# print(type(ds))


rawQuery = dsraw \
        .writeStream \
        .queryName("qraw")\
        .format("memory")\
        .start()

raw = spark.sql("select * from qraw")
raw.show() 

'''

raw.write.format("es") \
  .option("es.resource", "rail_all") \
  .option("es.nodes", "elasticsearch:9200") \
  .save()

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('ES_indexer').getOrCreate()
df = spark.createDataFrame([{'num': i} for i in xrange(10)])
df = df.drop('_id')
df.write.format(
    'org.elasticsearch.spark.sql'
).option(
    'es.nodes', 'http://spark-data-push-adertadaltdpioy124.us-west-2.es.amazonaws.com'
).option(
    'es.port', 9200
).option(
    'es.resource', '%s/%s' % ('index_name', 'doc_type_name'),
).save()

'''


'''
# Write toe elastic search

es_write_conf = {
        "es.nodes" : "localhost",
        "es.port" : "9200",
        "es.resource" : 'walker/apache',
        "es.input.json": "yes",
        "es.mapping.id": "doc_id"
    }

rdd2 = rdd.map(parse)

rdd3 = rdd2.map(addID    
       
rdd3.saveAsNewAPIHadoopFile(
        path='-',
        outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",       
        keyClass="org.apache.hadoop.io.NullWritable",
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
        conf=es_write_conf)

rdd3 = rdd2.map(addID

'''