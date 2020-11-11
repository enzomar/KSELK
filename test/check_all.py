from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import os
import time
import logging
import requests
# uncomment to see kafka module log
# logging.basicConfig(level=logging.DEBUG)



_topic='topic-test'
_num_message = 100


def kafka_is_up():
	producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092', 
		                     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
		                     retries=5)
	futures = []

	msg = 'health_check'
	# print('sending: {}'.format(msg))
	futures.append(producer.send('test', msg))

	ret = [f.get(timeout=5) for f in futures]	
	producer.close()
	return len(ret) == 1


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

def submit_sparkjob():
	os.system('sh submit_sparkjob_py.sh')

def produce_test_data():
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


def health_check():
	elastic = elastic_is_up()
	kafka = kafka_is_up()

	print('Kafka: {0}'.format(elastic))
	print('Elastic: {0}'.format(kafka))

	return elastic and kafka


def setup():
	elastic_create_index('rail_all')

def run():
	print('Health check')
	health_check()
	print('Setup')
	setup()
	#print('Submit spark job')
	#submit_sparkjob()
	print('Produce test data')
	produce_test_data()

	


if __name__ == '__main__':
	run()