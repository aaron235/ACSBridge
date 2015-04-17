#!/usr/bin/env python

##  Used for runing the HTTP server and the file watcher simultaneously
import threading

##  sends the request to the receiving server and parses the request from the sending server
import urllib

##  listens to FSM server on incoming port
import http.server
import socketserver

##  watches the directory for changes, specifically new .log files (not yet implemented)
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

##  Logging
import logging

##  Functions for handling/parsing HTTP requests
from psuedoALX_HTTP import Handler

##  Configuration options
from psuedoALX_config import config


############
##  MAIN  ##
############


def main():
	##  Set up logging
	logging.basicConfig( filename=config['LOG_PATH'], level=logging.DEBUG,
		format='%(asctime)s\t%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S' )
	print( "Logging to '%s'..." % config['LOG_PATH'] )

	try:
		##  set up a socketserver on the configured address running a Handler to handle GET/POST
		server = socketserver.TCPServer( ( config['EXTERNAL_SERVER'], config['PORT_IN'] ), Handler )

		print( "HTTP listener started on {server}:{port}".format( server=server.server_address[0], port=server.server_address[1] ) )
		logging.info( "HTTP listener started on {server}:{port}".format( server=server.server_address[0], port=server.server_address[1] ) )
		##  continue serving until a keyboard interrupt is recieved
		server.serve_forever()

	except (KeyboardInterrupt, SystemExit):
		print( "Keyboard interrupt recieved. Shutting down server." )
		logging.info( "Keyboard interrupt recieved. Shutting down server." )
		server.socket.close()

if __name__ == '__main__':
    main()
