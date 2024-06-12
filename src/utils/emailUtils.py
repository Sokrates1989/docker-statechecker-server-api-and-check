# Sends emails.

# Email specific imports.
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get environment variables.
import configUtils as ConfigUtils

# Definitions.
from valid_values import VALID_SMTP_PORTS



class EmailUtils:

    def __init__(self, useDateStringUtils=True):
        """
        Constructor for utils class to send emails.
        
        Args:
            useDateString (bool): Whether to use the datestringUtils or not. Prevents an infinite loop from datestringUtils.
        """
        # Get config.
        configUtils = ConfigUtils.ConfigUtils()

        # Unknown service indicator.
        self._unknownServiceIndicator = "Global"
        
        # Are E-Mail status messages enabled?
        self._email_enabled = configUtils.areEmailStatusMessagesEnabled()
 
        # Setup email sender and recipients.
        if self._email_enabled:
            self._sender={}

            # Sender User.
            self._sender["user"] = configUtils.getEmailSenderUser()

            # Sender Password.
            self._sender["password"] = configUtils.getEmailSenderPassword()

            # Sender Host.
            self._sender["host"] = configUtils.getEmailSenderHost()

            # Sender Port.
            self._sender["port"] = configUtils.getEmailSenderPort()
            if self._sender["port"] not in VALID_SMTP_PORTS:
                self._email_enabled = False

            # Default Recipients.
            self._recipients={}
            self._recipients["error"] = configUtils.getEmailErrorAdresses()
            self._recipients["info"] = configUtils.getEmailInfoAdresses()
            

        # Test sender login.
        if self._email_enabled:
            smpt_login_successful=self._test_smtp_login(self._sender)
            if smpt_login_successful != True:
                self._email_enabled = False
    

    def send_error_mails(self, message):
        if self._email_enabled:
            for error_mail in self._recipients["error"]:
                self._send_email(self._sender, error_mail, "State Checker Error", message)

    def send_info_mails(self, message):
        if self._email_enabled:
            for info_mail in self._recipients["info"]:
                self._send_email(self._sender, info_mail, "State Checker Information", message)

    def _test_smtp_login(self, sender):
        try:
            if (sender["port"]) not in VALID_SMTP_PORTS: 
                raise Exception("Port %s not one of %s" % (sender["port"], VALID_SMTP_PORTS))

            if sender["port"] in (465,):
                server = smtplib.SMTP_SSL(sender["host"], sender["port"])
            else:
                server = smtplib.SMTP(sender["host"], sender["port"])

            # Optional.
            server.ehlo()

            if sender["port"] in (587,): 
                server.starttls()
                
            server.login(sender["user"], sender["password"])
            server.quit()
            return True
        except Exception as e:
            return f"SMTP login failed. Error: <EMPHASIZE_STRING_START_TAG>{e}</EMPHASIZE_STRING_END_TAG>"


    def _send_email(self, sender, recipient_email, subject, message):

        # Set up the MIME.
        msg = MIMEMultipart()
        msg['From'] = sender["user"]
        msg['To'] = recipient_email
        msg['Subject'] = subject

        try:
            if sender["port"] not in VALID_SMTP_PORTS: 
                raise Exception("Port %s not one of %s" % (sender["port"], VALID_SMTP_PORTS))

            if sender["port"] in (465,):
                server = smtplib.SMTP_SSL(sender["host"], sender["port"])
            else:
                server = smtplib.SMTP(sender["host"], sender["port"])

            # Optional.
            server.ehlo()

            if sender["port"] in (587,): 
                server.starttls()

        except Exception as e:
            return e

        server.login(sender["user"], sender["password"])

        # Make message html.
        message = "<html><body>" + message + "</html></body>"

        # Replace new linnes \n with <br/> to make them work with html.
        message = message.replace("\n", "<br/>")

        # Replace emphasize String Tags.
        message=message.replace("<EMPHASIZE_STRING_START_TAG>", "<b>")
        message=message.replace("</EMPHASIZE_STRING_END_TAG>", "</b>")

        # Attach message.
        msg.attach(MIMEText(message, 'html'))

        # Send the email.
        server.sendmail(sender["user"], recipient_email, msg.as_string())

        # Close the connection.
        server.quit()
