#!/usr/bin/env python

##  sends the request to the receiving server
import urllib.request
##  parses the request from the sending server
import urllib.parse
##  listens to FSM server on incoming port
import socket
##  watches the directory for changes, specifically new .csv files
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileSystemEventHandler
##  Logging
import logging
##  Keeps daemon alive
import time

##  incoming and outgoing ports
PORT_IN = 80
PORT_OUT = 81

##  directory to watch for changes
WATCH_DIR = './'

##  URL of external server
EXTERNAL_SERVER = 'http://localhost:' + str( PORT_OUT )

##  Logging
LOG_PATH = './psuedoALX.log'

############
##  MAIN  ##
############

class CCureFileEvent( FileSystemEventHandler ):
	def on_created( self, event ):
		csv = open( event.src_path, r )

##  Set up logging
logging.basicConfig( filename=LOG_PATH, level=logging.DEBUG,
					format='%(asctime)s\t%(levelname)s: %message',
					datefmt='%Y-%m-%d %H:%M:%S' )
print( "Logging to '%s'..." % LOG_PATH )


CCureFileEventHandler = CCureFileEvent()

observer = Observer()
observer.schedule( CCureFileEventHandler, WATCH_DIR )
observer.start()
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	observer.stop()
observer.join()
################
##  FUNCTIONS ##
################

def parsePOST( request ):
	"""
	Accepts a string "request" that contains a URL with POST paramaters,
	and returns a dictionary representing request's POST paramaters.
	"""
	##  grabs and splits the paramaters of the request of the URL
	paramString = parse.urlParse( s ).params
	pairs = paramString.split( '&' )

	params = dict()

	##  divides each paramater into a tuple of its key and its value, decodes
	##  their URL encoding, and adds them to tuplePairs
	for pair in pairs:
		pairList = pair.split( '=' )
		##  set a value in the params dictionary. The key is the first value of the
		##  pair, the value is the second
		params[ parse.unquote( pairList[0] ) ] =  parse.unquote( pairList[1] )

	return params


def parseCSV( s ):
	"""
	Accepts a string of comma separated values, and returns a list of tuples
	representing the fields in the comma separated values as key-values, with
	the top row as the keys, and one dictionary for each set of values.
	"""

	lines = s.split( '\n' )

	rows = []

	for line in lines:
		values = line.split( ',' )
		rows.append( values )

	keySet = rows[0]
	valueSets = rows [1:]

	paramsList = []

	for values in valueSets:
		params = dict()
		for i in xrange( 0, keySet.length ):
			params[keySet[i]] = valueSets[i]
		paramsList.append( params )


	return paramsList


def formatPOST( url, params ):
	"""
	accepts a string "url" which this request is to be formatted to, and a
	dictionary "params" to add as a POST request to this URL.
	"""

	url += '?'
	for param in params.keys():
		url += parse.quote( param ) + '=' + parse.quote( params[param] ) + '&'

	##  remove the trailing '&'
	url = url[:-2]

	return url


def formatCSV( params ):
	csvString = ','.join( params.keys() )
	csvString += "\n"
	csvString += ','.join( params.items() )

	return csvString


def FSMtoCCure( params ):
	return params


def CCuretoFSM( params ):
	return params
