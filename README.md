# KSELK

**K**afka - **S**park - **EL**asticsearch - **K**ibana

## How to run / simulate
On the terminal ONE
```sh
sh start
sh test/submit_sparkjob_py.sh
```
On the terminal TWO
```sh
python test/produce_data.py
```
Waint and have a look to the oputput and both terminal, eventually checek the links blow.
On the terminal TWO
```sh
CTRL-C
```
On the terminal ONE
```sh
sh stop.sh
```

***What happened?***
You runned in docker 
- Kafka
- Spark (with Jupyter Notebook)
- Elasticsearch
- Kibana
Then you subimitted and run
- an intercative spark job writen in python that consumes Kafka records and print to consolle 
Finally you have simultated the production of Kafka records.

***Usefull link***
- Jupiter notebook: ``` docker logs kselk_spark_1 | grep 127.0.0.1 | tail -1 ```
- Spark: [http://127.0.0.1:4040/](http://127.0.0.1:4040/)
- Elasticsearch: [http://127.0.0.1:9200/](http://127.0.0.1:9200/)
- Kibana: [http://127.0.0.1:9200/](http://127.0.0.1:9200/)