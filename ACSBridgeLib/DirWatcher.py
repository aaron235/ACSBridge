##  to extend from and run this as a Process
import multiprocessing

##	for watching the directory for new file writes
import watchdog

##	send emails
import smtplib
##  format the emails as the right mimetype
from email.mime.text import MIMEText

class DirWatcherProcess( multiprocessing.Process ):
	"""
	This class extends multiprocessing.Process, and when run, watches the specified directory
	for new files that match the pattern (typically /.+\.log/). On write, it will detect if
	the new file is a CCure error log, and if it is, it will send it as an email from the
	configured address, to the configured address.
	"""
	def __init__( self, queue, logger, watchDir, watchPattern, smtpServer, smtpUser, smtpPass ):
		self.queue = queue
		self.logger = logger
		self.watchDir = watchDir
		self.watchPattern = watchPattern
		self.smtpServer = smtpServer
		self.smtpUser = smtpUser
		self.smtpPass = smtpPass

##	def run( self ):
##		fileWatcher = watchdog.Observer()
##		observer.schedule( self.sendLog, self.watchDir, recursive=False )

##	def setupMail( self ):
##	"""
##
##  """

##  def sendLog( self, logMessage ):
##	"""
##
##	"""
