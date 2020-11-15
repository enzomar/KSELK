docker exec -it kselk_spark_1 spark-submit \
             --packages org.apache.spark:spark-streaming-kafka-0-10_2.11:2.4.5,org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5,org.elasticsearch:elasticsearch-hadoop:7.7.1\
             --deploy-mode client \
             /home/jovyan/work/src/py/sample3.py
