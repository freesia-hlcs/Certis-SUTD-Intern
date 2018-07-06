import os.path
import sys
import json
import speech_recognition as sr
#import win32com.client

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )


r = sr.Recognizer()
CLIENT_ACCESS_TOKEN = '2c087495015448aabb887b153f6e81fd'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
#speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(words):
    print('Robot Say: ' + words)  # Represent robot 'say' function
    #speaker.Speak(words)


class Speech():
    def __init__(self):
        self.interrupt_intents = ['GoWashroom']  # List of interruption events. Now it only contains goWashroom.
        self.guest_bot = 'name'
        self.name_bot = ''
        self.response = ''
        self.action = ''
        self.action_bot = ''
        self.check = ''

    def listen(self):
        '''Record when the user is speaking and convert the speech audio file to text using Google voice recognition'''
        with sr.Microphone() as source:
            print('Console: Ready...')
            audio = r.listen(source)
            print('Console: Your speech is recorded.')
        try:
            words = r.recognize_google(audio).lower()
            print('Console: (you said) ' + words + '\n')

        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            say('Sry sir, please say it again.')
            words = self.listen()
        return words

    def respond_to(self, words):
        '''send the speech text to Dialogflow and return corresponding reply'''

        request = ai.text_request()
        request.lang = 'en'  # Language code
        request.session_id = "certis-robot-test"
        request.query = words

        json_response = request.getresponse().read().decode('utf-8')
        dict = json.loads(s=json_response)  # Convert the json received to dict

        response = dict['result']['fulfillment']['speech']
        self.response = response
        say(response)

        try:
            self.guest_bot = dict['result']['parameters']['name']

        # double_check_name - yes

        except TypeError and KeyError:
            pass

        if self.guest_bot != 'name':
            self.name_bot = self.guest_bot

        if dict['result']["metadata"] != {}:
            self.action_bot = dict['result']['action']

            if self.action_bot == 'double_check_name.double_check_name-yes':
                self.action = 'true'
            elif self.action_bot == 'double_check_name.double_check_name-no':
                self.action = 'false'
            else:
                self.action = ''

        if dict['result']["metadata"] != {}:  # Being empty means that now the talk intent belongs to common talk
            intent = dict['result']["metadata"]["intentName"]
            self.event_check(intent)

    def event_check(self, intent):
        if intent == 'GoWashroom':
            self.goto_washroom()

    def order_drink(self):
        '''Ask the guest whether he or she would like some drink'''
        self.respond_to('serve_drink_trigger')

    def check_name(self):
        # double check the guest's identity by asking for their name
        self.respond_to('name_check_trigger')

    def common_talk_name(self):

            words = self.listen()
            self.respond_to(words)
            if self.name_bot == '':
                return self.common_talk_name()
            else:
                return self.name_bot

    def print_name(self):
        return self.name_bot

    def double_check_name(self):
        self.respond_to('double_check_trigger')



    def common_talk_double_check(self):

            words = self.listen()
            self.respond_to(words)
            if self.action == 'true':
                self.check = 'true'
                return self.check
            elif self.action == 'false':
                self.check = 'false'
                return self.check
            else:
                return self.common_talk_double_check()

    def print_check(self):
        return self.check

    def common_talk(self):
        words = self.listen()
        self.respond_to(words)
        return self.common_talk()

    def goto_washroom(self):
        # Currently use this function to simulate gotoWashroom event.
        print('Robot move: ' + 'goto washroom')


if __name__ == '__main__':
    test = speech()
    say('Welcome to Certis CISCO Security! This is the meeting place.')
    #test.order_drink()
    test.double_check_name()
    test.common_talk_double_check()
