from kafka import KafkaProducer
import json
import os
import time
from datetime import datetime
import logging
# uncomment to see kafka module log
# logging.basicConfig(level=logging.DEBUG)



_topic='topic-test'
_num_message = 100

def produce_test_data():
	producer = KafkaProducer(bootstrap_servers='localhost:19092', 
		                     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
		                     retries=5)
	futures = []

	for i in range(_num_message):
		msg = {'event': '{0}'.format(i)}
		# print('sending: {}'.format(msg))
		futures.append(producer.send(_topic, msg))

	ret = [f.get(timeout=5) for f in futures]
	assert len(ret) == _num_message
	producer.close()


def run():
	while True:
		produce_test_data()
		time.sleep(2)

	


if __name__ == '__main__':
	run()