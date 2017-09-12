# run as user pi

git pull origin master
sudo killall zk_phone
sudo sh -c "nohup zk_phone" &
