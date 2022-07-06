# Using the test framework
- First, ping all the servers from all the clients to get the round-trip times.
- Second, Start the Python3 http servers my running the `server{n}HTTPStartup.sh`
- Run the `run_ipstat.sh` to gather ifstat from core switch to server switch.
- Start the VLC servers with `serverVLCStartup.sh {profile}`
- run the `python3 run-pings.py` to run pings
- run the `python3 run-ab-tests.py` to run all the ApacheBenchmark tests
- run `python3 run-vlc-clients.py` scripts according to the load configurations
- run the `python3 run-client-telnets.py` to make vlc measurements.
- Stop http clients.
- Stop VLC clients.
- Stop IFSTAT.
- Stop VLC servers.
- Stop http servers.

