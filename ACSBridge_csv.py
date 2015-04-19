##  For writing files with the time as the name
import time

##  Configuration options
from ACSBridge_global import globalVars

def writeCSV( params, writeDir ):
	"""
	Takes a dictionary 'params' and a directory to write to 'writeDir'
	and formats params' keys into one row of CSV, and the values into another row of
	CSV. It then writes them to the directory, in a .csv file named with the date.
	"""
	nowTime = time.strftime( '%Y-%m-%d_%H:%M:%S' )
	csv = open( writeDir + nowTime + ".csv", 'w' )
	csv.write( ','.join( params.keys() ) )
	csv.write( '\n' )
	csv.write( ','.join( params.values() ) )
	csv.close()
	globalVars['LOG'].info( "Wrote CSV file " + writeDir + nowTime + ".csv" )
