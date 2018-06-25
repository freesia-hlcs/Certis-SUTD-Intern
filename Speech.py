import os.path
import sys
import json
import speech_recognition as sr
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )

r = sr.Recognizer()
CLIENT_ACCESS_TOKEN = '2c087495015448aabb887b153f6e81fd'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

def say(words):
    print('Robot Say: '+ words)  #Represent robot 'say' function

class speech():
    def __init__(self):
        self.interrupt_intents = ['GoWashroom'] #List of interruption events. Now it only ocntanins goWashroom.

    def listen(self):
        '''Record when the user is speaking and convert the speech audio file to text using Google voice recognition'''
        with sr.Microphone() as source:
            print('Console: Ready...')
            audio = r.listen(source)
            print('Console: Your speech is recorded.')
        try:
            words = r.recognize_google(audio).lower()
            print('Console: (you said) ' + words + '\n')

        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            say('Sry sir, please say it again.')
            words = self.listen()
        return words


    def respond_to(self,words):
        '''send the speech text to Dialogflow and return corresponding reply'''

        request = ai.text_request()
        request.lang = 'en'#Language code
        request.session_id = "certis-robot-test"
        request.query = words

        json_response = request.getresponse().read().decode('utf-8')
        dict = json.loads(s=json_response) #Convert the json received to dict

        response = dict['result']['fulfillment']['speech']
        say(response)

        intent = dict['result']["metadata"]["intentName"]
        self.event_check(intent)


    def event_check(self,intent):
        if intent == 'GoWashroom':
            self.goto_washroom()


    def order_drink(self):
        '''Ask the guest whether he or she would like some drink'''
        self.respond_to('serve_drink_trigger')


    def common_talk(self):
        words = self.listen()
        self.respond_to(words)
        return self.common_talk()

    def goto_washroom(self):
        #Currently use this function to simulate gotoWashroom event.
        print('Robot move: '+ 'goto washroom')



if __name__ == '__main__':
    test = speech()
    say('Welcome to Certis CSCIO Security! This is the meeting place.')
    test.order_drink()
    test.common_talk()

