from kafka import KafkaProducer
import json
import os
import requests


def kafka_is_up():
	producer = KafkaProducer(bootstrap_servers='127.0.0.1:19092', 
		                     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
		                     retries=5)
	futures = []

	msg = {'health_check':1}
	# print('sending: {}'.format(msg))
	futures.append(producer.send('test', {'action':msg}))

	ret = [f.get(timeout=10) for f in futures]	
	producer.close()
	return len(ret) == 1


def elastic_is_up():
	ret = requests.get('http://localhost:9200/_cluster/health?pretty')
	body = ret.json()
	return body['status'] != 'red'

def health_check():
	elastic = elastic_is_up()
	kafka = kafka_is_up()

	print('Kafka: {0}'.format(elastic))
	print('Elastic: {0}'.format(kafka))

	return elastic and kafka

def run():
	print('Health check')
	health_check()	
	


if __name__ == '__main__':
	run()