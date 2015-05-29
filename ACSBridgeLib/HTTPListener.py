##  enables this to be run as a Process
import multiprocessing

##  serve HTTP on a port
import http.server
import socketserver

##  parse the request
import urllib

##  for naming files
import time

class HTTPListenerProcess( multiprocessing.Process ):
	"""
	This class extends multiprocessing.Process, and when run, hosts an HTTP listener on
	the specified port, and writes all incoming requests to a CSV file in the specified directory.
	"""
	def __init__( self, queue, logger, portIn, portOut, writeDir ):
		self.queue = queue
		self.logger = logger
		self.portIn = portIn
		self.portOut = portOut
		self.writeDir = writeDir


	def run( self ):
		handler = HTTPHandler
		handler.setLogger( handler, self.logger )
		handler.setWriteDir( handler, self.writeDir )
		server = socketserver.TCPServer( ( '', self.portIn ), handler )

		self.logger.info( "HTTP listener started on %s:%s" % server.server_address )
		##  Set the server to only handle_request() for this long
		server.timeout = 0.5

		while True:
			server.handle_request()
			if not self.queue.empty():
				code = self.queue.get()
				if code == 1:
					server.socket.close()
					break

class HTTPHandler( http.server.SimpleHTTPRequestHandler ):
	"""
	A child of http.server.SimpleHTTPRequestHandler. Simply listens for
	GET/POST requests, and on recieve, it extracts the paramaters and
	writes them to a .csv file in the specified directory.
	"""

	def setLogger( self, logger ):
		"""
		needed to give this HTTPHandler its own logging object
		"""
		self.logger = logger

	def setWriteDir( self, writeDir ):
		"""
		needed to give this HTTPHandler its own WriteDir
		"""
		self.writeDir = writeDir

	def do_POST( self ):
		"""
		On a POST request, this method will accept the request, parse its paramaters, and write
		them as CCure-readable CSV into the specified directory.
		"""
		self.logger.info( "POST request to " + self.path )
		##  Parses out the request into a dictionary
		params = parseParams( self.path )
		##  Writes the request paramaters to a .csv file
		if self.isValidRequest( params ):
			self.writeCSV( params )
			self.send_response( 200 )
			self.send_header('Content-type', 'text/html')
        	self.end_headers()
        	self.wfile.write('<html><body><pre>OK</pre></body></html>')
		else:
			logging.warning( "Invalid POST paramaters sent, ignoring request." )

	##	suppresses logging to the console; I've already got that covered
	def log_message(self, format, *args):
		return None

	def do_GET( self ):
		self.logger.info( "GET request to " + self.path )
		##  Parses out the request into a dictionary
		params = self.parseParams( self.path )
		##  Writes the request paramaters to a .csv file
		if self.isValidRequest( params ):
			self.writeCSV( params )
			self.send_response( 200 )
			self.send_header('Content-type', 'text/html')
        	self.end_headers()
        	self.wfile.write('<html><body><pre>OK</pre></body></html>')
		else:
			logging.warning( "Invalid GET paramaters sent, ignoring request." )


	def writeCSV( self, params ):
		"""
		Takes a dictionary 'params' and formats params' keys into one row of CSV, and
		the values into another row of CSV. It then writes them to writeDir, in a .csv
		file named with the date.
		"""
		nowTime = time.strftime( '%Y-%m-%d_%H:%M:%S' )
		csv = open( self.writeDir + nowTime + ".csv", 'w' )
		csv.write( ','.join( params.keys() ) + '\n' + ','.join( params.values() ) )
		csv.close()
		self.logger.info( "Wrote CSV file " + self.writeDir + nowTime + ".csv" )

	def parseParams( self, request ):
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

	def isValidRequest( self, params ):
		"""
		Returns True if the passed set is a set of request paramaters, otherwise
		returns False.
		"""
		for item in params.keys():
			if item == "":
				return False
		for item in params.values():
			if item == "":
				return False
		return True
