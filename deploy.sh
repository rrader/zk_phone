# run as user pi

sudo killall zk_phone
sudo sh -c "nohup zk_phone" > foo.out 2> foo.err < /dev/null &
