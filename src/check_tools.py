## Execute this file to test if tools are up and running.

# Api for listening to bot commands.
import telebot
import time

# Be able to write trace to logfile.
import traceback

# Import own classes.
# Insert path to utils to allow importing them.
import os
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "utils"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "models"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "definitions"))

# Own Utils, classes and other imports.
import stateCheckUtils
import stringUtils
import logger as Logger
import databaseWrapper as DatabaseWrapper
import configUtils as ConfigUtils
import emailUtils as EmailUtils

## Initialize vars.

# Get config.
configUtils = ConfigUtils.ConfigUtils()

# Instantiate classes.
# Database connection.
dbWrapper = DatabaseWrapper.DatabaseWrapper()
# Logger.
logger = Logger.Logger("check_tools")

# Initialize bots.
botToken = configUtils.getTelegramBotToken()
bot = telebot.TeleBot(botToken, parse_mode="HTML")
errorChatIDs = configUtils.getTelegramErrorChatsIDs()
infoChatIDs = configUtils.getTelegramInfoChatsIDs()

# Initialize email messaging.
emailUtils = EmailUtils.EmailUtils()


# Handles error exceptions (log and info to admin).
def handleCommandException(exceptionLocationAndAdditionalInformation, exception):
    # Log error.
    errorLogText = exceptionLocationAndAdditionalInformation + " " + str(exception)

    # Add traceback to logfile.
    traceOfError = traceback.format_exc()
    logger.logError(str(traceOfError) + "\n" + errorLogText)

    # Send error message to admin telegram chat, if intended.
    if configUtils.areTelegramStatusMessagesEnabled():
        bot = telebot.TeleBot(botToken, parse_mode="HTML")
        for errorChatID in errorChatIDs:
            bot.send_message(errorChatID, errorLogText)

    # Send mails.
    emailUtils.send_error_mails(errorLogText)


# Info, that checking schedule is still taking place (log and info).
def infoCheckingToolsIsWorking(justStartedChecking=False, telegramTimeReached=False, emailTimeReached=False):
    # Create info text.
    infoLogText = "<b><u>Tools are being checked.</u></b>\nWebsites are being checked every <b>" + str(
        checkWebsitesEveryXMinutes) + "</b> minutes"
    if justStartedChecking:
        infoLogText += "\nJust (re-)started checking tools."
        
        # Telegram message enabled? -> Add frequency info.
        if configUtils.areTelegramStatusMessagesEnabled():
            infoLogText += "\n\nAbout every <b>" + str(telegramMessageEveryXMinutes) + "</b> minutes a status message should be send, to verify that this program is still working correctly."
        
        # Email message enabled? -> Add frequency info.
        if configUtils.areEmailStatusMessagesEnabled():
            infoLogText += "\n\nAbout every <b>" + str(emailMessageEveryXMinutes) + "</b> minutes a status message should be send, to verify that this program is still working correctly."
    else:
        infoLogText += "\n\nThis is an information to ensure, that the program is working correctly."
        
        # Telegram message enabled and telegramtimeReached? -> Add frequency info.
        if configUtils.areTelegramStatusMessagesEnabled() and telegramTimeReached:
            infoLogText += "\n\nThis message should show up again in " + str(
            telegramMessageEveryXMinutes) + " minutes, verifying that this program is still working correctly."
        
        # Email message enabled and emailtimeReached? -> Add frequency info.
        if configUtils.areEmailStatusMessagesEnabled() and emailTimeReached:
            infoLogText += "\n\nThis message should show up again in " + str(
            emailMessageEveryXMinutes) + " minutes, verifying that this program is still working correctly."

    infoLogText += "\nIf not -> Try to restart this program and take a look at the logs."

    # Add status message of checked tools.
    infoLogText += "\n\n" + stateCheckUtils.getToolStatesMessage()

    # Log information.
    logger.logInformation(infoLogText)

    # Send message to admin telegram chat, if enabled and time reached.
    if configUtils.areTelegramStatusMessagesEnabled() and (justStartedChecking or telegramTimeReached):

        # Does message have to be split?
        if len(infoLogText) > 4096:

            # Split message.
            individualMessages = stringUtils.splitLongTextIntoWorkingMessages(infoLogText)

            # Send messages.
            bot = telebot.TeleBot(botToken, parse_mode="HTML")
            for individualMessage in individualMessages:
                for infoChatID in infoChatIDs:
                    bot.send_message(infoChatID, individualMessage)

        else:
            # Message does not have to be split.
            bot = telebot.TeleBot(botToken, parse_mode="HTML")
            for infoChatID in infoChatIDs:
                bot.send_message(infoChatID, infoLogText)

    # Send mails.
    if justStartedChecking or emailTimeReached:
        emailUtils.send_info_mails(infoLogText)


## Check whether a scheduled countdown has to be sent.

# Only print every xth time, that we are still checking.
printEvery = 100

# When to send messages?
telegramMessageEveryXMinutes = configUtils.getTelegramStatusMessagesEveryXMinutes()
emailMessageEveryXMinutes = configUtils.getEmailStatusMessagesEveryXMinutes()

# How often to check websiteStates.
checkWebsitesEveryXMinutes = configUtils.getWebsiteChecksEveryXMinutes()
# How often to check google drive backups.
checkGoogleDriveEveryXMinutes = configUtils.getGoogleDriveChecksEveryXMinutes()

i = 0
print("checking ...")
infoCheckingToolsIsWorking(True)
while True:
    try:
        # Always recreate database to avoid disconnection error.
        dbWrapper = DatabaseWrapper.DatabaseWrapper()

        ## Info that checking of schedule is still taking place.

        # Increment counter.
        i = i + 1

        # Output to console.
        if (i % printEvery == 0):
            print("checking (" + str(i) + ") ...")

        # Update google drive backup states.
        if (i % checkGoogleDriveEveryXMinutes == 1):
            stateCheckUtils.updateGoogleDriveFolderBackupChecks()

        # Get states of tools.
        toolStateItems_api = stateCheckUtils.getToolStates_api()
        toolStateItems = toolStateItems_api
        toolStateItems += stateCheckUtils.getToolStates_backups()

        # Check websites.
        if (i % checkWebsitesEveryXMinutes == 1):
            toolStateItems += stateCheckUtils.getToolStates_websites()

        # Check the states of the tools.
        for toolStateItem in toolStateItems:

            # Is the tool up?
            if toolStateItem.toolIsUp == False:

                # Tool is down.

                # Has the error message already been sent?
                if toolStateItem.toolIsDownMessageHasBeenSent == False:

                    # The error message has not been sent yet.
                    # Output info.
                    print("Found tool, that is is down and message has not been sent yet..")
                    print(toolStateItem.name)
                    print("sending mesage now..")

                    # Indicate, that tool is down message has been sent.
                    if toolStateItem.isCustomCheck == True:
                        dbWrapper.updateWebsiteState(toolStateItem.name, "Down")
                        dbWrapper.updateWebsiteIsDownMessageHasBeenSentState(toolStateItem.name, 1)
                    elif toolStateItem.isBackupCheck == True:
                        # Indicate to DB, that message has been sent.
                        dbWrapper.updateBackupIsDownMessageHasBeenSentState(toolStateItem.name, 1)
                    else:
                        # Indicate to DB, that message has been sent.
                        dbWrapper.updateToolIsDownMessageHasBeenSentState(toolStateItem.name, 1)

                    # Send the message to the error message channel.
                    toolStateItemIsDownMsg = "Your tool is <b>DOWN!</b> \n\n<b>" + str(toolStateItem.name) + "</b>"
                    toolStateItemIsDownMsg += "" if toolStateItem.description == "" else "\n" + str(
                        toolStateItem.description)
                    toolStateItemIsDownMsg += "" if toolStateItem.statusMessage == "" or toolStateItem.statusMessage == "OK" else "\n" + str(
                        toolStateItem.statusMessage)
                    
                    # Send message to admin telegram chat, if enabled.
                    if configUtils.areTelegramStatusMessagesEnabled():
                        bot = telebot.TeleBot(botToken, parse_mode="HTML")
                        for errorChatID in errorChatIDs:
                            bot.send_message(errorChatID, toolStateItemIsDownMsg)

                    # Send mails.
                    emailUtils.send_error_mails(toolStateItemIsDownMsg)
                    


            else:

                # Tool is up.

                # Has there been an error cleared message already ?
                if toolStateItem.toolIsDownMessageHasBeenSent == True:

                    # There has been an error message recently.
                    # Output info.
                    print("Found tool, that is up again..")
                    print(toolStateItem.name)
                    print("sending message now..")

                    # Indicate, that tool is up message has been sent.
                    if toolStateItem.isCustomCheck == True:
                        dbWrapper.updateWebsiteState(toolStateItem.name, "Up")
                        dbWrapper.updateWebsiteIsDownMessageHasBeenSentState(toolStateItem.name, 0)
                    elif toolStateItem.isBackupCheck == True:
                        # Indicate to DB, that message has been sent.
                        dbWrapper.updateBackupIsDownMessageHasBeenSentState(toolStateItem.name, 0)
                    else:
                        # Indicate to DB, that message has been sent.
                        dbWrapper.updateToolIsDownMessageHasBeenSentState(toolStateItem.name, 0)

                    # Send the message to the error message channel.
                    toolStateItemIsUpAgainMsg = "Your tool is <b>UP AGAIN!</b> \n\n<b>" + str(
                        toolStateItem.name) + "</b>"
                    toolStateItemIsUpAgainMsg += "" if toolStateItem.description == "" else "\n" + str(
                        toolStateItem.description)
                    toolStateItemIsUpAgainMsg += "" if toolStateItem.statusMessage == "" or toolStateItem.statusMessage == "OK" else "\n" + str(
                        toolStateItem.statusMessage)
                    
                    # Send message to admin telegram chat, if enabled.
                    if configUtils.areTelegramStatusMessagesEnabled():
                        bot = telebot.TeleBot(botToken, parse_mode="HTML")
                        for errorChatID in errorChatIDs:
                            bot.send_message(errorChatID, toolStateItemIsUpAgainMsg)

                    # Send mails.
                    emailUtils.send_error_mails(toolStateItemIsUpAgainMsg)

        # Send info messages that tool is still checking.
        if (i % telegramMessageEveryXMinutes == 0):
            infoCheckingToolsIsWorking(telegramTimeReached=True)
        if (i % emailMessageEveryXMinutes == 0):
            infoCheckingToolsIsWorking(emailTimeReached=True)

        # Sleep 60 seconds with calculated offset.
        time.sleep(configUtils.calculateOffset(60))

    except Exception as e:
        handleCommandException("An Error occured while checking tools: ", str(e))

        # Sleep 60 seconds with calculated offset.
        time.sleep(configUtils.calculateOffset(60))
