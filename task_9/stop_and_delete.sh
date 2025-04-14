sudo docker stop nginx
sudo docker rm nginx

sudo docker stop app
sudo docker rm app

sudo docker stop database
sudo docker rm database


sudo docker rmi nginx_img
sudo docker rmi app_img
sudo docker rmi database_img
sudo docker network rm my_network