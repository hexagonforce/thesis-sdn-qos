#*************************************************************
# Description: Python Program for starting up VLC Streaming Media server
#              in Video-On-Demand mode via telnet session.
# Filename   : telnetStartVLCServer.py
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py via command line.
#*************************************************************
import sys, getopt
import telnetlib, time
import socket
import re
import logging
from threading import Event, Thread
import os.path, os
from datetime import date, datetime, timedelta

logging.basicConfig(level=logging.DEBUG,
                    filename='telnetStartVLC.log', 
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')

logging.info("\n\n")
# Global Variables
timeout = 120

logging.info("Attempting  to start telnet vlc")

# Main method when launched.
def main(argv):
    port = 4212
    clientname = "localhost"
    vlm_file = ""

    logging.info("ARGV: {}".format(argv))
    vlmfile = f'{argv}.vlm'
    # if argv == "BBB":
    #     vlm_file = "BBBVLCConfig.vlm"
    # elif argv == "Gfriend":
    #     vlm_file = "GfriendVLCConfig.vlm"
    # elif argv == "Spring":
    #     vlm_file = "SpringVLCConfig.vlm"

    vlm_load = b"load /home/mininet/thesis-code/simulation/{vlm_file}"

    logging.info ("Connecting...")
    try:
        session = telnetlib.Telnet(clientname, port, timeout)
    except socket.timeout:
        logging.info ("socket timeout")
    else:
        output = session.read_until(b"Password:", timeout)
        logging.info("First output: {}".format(output))
        session.write(b"mininet" + b"\r\n")
        output = session.read_until(b">", timeout )
        logging.info("Second output: {}".format(output))
        session.write(vlm_load + b"\r\n")
        eager = session.read_very_eager()
        output = session.read_until(b">", timeout )
        logging.info("Loading BBBVLCConfig output: {}".format(output))
        logging.info("Detailed Output: {}".format(eager))
        session.write(b"show media" + b"\r\n")
        media = session.read_very_eager()
        logging.info("Media: {}".format(media))
        session.write(b"quit" + b"\r\n")
        
        session.close()
        logging.info("Closing Session")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))







    