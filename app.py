from flask import Flask, jsonify, render_template, request
import requests
import webbrowser
import time
import datetime
import RPi.GPIO as GPIO 
from threading import Thread
import os
from dummy_feeder import Dummy_feeder
import sys
from stage1 import *

app = Flask(__name__)

res = [None] * 20

# OBJECT DEFINITION 

gear_feeder = Gear_Feeder() 
gear_sorter = Gear_Sorter(gear_feeder)
main_rail = Main_Rail()


# DATA TRANSFER ROOT FOR SENSORS & ACTUATORS STATES

@app.route('/data') 
def stuff():

    global gear_feeder 
    my_feeder = Dummy_feeder(3,3)

    if gear_feeder.state == False :
        res[0] = 'Inactive'
        res[4] = 'red'

    elif gear_feeder.state == True:
        res[0] = 'Active'
        res[4] = '#66cc00'

    if gear_feeder.MagSensor.read() == False:
        res[1] = 'Not Detected'

    elif gear_feeder.MagSensor.read() == True:
        res[1] = 'Detected'

    print(res[1])

    if gear_feeder.GateA.state == 'close':
        res[2] = 'Closed'
        res[5] = 'red'

    elif gear_feeder.GateA.state == 'open':
        res[2] = 'Opened'
        res[5] = '#66cc00'

    if gear_feeder.GateB.state == 'close' :
        res[3] = 'Closed'
        res[12] = 'red'

    elif gear_feeder.GateB.state == 'open':
        res[3] = 'Opened'
        res[12] = '#66cc00'

    if gear_sorter.state == True:
        res[6] = 'Active'
        res[13] = '#66cc00'
    
    elif gear_sorter.state == False:
        res[6] = "Inactive"
        res[13] = 'red'
    
    if gear_sorter.gear1MagSensor.read() == True :
        res[7] = 'Detected'
    
    elif gear_sorter.gear1MagSensor.read() == False:
        res[7] = "Not Detected"

    if gear_sorter.gear2MagSensor.read() == True :
        res[8] = 'Detected'
    
    elif gear_sorter.gear2MagSensor.read() == False:
        res[8] = "Not Detected"

    if gear_sorter.GateA.state == 'open' :
        res[9] = 'Open'
        res[14] = '#66cc00'
    
    elif gear_sorter.GateA.state == 'close':
        res[9] = "Close"
        res[14] = 'red'
    
    if gear_sorter.GateB.state == 'open' :
        res[10] = 'Open'
        res[15] = '#66cc00'
    
    elif gear_sorter.GateB.state == 'close':
        res[10] = "Close"
        res[15] = 'red'

    if  my_feeder.random_states[2] == 0:
        res[11] = 13
    
    elif my_feeder.random_states[2] == 1:
        res[11] = 12

    return jsonify(result = res)


#  TRANSFER ROOT FOR THE ACTIONS & COMMANDS OF THE DECVICE

@app.route("/<action>")
def action(action):

    global gear_feeder
    global gear_sorter
    global mail_rail

    if action == "on":
        gear_feeder.start()
    elif action == "off":
        gear_feeder.stop()
    
    if action == 'rotate':    
        gear_feeder.MagInsert()

    if action == 'magInsert':
        gear_sorter.MagInsert()

    if action == 'sorterStart':
        gear_sorter.start()

    elif action == 'sorterStop':
        gear_sorter.stop()                
    
    if action == 'reject':
        gear_sorter.reject()

    if action == 'mainRailIn':
        main_rail.home()

    elif action == 'mainRailMove':
        main_rail.move()

    return render_template('index.html')    

@app.route('/')
def index():

    return render_template('index.html') 

# main driver function
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=2000)
