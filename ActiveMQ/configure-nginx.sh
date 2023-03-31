host=$(docker exec activemq hostname -i)
sed "s/hostname/$host/g" default.conf > default-$host.conf
docker cp default-$host.conf nginx-activemq:/etc/nginx/conf.d/default.conf
docker exec nginx-activemq service nginx reload
rm -rf default-$host.conf