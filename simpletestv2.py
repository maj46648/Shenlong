#   Author: Johannes Maier
#   date: 2020-06-21

import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ["anzuschalten", "anzumachen", "anmachen", "anschalten",
            "an"]  # alle Werte, die als Synonyme im Slot Type definiert wurden
STATUSOFF = ["auszuschalten", "auszumachen", "ausmachen", "ausschalten", "aus"]


@ask.launch
def launch():
    speech_text = 'Wilkommen zur Raspberry Pi Automatisierung.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('LightIntent', mapping={'status': 'status'})
def Gpio_Intent(status, room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    if status in STATUSON:
        GPIO.output(17, GPIO.HIGH)
        return statement('Licht wurde angeschaltet')
    elif status in STATUSOFF:
        GPIO.output(17, GPIO.LOW)
        return statement('Licht wurde ausgeschaltet')
    else:
        return statement('Sorry, der Befehl ist leider nicht möglich.')

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
