FILE_EXT=`basename "$1"`
FILE=`echo "$FILE_EXT" | cut -f 1 -d '.'`
docker exec -it kselk_scalac_1 scalac -d /tmp/spark_jobs/target/${FILE}.jar /tmp/spark_jobs/$1