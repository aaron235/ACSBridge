
##  sends the request to the receiving server and parses the request from the sending server
import urllib
##  listens to FSM server on incoming port
import http.server
import socketserver
##  Functions for handling CSV files
from ACSBridge_csv import writeCSV

##  Configuration options
from ACSBridge_global import globalVars

class Handler( http.server.SimpleHTTPRequestHandler ):
	"""
	A child of http.server.SimpleHTTPRequestHandler. Simply listens for
	GET/POST requests, and on recieve, it extracts the paramaters and
	writes them to a .csv file in the specified directory.
	"""
	def do_POST( self ):
		print( "POST request to " + self.path )
		globalVars['LOG'].info( "POST request to " + self.path )
		##  Parses out the request into a dictionary
		params = parsePOST( self.path )
		##  Writes the request paramaters to a .csv file
		writeCSV( params, globalVars['CCURE_DIR'] )
	def do_GET( self ):
		print( "GET request to " + self.path )
		globalVars['LOG'].info( "GET request to " + self.path )
		##  Parses out the request into a dictionary
		params = parsePOST( self.path )
		##  Writes the request paramaters to a .csv file
		writeCSV( params, globalVars['CCURE_DIR'] )


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
