sudo docker stop app
sudo docker rm app
sudo docker stop database
sudo docker rm database
sudo docker rmi app_img
sudo docker rmi database_img
sudo docker network rm my_network