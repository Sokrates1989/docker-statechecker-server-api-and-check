from enum import Enum

class LogLevel(Enum):
    INFO = "INFO"
    VERBOSE = "VERBOSE"
    IMPORTANT_ONLY = "IMPORTANT_ONLY"

class MessageLevel(Enum):
    IMPORTANT = ("IMPORTANT", "‼️")
    ERROR = ("ERROR", "🛑")
    WARNING = ("WARNING", "⚠️")
    INFO = ("INFO", "ℹ️")
    VERBOSE = ("VERBOSE", "🔍")
    
    def __init__(self, level, icon):
        self.level = level
        self.icon = icon

    def __str__(self):
        return f'{self.icon} {self.level}'
    
    def get_lowercase_representation_with_icon(self):
        return f'{self.icon} {str(self.level).lower()}'

class MessagingPlatforms(Enum):
    LOGGING = "LOGGING"
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"


VALID_SMTP_PORTS = (25, 587, 465)

