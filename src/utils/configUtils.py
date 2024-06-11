## Config operations like getting config array or other config Values.

# For accessing google drive.
from __future__ import print_function
from oauth2client.service_account import ServiceAccountCredentials

# Interaction with operating system (read write files).
import os

# For getting config.
import json

# For safely parsing json string to dict (https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary).
import ast


class ConfigUtils:
    """
    Get any configuration settings.
    """
    # Constructor creating logfiles and paths.
    def __init__(self):
          
        try:
            config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config.txt")
            config_file = open(config_file_pathAndName)
            self._config_array = json.load(config_file)
        except:
            # Get config array from Environment Variable.
            statechecker_server_config = os.getenv("STATECHECKER_SERVER_CONFIG")
            if statechecker_server_config:
                self._config_array = json.loads(statechecker_server_config)
            else:
                # If neither the file nor the environment variable is found, raise an error or handle it appropriately
                raise ValueError("configUtils: Could not get config array from config.txt nor environment variable STATECHECKER_SERVER_CONFIG")


    def getConfigArray(self):
        """
        Get the configuration array.

        Just for debugging. Please use direct methods for individual configuration items.

        Returns:
            (array): Confiuration array.
        """
        return self._config_array
    

    def getTolerencePeriodInSeconds(self):
        """
        Get tools using api tolerence period in seconds.

        Returns:
            (int): Tolerence period in seconds.
        """
        tools_using_api_tolerance_period_in_seconds=os.getenv("TOOLS_USING_API_TOLERANCE_PERIOD_IN_SECONDS")
        if tools_using_api_tolerance_period_in_seconds:
            tools_using_api_tolerance_period_in_seconds = tools_using_api_tolerance_period_in_seconds.strip().strip("\"")
        else:
            if "toolsUsingApi_tolerancePeriod_inSeconds" in self._config_array:
                tools_using_api_tolerance_period_in_seconds = self._config_array["toolsUsingApi_tolerancePeriod_inSeconds"]
        return int(tools_using_api_tolerance_period_in_seconds)
    

    def getWebsitesToCheck(self):
        """
        Get websites to check.

        Returns:
            (array): Websites to check.
        """
        websites_to_check=os.getenv("WEBSITES_TO_CHECK")
        if websites_to_check:
            websites_to_check = [item.strip() for item in websites_to_check.strip().strip("\"").split(',')]
        else:
            if "websites" in self._config_array:
                if "websitesToCheck" in self._config_array["websites"]:
                    websites_to_check = self._config_array["websites"]["websitesToCheck"]
        return websites_to_check


    
    ## DB Con ##
    def getDatabaseHost(self):
        """
        Get database host.

        Returns:
            (str): Host where db is.
        """
        db_host=os.getenv("DB_HOST")
        if db_host:
            db_host = db_host.strip().strip("\"")
        else:
            if "database" in self._config_array:
                if "host" in self._config_array["database"]:
                    db_host = self._config_array["database"]["host"]
        return db_host
    
    def getDatabaseUser(self):
        """
        Get database user.

        Returns:
            (str): Database user.
        """
        db_user=os.getenv("DB_USER")
        if db_user:
            db_user = db_user.strip().strip("\"")
        else:
            if "database" in self._config_array:
                if "user" in self._config_array["database"]:
                    db_user = self._config_array["database"]["user"]
        return db_user
    
    def getDatabasePassword(self):
        """
        Get database password.

        Returns:
            (str): Database password of database user.
        """
        db_pw=""
        try:
            DB_PW_FILE = os.getenv("DB_PW_FILE")
            with open(f"{DB_PW_FILE}", "r") as db_pw_file:
                db_pw = db_pw_file.read().strip()
        except:
            pass
        finally:
            # In case of an error or the secret is not set.
            if not db_pw or db_pw.lower() == "none":
                db_pw = os.getenv('DB_PW').strip().strip("\"")
        if not db_pw or db_pw == "":
            # Get PW from config.
            if "database" in self._config_array:
                if "password" in self._config_array["database"]:
                    db_pw = self._config_array["database"]["password"]

        return db_pw
    
    def getDatabaseName(self):
        """
        Get database name.

        Returns:
            (str): Name of database.
        """
        db_name=os.getenv("DB_NAME")
        if db_name:
            db_name = db_name.strip().strip("\"")
        else:
            if "database" in self._config_array:
                if "database" in self._config_array["database"]:
                    db_name = self._config_array["database"]["database"]
        return db_name
    
    # Telegram settings.
    def getTelegramBotToken(self):
        """
        Get telegram bot token.

        Returns:
            (str): Token for the bot.
        """
        bot_token=""
        try:
            TELEGRAM_SENDER_BOT_TOKEN_FILE = os.getenv("TELEGRAM_SENDER_BOT_TOKEN_FILE")
            with open(f"{TELEGRAM_SENDER_BOT_TOKEN_FILE}", "r") as bot_token_file:
                bot_token = bot_token_file.read().strip()
        except:
            pass
        finally:
            # In case of an error or the secret is not set.
            if not bot_token or bot_token.lower() == "none":
                bot_token = os.getenv('TELEGRAM_SENDER_BOT_TOKEN').strip().strip("\"")
        if not bot_token or bot_token == "":
            # Get PW from config.
            if "telegram" in self._config_array:
                if "botToken" in self._config_array["telegram"]:
                    bot_token = self._config_array["telegram"]["botToken"]

        return bot_token



    def getTelegramErrorChatsIDs(self):
        """
        Get chat ids to send error messages to.

        Returns:
            (array): Chat ids for errors.
        """
        errorChatIDs=os.getenv("TELEGRAM_RECIPIENTS_ERROR_CHAT_IDS")
        if errorChatIDs:
            errorChatIDs = [item.strip() for item in errorChatIDs.strip().strip("\"").split(',')]
        else:
            if "telegram" in self._config_array:
                if "errorChatIDs" in self._config_array["telegram"]:
                    errorChatIDs = [item.strip() for item in self._config_array["telegram"]["errorChatIDs"].strip().strip("\"").split(',')]
                elif "errorChatID" in self._config_array["telegram"]:
                    errorChatIDs=[]
                    errorChatIDs.append(self._config_array["telegram"]["errorChatID"])
        return errorChatIDs


    def getTelegramInfoChatsIDs(self):
        """
        Get chat ids to send info messages to.

        Returns:
            (array): Chat ids for info messages.
        """
        infoChatIDs=os.getenv("TELEGRAM_RECIPIENTS_INFO_CHAT_IDS")
        if infoChatIDs:
            infoChatIDs = [item.strip() for item in infoChatIDs.strip().strip("\"").split(',')]
        else:
            if "telegram" in self._config_array:
                if "infoChatIDs" in self._config_array["telegram"]:
                    infoChatIDs = [item.strip() for item in self._config_array["telegram"]["infoChatIDs"].strip().strip("\"").split(',')]
                elif "infoChatID" in self._config_array["telegram"]:
                    infoChatIDs=[]
                    infoChatIDs.append(self._config_array["telegram"]["infoChatID"])
        return infoChatIDs
    

    # Status Messages.
    def getStatusMessagesTimeOffsetPercentage(self):
        """
        Get time offset besed on the amount of time the calculation handling takes, to make every x minutes more accurate.

        Returns:
            (float): percentage value to adjust time every x minutes.
        """
        telegramStatusMessageEveryXMinutes=os.getenv("STATUS_MESSAGES_TIME_OFFSET_PERCENTAGE")
        if telegramStatusMessageEveryXMinutes:
            telegramStatusMessageEveryXMinutes = telegramStatusMessageEveryXMinutes.strip().strip("\"")
        else:
            if "telegram" in self._config_array:
                if "adminStatusMessage_operationTime_offsetPercentage" in self._config_array["telegram"]:
                    telegramStatusMessageEveryXMinutes = self._config_array["telegram"]["adminStatusMessage_operationTime_offsetPercentage"]
        return float(telegramStatusMessageEveryXMinutes)
    

    # Telegram.
    def areTelegramStatusMessagesEnabled(self):
        """
        Are telgram status messages enabled?

        Returns:
            (bool): Whether telegram status messages are enabled.
        """
        areTelegramStatusMessagesEnabled=os.getenv("TELEGRAM_ENABLED")
        if areTelegramStatusMessagesEnabled:
            areTelegramStatusMessagesEnabled = areTelegramStatusMessagesEnabled.strip().strip("\"").lower() == "true"
        else:
            areTelegramStatusMessagesEnabled = True
        return int(areTelegramStatusMessagesEnabled)
    

    def getTelegramStatusMessagesEveryXMinutes(self):
        """
        Get amount of minutes when to send telegram status messages.

        Send telegram status messages every x minutes based on this value.

        Returns:
            (int): Amount of minutes between each telegram status message.
        """
        telegramStatusMessageEveryXMinutes=os.getenv("TELEGRAM_STATUS_MESSAGES_EVERY_X_MINUTES")
        if telegramStatusMessageEveryXMinutes:
            telegramStatusMessageEveryXMinutes = telegramStatusMessageEveryXMinutes.strip().strip("\"")
        else:
            if "telegram" in self._config_array:
                if "adminStatusMessage_everyXMinutes" in self._config_array["telegram"]:
                    telegramStatusMessageEveryXMinutes = self._config_array["telegram"]["adminStatusMessage_everyXMinutes"]
        return int(telegramStatusMessageEveryXMinutes)
    

    # Email.
    def areEmailStatusMessagesEnabled(self):
        """
        Are email status messages enabled?

        Returns:
            (bool): Whether email status messages are enabled.
        """
        areEmailStatusMessagesEnabled=os.getenv("EMAIL_ENABLED")
        if areEmailStatusMessagesEnabled:
            areEmailStatusMessagesEnabled = areEmailStatusMessagesEnabled.strip().strip("\"").lower() == "true"
        else:
            areEmailStatusMessagesEnabled = True
        return int(areEmailStatusMessagesEnabled)
    
    def getEmailStatusMessagesEveryXMinutes(self):
        """
        Get amount of minutes when to send email status messages.

        Send email status messages every x minutes based on this value.

        Returns:
            (int): Amount of minutes between each email status message.
        """
        emailStatusMessageEveryXMinutes=os.getenv("TELEGRAM_STATUS_MESSAGES_EVERY_X_MINUTES")
        if emailStatusMessageEveryXMinutes:
            emailStatusMessageEveryXMinutes = emailStatusMessageEveryXMinutes.strip().strip("\"")
        else:
            emailStatusMessageEveryXMinutes = 60
            if "email" in self._config_array:
                if "adminStatusMessage_everyXMinutes" in self._config_array["email"]:
                    emailStatusMessageEveryXMinutes = self._config_array["email"]["adminStatusMessage_everyXMinutes"]
        return int(emailStatusMessageEveryXMinutes)

    

    # Check Frequency.
    def getWebsiteChecksEveryXMinutes(self):
        """
        How often to check websiteStates?

        Returns:
            (int): Amount of minutes between each website checks.
        """
        websiteChecksEveryXMinutes=os.getenv("CHECK_WEBSITES_EVERY_X_MINUTES")
        if websiteChecksEveryXMinutes:
            websiteChecksEveryXMinutes = websiteChecksEveryXMinutes.strip().strip("\"")
        else:
            websiteChecksEveryXMinutes = 30
            if "websites" in self._config_array:
                if "checkWebSitesEveryXMinutes" in self._config_array["websites"]:
                    websiteChecksEveryXMinutes = self._config_array["websites"]["checkWebSitesEveryXMinutes"]
        return int(websiteChecksEveryXMinutes)
    

    # Google Drive.
    def getGoogleDriveFoldersToCheck(self):
        """
        Get google drive folders to check.

        Returns:
            (array): Google drive folders to check.
        """
        foldersToCheck = []
        if "googleDrive" in self._config_array:
            if "foldersToCheck" in self._config_array["googleDrive"]:
                foldersToCheck = self._config_array["googleDrive"]["foldersToCheck"]
        return foldersToCheck
    

    def getGoogleDriveServiceAccountCredentials(self):
        """
        Get google drive service account credentials.

        Returns:
            (credentials): Google drive service account credentials.
        """
        scope = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        swarm_credentials_secret_json = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_FILE")
        credentials = ""

        # If deployed via swarm -> use secret file, if not use service_account_key.json nin main directory.
        if swarm_credentials_secret_json == "/run/secrets/SET THIS ENVIRONMENT VAR IN SWARM DEPLOY ENVIRONMENTS":
            credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account_key.json', scope)
        else:
            GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_FILE = swarm_credentials_secret_json
            with open(f"{GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_FILE}", "r") as googleDriveServiceAccountJson_file:
                googleDriveServiceAccountJson_dict = ast.literal_eval(googleDriveServiceAccountJson_file.read().strip())
                credentials = ServiceAccountCredentials. from_json_keyfile_dict(googleDriveServiceAccountJson_dict, scope)
    
        return credentials
    
    
    def getGoogleDriveChecksEveryXMinutes(self):
        """
        How often to check google drive folders?

        Returns:
            (int): Amount of minutes between each goolge drive folder checks.
        """
        googleDriveChecksEveryXMinutes=os.getenv("CHECK_GOOGLEDRIVE_EVERY_X_MINUTES")
        if googleDriveChecksEveryXMinutes:
            googleDriveChecksEveryXMinutes = googleDriveChecksEveryXMinutes.strip().strip("\"")
        else:
            googleDriveChecksEveryXMinutes = 60
            if "googleDrive" in self._config_array:
                if "checkFilesEveryXMinutes" in self._config_array["googleDrive"]:
                    googleDriveChecksEveryXMinutes = self._config_array["googleDrive"]["checkFilesEveryXMinutes"]
        return int(googleDriveChecksEveryXMinutes)
    

