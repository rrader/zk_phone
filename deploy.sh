# run as user pi

git pull origin master
sudo killall zk_phone
sudo su -c "nohup zk_phone &"