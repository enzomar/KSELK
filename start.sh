echo "----------------------------"
echo " (re)Start Kafka -Spark - ELastic - Kibana "
echo "----------------------------"
docker-compose stop 
docker-compose build 

sudo sysctl -w vm.max_map_count=262144

docker-compose up -d
docker-compose ps

echo "----------------------------"
echo " Validate connections"
echo "----------------------------"
sleep 5
python test/validate.py
