sudo docker network create my_network
sudo docker build -t app_img -f Dockerfile_API .
sudo docker build -t database_img -f Dockerfile_database .
sudo docker build -t nginx_img -f Dockerfile_nginx .

sudo docker run --name database --network my_network -p 5433:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=12345rcpc -e POSTGRES_DB=urls -d database_img

sleep 5

sudo docker run --name app --network my_network --link database -p 8001:8001 -d app_img

sudo docker run --name nginx --network my_network -p 80:80 -d nginx_img