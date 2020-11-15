echo "----------------------------"
echo " (re)Start Kafka -Spark - ELastic - Kibana "
echo "----------------------------"
docker-compose stop 
docker-compose build 

# INSTALL ELASTIC
# if MAC ...
#
# screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty
# sysctl -w vm.max_map_count=262144
# CTRL a d 
#
# if linux
sudo sysctl -w vm.max_map_count=262144
#     

docker-compose up -d
docker-compose ps

echo "----------------------------"
echo " Validate connections"
echo "----------------------------"
sleep 5
python3 test/validate.py
