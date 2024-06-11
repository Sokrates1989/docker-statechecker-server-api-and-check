### Logs information and errors both in day based files and one big file. LogPath: PATH/TO/PRICETRACKER/logs/

## Imports.
# For file operations with operating system.
import os

## Own Modules.
# For creating files.
import fileUtils
# For getting datestrings.
import dateStringUtils


class Logger:

	# Constructor creating logfiles and paths.
	def __init__(self, logScope="check_tools"):

		# What am I logging stuff for?
		if logScope == "check_tools":
			self.logtext_info = "TOOLCHECKER_INFO"
			self.logtext_warning = "TOOLCHECKER_WARNING"
			self.logtext_error = "TOOLCHECKER_ERROR"
		else:
			self.logtext_info = "UNKNOWN_INFO"
			self.logtext_warning = "UNKNOWN_WARNING"
			self.logtext_error = "UNKNOWN_ERROR"

		# Global logs.
		self.logPath = os.path.join("/code" , "logs")
		self.globalErrorLogFile = os.path.join(self.logPath , "errorlog.txt")
		self.globalLogFile = os.path.join(self.logPath , "log.txt")
		fileUtils.createFileIfNotExists(self.globalErrorLogFile)
		fileUtils.createFileIfNotExists(self.globalLogFile)

		# Daybased logs.
		self.dayLogPath = os.path.join(self.logPath, "dayBased")
		self.updateDayBasedLogFilePaths()
		

	# Create dayBased logfile paths.
	def updateDayBasedLogFilePaths(self):
		dateStringForLogFileName = dateStringUtils.getDateStringForLogFileName()
		dayBasedErrorLogFileName = dateStringForLogFileName + "_errorlog.txt"
		dayBasedLogFileName = dateStringForLogFileName + "_log.txt"
		self.dayBasedErrorLogFile = os.path.join(self.dayLogPath , dayBasedErrorLogFileName)
		self.dayBasedLogFile = os.path.join(self.dayLogPath , dayBasedLogFileName)
		fileUtils.createFileIfNotExists(self.dayBasedErrorLogFile)
		fileUtils.createFileIfNotExists(self.dayBasedLogFile)


	## Logs an Error to 4 logfiles.
	# Logs to globalErrorLogFile, globalLogFile, dayErrorLogFile and dayLogFile.
	# Log entry will look like this: [2022-03-31 22:02:04] - [PYTHON_ERROR] - [errorToLog]
	def logError(self, errorToLog):

		# Always update day based log files first.
		self.updateDayBasedLogFilePaths()

		# Prepare full log text.
		fullLogText = "\n" + dateStringUtils.getDateStringForLogTag() + " - " + "[" + self.logtext_error + "]" + " - [" + errorToLog + "]"

		# write fullLogText to both info and error logs (day and global log files)
		self._log(self.globalErrorLogFile, fullLogText)
		self._log(self.globalLogFile, fullLogText)
		self._log(self.dayBasedErrorLogFile, fullLogText)
		self._log(self.dayBasedLogFile, fullLogText)

		# Print message to CLI.
		self._print_log_message(fullLogText)


	## Logs a Warning to 4 logfiles.
	# Logs to globalErrorLogFile, globalLogFile, dayErrorLogFile and dayLogFile.
	# Log entry will look like this: [2022-03-31 22:02:04] - [PYTHON_WARNING] - [warningToLog]
	def logWarning(self, warningToLog):

		# Always update day based log files first.
		self.updateDayBasedLogFilePaths()

		# Prepare full log text.
		fullLogText = "\n" + dateStringUtils.getDateStringForLogTag() + " - " + "[" + self.logtext_warning + "]" + " - [" + warningToLog + "]"

		# write fullLogText to both info and error logs (day and global log files)
		self._log(self.globalErrorLogFile, fullLogText)
		self._log(self.globalLogFile, fullLogText)
		self._log(self.dayBasedErrorLogFile, fullLogText)
		self._log(self.dayBasedLogFile, fullLogText)

		# Print message to CLI.
		self._print_log_message(fullLogText)


	## Logs an Information to 2 logfiles.
	# Logs to globalLogFile and dayLogFile.
	# Log entry will look like this: [2022-03-31 22:02:04] - [PYTHON_INFO] - [informationToLog]
	def logInformation(self, informationToLog):

		# Always update day based log files first.
		self.updateDayBasedLogFilePaths()

		# Prepare full log text.
		fullLogText = "\n" + dateStringUtils.getDateStringForLogTag() + " - " + "[" + self.logtext_info + "]" + " - [" + informationToLog + "]"

		# write fullLogText info logs (day and global log files)
		self._log(self.globalLogFile, fullLogText)
		self._log(self.dayBasedLogFile, fullLogText)

		# Print message to CLI.
		self._print_log_message(fullLogText)


	# PRIVATE function write a string to a file
	def _log(self, file, fullLogText):
		with open(file, 'a+') as f:
			f.write("\n" + fullLogText)
	
	

	def _print_log_message(self, message_to_print:str):
		"""
		Print message to cli.

		Replaces Special tags to improve output.

		Args:
			message_to_print (str): The message to pring.
		"""
		# String replacements.
		message_to_print=message_to_print.replace("<EMPHASIZE_STRING_START_TAG>", "\"")
		message_to_print=message_to_print.replace("</EMPHASIZE_STRING_END_TAG>", "\"")

		# Print message.
		print(message_to_print)
