from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import os
import time
import logging
import requests
# uncomment to see kafka module log
# logging.basicConfig(level=logging.DEBUG)



_topic='pdt.rail2'
_num_message = 100


def elastic_is_up():
	ret = requests.get('http://localhost:9200/_cluster/health?pretty')
	body = ret.json()
	return body['status'] != 'red'


def elastic_list_indexes():
	ret = requests.get('http://localhost:9200/_cat/indices')
	print('{0}'.format(ret.text.strip()))


def elastic_create_index(index):
	requests.put('http://localhost:9200/{0}'.format(index))

def elastic_delete_index(index):
	requests.delete('http://localhost:9200/{0}'.format(index))

def setup_deploy_spakr_job():
	os.system('sh rerun_spark.sh &')

def setup_send_to_kafka():
	producer = KafkaProducer(bootstrap_servers='localhost:9092', 
		                     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
		                     retries=5)
	futures = []

	for i in range(_num_message):
		msg = 'msg {0}'.format(i)
		# print('sending: {}'.format(msg))
		futures.append(producer.send(_topic, msg))

	ret = [f.get(timeout=5) for f in futures]
	assert len(ret) == _num_message
	producer.close()



def validate_kafka():
	consumer = KafkaConsumer(
	    _topic,
	    bootstrap_servers=['localhost:9092'],
	    auto_offset_reset='earliest',
	    value_deserializer=lambda x: json.loads(x.decode('utf-8')))
	received =list()
	for x in consumer:
		received.append(x.value)
	print('Consumed: {0}'.len(received))
	#print('produced: {0}, consumed: {1}'.format(_num_message, len(received)))
	#assert len(received) == _num_message
	
	consumer.close()

def read_from_elastic():
	pass





def run():
	#print("SETUP: update spark job")
	#setup_deploy_spakr_job()
	#time.sleep(1)
	#print("SETUP: populate kafka")
	#setup_send_to_kafka()
	#time.sleep(5)
	#print("VALIDATION: check kafka contains the sent data")
	#consume_kafka()
	elastic_is_up()
	#elastic_list_indexes()
	elastic_create_index('rail_all')
	#elastic_list_indexes()
	#elastic_delete_index('pippo')
	elastic_list_indexes()




if __name__ == '__main__':
	run()