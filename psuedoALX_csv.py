##  For writing files with the time as the name
import time

##  Configuration options
import psuedoALX_config

def writeCSV( params, writeDir ):
	csv = open( writeDir + time.strftime('%Y-%m-%d_%H:%M:%S') + ".csv", 'w' )
	csv.write( ','.join( params.keys() ) )
	csv.write( '\n' )
	csv.write( ','.join( params.values() ) )
	csv.close()
