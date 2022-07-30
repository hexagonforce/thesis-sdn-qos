#*************************************************************
# Description: Python Program for processing VLC results via 
#              telnet client session.
# Filename   : vlcrctelnetclient.py
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py via shell script.
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
                    filename='vlcrctelnetclient.log', 
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')

logging.info("\n\n")
logging.info("Starting")
# Global Variables
newlinechar = b'\r\n'
host="localhost"
portint=4313
timeout = 120
filename = "/home/mininet/thesis-code/simulation/test.results/vlc-clients"
clientname = ""
target_server = ""
datetimestr=""
endtimestr=""
endtime = datetime.now() + timedelta(seconds=600)
runtype=""
usecase=0
queuecase = "0.0"
loadcase = 0

rawdata=""
averagedata=""

totalsamples=0

demuxbytesread = 0.00
demuxbitrate = 0.00
demuxcorrupted = 0.00
framesdisplayed = 0.00
frameslost = 0.00
buffersplayed = 0.00
bufferslost = 0.00

totdemuxbytesread = 0.00
totdemuxbitrate = 0.00
totdemuxcorrupted = 0.00
totframesdisplayed = 0.00
totframeslost = 0.00
totbuffersplayed = 0.00
totbufferslost = 0.00

avedemuxbitrate = 0.00
avedemuxcorrupted = 0.00
aveframesdisplayed = 0.00
aveframeslost = 0.00
avebuffersplayed = 0.00
avebufferslost = 0.00

cancel_future_calls = Event().set

# Method to parse parameter value given a start and end string identifiers within string text.
def getParamValue(string, start, end):
    result = 0.00
    try:
        result = re.search(f'{start}(.*){end}', string).group(1)
        # result = re.search('%s(.*)%s' % (start, end), string)
        logging.info(f"getParamValue RESULT: {result}\tType: {type(result)}")
    except AttributeError as err:
        logging.info("AttributeError: {}".format(err))
        result = "0.00"
    return result

# Method to query telnet session to local VLC server on localhost every 5 seconds and add to totals.
def queryViaTelnet(session):
    global newlinechar, clientname, portint, runtype, rawdata, timeout, endtime, totalsamples, demuxbytesread, demuxbitrate, demuxcorrupted, framesdisplayed, frameslost, buffersplayed, bufferslost, totdemuxbytesread, totdemuxbitrate, totdemuxcorrupted, totframesdisplayed, totframeslost, totbuffersplayed, totbufferslost

    session.write(b"get_title"+ newlinechar)
    title = session.read_until(b">", timeout)
    logging.info(f"queryViaTelnet Current Stream: {title}")
    
    session.write(b"stats" + newlinechar)
    
    output = session.read_until(b">", timeout)
    logging.info(f"Stats: {output}")
    
    if datetime.now() <= endtime:
        logging.info("Getting Stats. Please Please Please")
        
        if output.strip() == "" or output.strip() == ">":
            session.write(b"stop" + newlinechar)
            session.write(b"goto 0" + newlinechar)
            output = session.read_until(b">", timeout )
            logging.info(f"Restart: goto 0: {output}")
    
            session.write(b"play" + newlinechar)
            output = session.read_until(b">", timeout )
            logging.info(f"Restart: play: {output}")
    
            session.write(b"is_playing" + newlinechar)
            output = session.read_until(b">", timeout )
            logging.info(f"Restart: is_playing: {output}")
            # Open Output File
            output = session.read_until(b">", timeout)

            session.write(b"get_title" + newlinechar)
            title = session.read_until(b">", timeout)
            logging.info(f"queryViaTelnet if output empty Current Stream: {title}")
        
        session.write(b"stats" + newlinechar)
        output = session.read_until(b">", timeout)
        logging.info(f"Here Here: Session: {session}\nDatetime Checking Stats: {output}")

        # Add to total samples done.
        totalsamples+=1

        # Parse Data
        strdemuxbytesread = getParamValue(output, "demux bytes read :", " KiB").strip()
        strdemuxbitrate = getParamValue(output, "demux bitrate    :", " kb/s").strip()
        strdemuxcorrupted = getParamValue(output, "demux corrupted  :", "\n").strip()
        strframesdisplayed =  getParamValue(output, "frames displayed :", "\n").strip()
        strframeslost =  getParamValue(output, "frames lost :", "\n").strip()
        strbuffersplayed =  getParamValue(output, "buffers played   :", "\n").strip()
        strbufferslost =  getParamValue(output, "buffers lost     :", "\n").strip()
            
        demuxbytesread = 0.00
        demuxbitrate = 0.00
        demuxcorrupted = 0.00
        framesdisplayed = 0.00
        frameslost = 0.00
        buffersplayed = 0.00
        bufferslost = 0.00

        try:
            demuxbytesread = float(strdemuxbytesread)
            demuxbitrate = float(strdemuxbitrate)
            demuxcorrupted = float(strdemuxcorrupted)
            framesdisplayed = float(strframesdisplayed)
            frameslost = float(strframeslost)
            buffersplayed = float(strbuffersplayed)
            bufferslost = float(strbufferslost)
        
            # Add to totals
            totdemuxbytesread = demuxbytesread
            totdemuxbitrate+=demuxbitrate
            totdemuxcorrupted+=demuxcorrupted
            totframesdisplayed+=framesdisplayed
            totframeslost+=frameslost
            totbuffersplayed+=buffersplayed
            totbufferslost+=bufferslost
            
            rawline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s" % (clientname, portint, runtype, totalsamples, demuxbytesread, demuxbitrate, demuxcorrupted, framesdisplayed, frameslost, buffersplayed, bufferslost, newlinechar)
            rawdata+=rawline
            
        except ValueError:
            logging.info("Could not read statistics from Telnet.")
    else:
        logging.info("Session Done")
        handleSessionEnd(session)
        
# Method to handle each VLC telnet session to each host, including closing down telnet session, averaging data, writing to file, and killing process of telnet clients on each host.
def handleSessionEnd(session):
    global newlinechar, cancel_future_calls, portint, filename, clientname, host, datetimestr, usecase,  queuecase, loadcase, runtype, rawdata, averagedata, totalsamples, totdemuxbytesread, totdemuxbitrate, totdemuxcorrupted, totframesdisplayed, totframeslost, totbuffersplayed, totbufferslost, avedemuxbitrate, avedemuxcorrupted, aveframesdisplayed, aveframeslost, avebuffersplayed, avebufferslost

    cancel_future_calls()

    session.write(b"shutdown" + newlinechar)
    session.close()
    logging.info("Closing Session")
    
    if totalsamples > 0:
        avedemuxbitrate = totdemuxbitrate/totalsamples
        avedemuxcorrupted = totdemuxcorrupted/totalsamples
        aveframesdisplayed = totframesdisplayed/totalsamples
        aveframeslost = totframeslost/totalsamples
        avebuffersplayed = totbuffersplayed/totalsamples
        avebufferslost = totbufferslost/totalsamples
    
    averagedata = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s" % (usecase, loadcase, queuecase, runtype, datetimestr, clientname, host, portint, totalsamples, totdemuxbytesread, avedemuxbitrate, avedemuxcorrupted, aveframesdisplayed, aveframeslost, avebuffersplayed, avebufferslost, newlinechar)

    rawdataheader = "%s\t-\t-" % clientname
    completerawdata = "%s" % rawdata
    storeFiles(completerawdata, averagedata)


# Method to store results into raw and aggregated  VLC csv files.
def storeFiles(rawdata, averagedata):
    global filename, clientname, target_server, datetimestr, usecase, queuecase, loadcase, newlinechar

    logging.info(f"Store Files: {filename}\t{datetimestr}\t{usecase}\t")

    rawdatafilename = f'{filename}/{clientname}->{target_server}vlc-run-results-raw.csv'
    averagedatafilename = f'{filename}/vlc-run-results-ave-{usecase}-{loadcase}-{queuecase}.csv'

    logging.info("Raw File: {}".format(rawdatafilename))
    logging.info("AVG File: {}".format(averagedatafilename))

    if not os.path.isfile(rawdatafilename):
        rawdata = "Client Name\tPort Used\tRequest Type\tTotal Samples\tDemux Bytes Read\tDemux Bitrate\tDemux Corrupted\tFrames Displayed\tFrames Lost\tBuffers Played\tBuffers Lost%s%s" % (newlinechar, rawdata)
        
    targetrd = open(rawdatafilename, 'a')
    targetrd.write(rawdata)
    targetrd.close()

    if not os.path.isfile(averagedatafilename):
        averagedata = "Use Case\tLoad Configuration\tQueue Configuration\tRequest Type\tRun Date\tClient Name\tHost IP\tPort Used\tTotal Samples\tDemux Bytes Read\tDemux Bitrate\tDemux Corrupted\tFrames Displayed\tFrames Lost\tBuffers Played\tBuffers Lost%s%s" % (newlinechar, averagedata)
        
    targetad = open(averagedatafilename, 'a')
    targetad.write(averagedata)
    targetad.close()

# Method to call telnet session querying for statistics every n interval secondsl.
def call_repeatedly(interval, func, *args):
    logging.info("ARGS: {}".format(*args))
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # The first call is in `intervals seconds
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

# Main method when launched.
def main(argv):
    global cancel_future_calls, host, portint, timeout, filename, clientname, target_server, datetimestr, endtime, runtype, usecase, queuecase, loadcase, rawdata, averagedata, totalsamples, demuxbitrate, demuxcorrupted, framesdisplayed, frameslost, buffersplayed, bufferslost, totdemuxbitrate, totdemuxcorrupted, totframesdisplayed, totframeslost, totbuffersplayed, totbufferslost, avedemuxbitrate, avedemuxcorrupted, aveframesdisplayed, aveframeslost, avebuffersplayed, avebufferslost

    # Get command line arguments.
    port = 4313
    clientname = "localhost"
    usecasestr ="0"
    loadcasestr = "0"
    endtimestr = ""
    try:
        opts, args = getopt.getopt(argv,"p:c:s:d:t:h:u:q:l:e:",["port=","clientname=","server=", "datetime=","type=","host=","usecase=","queuecfg=","loadcfg=","endtime="])
        logging.info ("opts: {}\nargs: {}".format(opts, args))
    except getopt.GetoptError as err:
        logging.info("ERR: {}".format(err))
        # sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--port"):
            port = arg
        elif opt in ("-c", "--clientname"):
            clientname = arg
        elif opt in ("-s", "--server"):
            target_server = arg
        elif opt in ("-d", "--datetime"):
            datetimestr = arg
        elif opt in ("-t", "--type"):
            runtype = arg
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-u", "--usecase"):
            usecasestr = arg
        elif opt in ("-q", "--queuecfg"):
            queuecase = arg
        elif opt in ("-l", "--loadcfg"):
            loadcasestr = arg
        elif opt in ("-e", "--endtime"):
            endtimestr = arg
            logging.info ("endtimesr: {}".format(endtimestr))
    
    logging.info("Starting Client...")
    logging.info("Port: %s" % port)
    logging.info("Clientname: %s" % clientname)
    logging.info("Target Server: %s" % target_server)
    logging.info("DateTime: %s" % datetimestr)
    logging.info("RunType: %s" % runtype)
    logging.info("Host: %s" % host)
    logging.info("UseCase: %s" % usecasestr)
    logging.info("QueueCase: %s" % queuecase)
    logging.info("LoadCase: %s" % loadcasestr)
    logging.info("EndTime: %s" % endtimestr)
    
    # Cast some command line arguments to proper type.
    try:
        portint = int(port)
        usecase = usecasestr
        loadcase = int(loadcasestr)
        endtime = datetime.strptime(endtimestr, "%m%d%Y%H%M%S")
        logging.info(" Try Try\nHost: {}\tPort: {}\tUse Case: {}\tLoad Case: {}\tEnd Time: {}".format(host, portint, usecase, loadcase, endtime))
    except ValueError:
        logging.info("Could not convert case argument to a valid case. Using Default.")
    
    # Start telnet session.
    logging.info ("Connecting...")
    try:
        print(host, portint, timeout)
        session = telnetlib.Telnet(host, portint, timeout)
        logging.info("Session: {}".format(session))

    except socket.timeout:
        logging.info ("socket timeout")
    else:
        output = session.read_until(b">", timeout )
        logging.info("Sending Commands...")
        session.write(b"stop" + newlinechar)
        output = session.read_until(b">", timeout )
        logging.info("STOP: {}".format(output))
        session.write(b"goto 0" + newlinechar)
        output = session.read_until(b">", timeout )
        logging.info("goto 0: %s" % output)
        output = session.read_until(b">", timeout )

        session.write(b"play" + newlinechar)
        output = session.read_until(b">", timeout )
        logging.info("play: %s" % output)

        session.write(b"is_playing" + newlinechar)
        output = session.read_until(b">", timeout )
        logging.info("is_playing: %s" % output)

        session.write(b"get_title" + newlinechar)
        title = session.read_until(b">", timeout)
        logging.info("Current Stream: {}".format(title))
        # Open Output File

        session.write(b"stats" + newlinechar)
        output = session.read_until(b">", timeout)
        logging.info("Main Stats: {}".format(output))
        
        # For Every 5 seconds until output.trim is ""
        cancel_future_calls = call_repeatedly(5, queryViaTelnet, session)
        logging.info("Cancelled Calls")
        
        logging.info("Spawning Threads Per 5 Second Interval.")
        

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
