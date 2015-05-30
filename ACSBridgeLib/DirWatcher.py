##  to extend from and run this as a Process
import multiprocessing

##	for watching the directory for new file writes
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

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
	def __init__( self, queue, logger, watchDir, watchPattern, smtpServer, smtpUser, smtpPass, mailFrom, mailTo ):
		self.queue = queue
		self.logger = logger
		self.watchDir = watchDir
		self.watchPattern = watchPattern
		##  set up emailing
		self.mailer = smtplib.SMTP( smtpServer )
		self.mailer.starttls()
		self.mailer.login( smtpUser, smtpPass )
		self.mailFrom = mailFrom
		self.mailTo = mailTo


	def run( self ):
		event_handler = LoggingEventHandler()
		fileWatcher = Observer()
		fileWatcher.schedule( event_handler, self.watchDir, recursive=False )
		fileWatcher.start()

		##  logWriteEvent.src_path == './log_file.log'

		self.logger.info( "Directory watcher started, watching " + self.watchDir )

		self.sendMail( """This is a test of the automated ACSBridge error reporter! An email from this
			address will mean that something is wrong with the CCure server. This message,
			however, is just a test of the SMTP mailing system. Have a nice day!""" )

	def sendLog( self ):
		return None

	def sendMail( self, message ):
		self.logger.info( "Sending email to configured addresses" )
		for address in self.mailTo:
			self.mailer.sendmail( self.mailFrom, address, message )

##	def setupMail( self ):
##	"""
##
##	"""

##  def sendLog( self, logMessage ):
##	"""
##
##	"""
