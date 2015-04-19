#!/usr/bin/env python

##  Used for runing the HTTP server and the file watcher simultaneously
import threading
import time

##  sends the request to the receiving server and parses the request from the sending server
import urllib

##  listens to FSM server on incoming port
import http.server
import socketserver

##  watches the directory for changes, specifically new .log files (not yet implemented)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

##  Logging
import logging

##  Functions for handling/parsing HTTP requests
from ACSBridge_http import Handler

##  Configuration options
from ACSBridge_global import globalVars

##  Threading, for simultaneous file watching and socket serving
from multiprocessing import Process

############
##  MAIN  ##
############

def httpServe():
	##  set up a socketserver on the configured address running a Handler to handle GET/POST
	server = socketserver.TCPServer( ( globalVars['EXTERNAL_SERVER'], globalVars['PORT_IN'] ), Handler )

	print( "HTTP listener started on %s:%s" % server.server_address )
	globalVars['LOG'].info( "HTTP listener started on %s:%s" % server.server_address )
	##  continue serving until a keyboard interrupt is recieved
	server.serve_forever()

	#server.socket.close()


def watchFiles():
	return 0


def main():
	logging.basicConfig( filename=globalVars['LOG_PATH'], level=logging.DEBUG,
		format='%(asctime)s\t%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S' )
	globalVars['LOG'] = logging.getLogger( 'main' )

	print( "Logging to '%s'..." % globalVars['LOG_PATH'] )

	##  Set up the HTTP server to run in another thread
	httpThread = Process( target=httpServe )
	httpThread.start()

	try:
		while True:
			time.sleep(1)
	except (KeyboardInterrupt, SystemExit):
		print( "Keyboard interrupt recieved. Shutting down server." )
		globalVars['LOG'].info( "Keyboard interrupt recieved. Shutting down server." )
		httpThread.terminate()


if __name__ == '__main__':
	main()
