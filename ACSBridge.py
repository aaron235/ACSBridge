#!/usr/bin/env python

from ACSBridgeLib.HTTPListener import HTTPListenerProcess
from ACSBridgeLib.DirWatcher import DirWatcherProcess
import ACSBridgeLib.DirWatcher

##  for loading configuration options
import yaml

##  for logging
import logging

from multiprocessing import Queue

def main():
	##  load config:
	f = open( 'config.yaml' )
	config = yaml.safe_load( f )
	f.close()

	##  Set up logging
	logging.basicConfig( filename=config['LOG_FILE'],
						 level=logging.DEBUG,
						 format='%(asctime)s\t%(levelname)s: %(message)s',
						 datefmt='%Y-%m-%d %H:%M:%S' )
	logger = logging.getLogger( 'main' )

	##  Set up process for HTTP listener
	HTTPQueue = Queue()
	HTTPProcess = HTTPListenerProcess( HTTPQueue, logger, config['PORT_IN'], config['PORT_OUT'], config['CCURE_DIR'] )

	HTTPProcess.run()

	DirWatcherQueue = Queue()
	DirWatcherProcess = DirWatcherProcess( DirWatcherQueue, logger, config['CCURE_DIR'], config['CCURE_LOG_PATTERN'],
		config['SMTP_SERVER'], config['SMTP_USER'], config['SMTP_PASS'] )

	try:
		while True:
			time.sleep(1)
	except (KeyboardInterrupt, SystemExit):
		logging.info( "Keyboard interrupt recieved. Shutting down server." )
		HTTPQueue.put( 1 )


##  run main
if __name__ == '__main__':
	main()
