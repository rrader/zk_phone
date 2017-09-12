# run as user pi

git pull origin master
sudo killall zk_phone
sudo sh -c "nohup zk_phone" > foo.out 2> foo.err < /dev/null &
