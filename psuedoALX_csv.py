##  For writing files with the time as the name
import time

##  Configuration options
import psuedoALX_config

def writeCSV( params, writeDir ):
	"""
	Takes a dictionary 'params' and a directory to write to 'writeDir'
	and formats params' keys into one row of CSV, and the values into another row of
	CSV. It then writes them to the directory, in a .csv file named with the date.
	"""
	csv = open( writeDir + time.strftime( '%Y-%m-%d_%H:%M:%S' ) + ".csv", 'w' )
	csv.write( ','.join( params.keys() ) )
	csv.write( '\n' )
	csv.write( ','.join( params.values() ) )
	csv.close()
