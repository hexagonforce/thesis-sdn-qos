sleeptime=330

sudo -u mininet ifstat -i switch10-eth2 -t -n > /home/mininet/thesis-code/simulation/test.results/ifstat-results.csv &

sleep $sleeptime;

sudo pkill -f ifstat &
exit 0
