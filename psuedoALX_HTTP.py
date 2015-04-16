
##  sends the request to the receiving server and parses the request from the sending server
import urllib
##  listens to FSM server on incoming port
import http.server
import socketserver
##  Functions for handling CSV files
from psuedoALX_csv import writeCSV

##  Configuration options
from psuedoALX_config import config

class Handler( http.server.SimpleHTTPRequestHandler ):
	def do_POST( self ):
		print( "POST request to " + self.path )
		##  Parses out the request into a dictionary
		params = parsePOST( self.path )
		##  Writes the request paramaters to a .csv file
		writeCSV( params, config['CCURE_DIR'] )
	def do_GET( self ):
		print( "GET request to " + self.path )
		##  Parses out the request into a dictionary
		params = parsePOST( self.path )
		##  Writes the request paramaters to a .csv file
		writeCSV( params, config['CCURE_DIR'] )


def parsePOST( request ):
	"""
	Accepts a string "request" that contains a URL with POST paramaters,
	and returns a dictionary representing request's POST paramaters.
	"""
	##  grabs and splits the paramaters of the request of the URL
	paramString = urllib.parse.urlparse( request ).query
	pairs = paramString.split( '&' )
	params = dict()

	##  divides each paramater into a tuple of its key and its value, decodes
	##  their URL encoding, and adds them to tuplePairs
	for pair in pairs:
		pairList = pair.split( '=' )
		##  set a value in the params dictionary. The key is the first value of the
		##  pair, the value is the second
		params[ urllib.parse.unquote( pairList[0] ) ] = urllib.parse.unquote( pairList[1] )

	return params