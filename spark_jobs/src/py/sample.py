import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.11:2.4.5,org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.5 pyspark-shell'

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import StructType
from pyspark.sql.types import StringType
from datetime import datetime

KAFKA_TOPIC_NAME_CONS = "topic-test"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'kafka:9092'

# Set Elasticsearch config
es_hostname='elasticsearch'
es_portno='9200'
es_doc_type_name='demo-index/doc'

spark = SparkSession \
    .builder \
    .appName("SSKafka") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Create DataFrame representing the stream of input lines from connection to localhost:9999
df_message = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS) \
    .option("subscribe", KAFKA_TOPIC_NAME_CONS) \
    .load()

print('Processing...')
# convert the data into string
df_message_string = df_message.selectExpr("CAST(value AS STRING) as value")

# define schema to read the Json format data
message_schema = StructType() \
    .add('event', StringType())    
# parse JSON data
df_message_string_parsed = df_message_string.select(from_json(df_message_string.value, message_schema).alias('msg_data'))
# https://kb.objectrocket.com/elasticsearch/how-to-create-a-timestamp-field-for-an-elasticsearch-index-275
# https://sparkbyexamples.com/spark/spark-dataframe-withcolumn/
df=df_message_string_parsed.withColumn('timestamp', current_timestamp())

# Start running the query that prints the running counts to the console
'''
queryConsolle = df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
queryConsolle.awaitTermination()
'''

queryElastic = df \
        .writeStream \
        .format("es") \
        .outputMode("append") \
        .option("es.nodes", es_hostname) \
        .option("es.port", es_portno) \
        .option("checkpointLocation", "checkpoint/send_to_es") \
        .option('es.resource', es_doc_type_name) \
        .start()

queryElastic.awaitTermination()


