docker-compose stop 
docker-compose build 

# sudo sysctl -w vm.max_map_count=262144

docker-compose up -d
docker-compose ps
sleep 5
echo 'Link to connect to Jupyter notebooks'
docker logs kselk_spark_1 | grep NotebookApp | grep 127.0.0.1:8888 | tail -1