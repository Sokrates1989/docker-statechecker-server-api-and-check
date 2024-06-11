# Model to wrap state of website and whether that state has been sent to admin.

# To convert class to json and back.
import json


class WebsiteStateAndMessageSentItem:

    # Constructor.
    def __init__(self, name, state="Down", isDownMessageHasBeenSent=True):
        self.name = name
        self.state = state
        self.isDownMessageHasBeenSent = isDownMessageHasBeenSent

    def asMap(self):
        return {
            "name": self.name,
            "state": self.state,
            "isDownMessageHasBeenSent": self.isDownMessageHasBeenSent,
        }

    def toJson(self):
        return json.dumps(self.asMap())


    # Checks, if the newly received website state has already been sent based on classes values.
    def isMessageIsDownMessageLastSentMessage(self):
        if self.state == "Down" and self.isDownMessageHasBeenSent == True:
            return True
        else:
            return False


    @staticmethod
    def fromJson(jsonString):
        asMap = json.loads(jsonString)
        return WebsiteStateAndMessageSentItem(name=asMap["name"],
                                              state=asMap["state"],
                                              isDownMessageHasBeenSent=asMap["isDownMessageHasBeenSent"])
