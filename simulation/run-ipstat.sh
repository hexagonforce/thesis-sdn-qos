sleeptime=330

sudo -u mininet ifstat -i switch1-eth5 -t -n > /home/mininet/thesis-code/simulation/test.results/ifstat-results.csv &

sleep $sleeptime;

sudo pkill -f ifstat &
exit 0
