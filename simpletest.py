# haus.py
import logging
import time
from time import sleep
import RPi.GPIO as GPIO
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

GPIO.setmode(GPIO.BCM)
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def gruss():
    GPIO.setup(17, GPIO.OUT) # GPIO 0
    GPIO.setup(18, GPIO.OUT) # GPIO 1
    GPIO.setup(27, GPIO.OUT) # GPIO 2
    gruss = render_template('gruss')
    return question(gruss)


@ask.intent("FernseherIntent", mapping={'status': 'status'})
def fernseher(status):
    print('test=>{}'.format(status))
    if status == "an" or status == "erscheine":
        print('AN')
        GPIO.output(17, GPIO.HIGH)  # GPIO 0
        sleep(0.5)
        GPIO.output(18, GPIO.HIGH)  # GPIO 1
        sleep(0.5)
        GPIO.output(27, GPIO.HIGH)  # GPIO 2
    if status == "aus":
        print('AUS')
        GPIO.output(17, GPIO.LOW)  # GPIO 0
        GPIO.output(18, GPIO.LOW)  # GPIO 1
        GPIO.output(27, GPIO.LOW)  # GPIO 2
    status = render_template('fernseher', status=status)
    return question(status)


@ask.intent("LichtIntent", mapping={'status': 'status'})
def licht(status):
    if status == "an":
        GPIO.output(18, GPIO.HIGH)  # GPIO 1
    if status == "aus":
        GPIO.output(18, GPIO.LOW)  # GPIO 1
    status = render_template('licht', status=status)
    return question(status)


@ask.intent("SteckdoseIntent")
def steckdose(status):
    if status == "an":
        GPIO.output(27, GPIO.HIGH)  # GPIO 2
    if status == "aus":
        GPIO.output(27, GPIO.LOW)  # GPIO 2
    status = render_template('dose', status=status)
    return question(status)


if __name__ == '__main__':
    app.run(debug=True)