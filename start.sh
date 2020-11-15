echo "----------------------------"
echo " (re)Start Kafka -Spark - ELastic - Kibana "
echo "----------------------------"
docker-compose stop 
docker-compose build 

# MEM CONFIG FOR RUNNING ELASTIC
if [ "$(uname)" == "Darwin" ]; then
	echo ' Ensure you made:'
	echo ' screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty'
	echo ' sysctl -w vm.max_map_count=262144'
	echo ' CTRL a d' 
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
	sudo sysctl -w vm.max_map_count=262144
fi
    

docker-compose up -d
docker-compose ps

echo "----------------------------"
echo " Validate connections"
echo "----------------------------"
sleep 8
python3 test/validate.py
