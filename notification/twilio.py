import os
from twilio.rest import Client as twilioclient

class Notification:

    def __init__(self, account_sid, auth_token, my_number, twilio_number=""):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.my_number = my_number
        if twilio_number != "":
            self.twilio_number = twilio_number
        else:
            self.twilio_number = my_number

    # Call me anytime even in night

    def notify_me(self, message):

        client = twilioclient(self.account_sid, self.auth_token)
        call = client.calls.create(
                            twiml='<Response><Say>{}</Say></Response>'.format(message),
                            to = self.my_number,
                            from_ = self.twilio_number
                        )
        print(call.sid)