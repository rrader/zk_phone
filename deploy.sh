# run as user pi

sudo killall zk_phone || true
nohup sudo zk_phone > foo.out 2> foo.err < /dev/null &
