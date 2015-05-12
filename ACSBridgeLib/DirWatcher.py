##  to extend from and run this as a Process
import multiprocessing

##	for watching the directory for new file writes
import watchdog

##	send emails
import smtplib
##  format the emails as the right mimetype
from email.mime.text import MIMEText

class DirWatcherProcess( multiprocessing.Process ):

	def __init__( self, queue, logger, watchDir, watchPattern, smtpServer, smtpUser, smtpPass ):
		self.queue = queue
		self.logger = logger
		self.watchDir = watchDir
		self.watchPattern = watchPattern
		self.smtpServer = smtpServer
		self.smtpUser = smtpUser
		self.smtpPass = smtpPass

##	def run( self ):
		fileWatcher = watchdog.Observer()
		observer.schedule( function_handle, watchDir, recursive=False )
