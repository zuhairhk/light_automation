# import statements
from tuya_connector import TuyaOpenAPI
import os
import speech_recognition as sr
#import pyttsx3

# env variables
ACCESS_ID = os.environ['ACCESS_ID']
ACCESS_KEY = os.environ['ACCESS_KEY']
API_ENDPOINT = os.environ['API_ENDPOINT']
LIGHTBULB_DEVICE_ID = os.environ['LIGHTBULB_DEVICE_ID']

# CONNECTION
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Audio Recognition Setup
recognizer = sr.Recognizer()

# Function that controls state of bulb
def light_state(mode):
    commands = {'commands': [
                                {
                                    'code': 'switch_led',
                                    'value': mode
                                }
                            ]
                }
    
    openapi.post(f'/v1.0/iot-03/devices/{LIGHTBULB_DEVICE_ID}/commands', commands)

# Function that changes colour of bulb
def set_colour(colour):
    commands = {'commands': [
                                { 
                                    'code': 'colour_data_v2', 
                                    'value': {'h': colour, 's': 1000, 'v': 1000}
                                }
                            ]
                }


    openapi.post(f'/v1.0/iot-03/devices/{LIGHTBULB_DEVICE_ID}/commands', commands)

# Function that sets mode of lightbulb [white, colour, scene, music]
def light_mode(mode):
    commands = {'commands': [
                                {
                                    'code': 'work_mode',
                                    'value': mode
                                }
                            ]
                }

    openapi.post(f'/v1.0/iot-03/devices/{LIGHTBULB_DEVICE_ID}/commands', commands)

def voice_to_colour(text):
    colours = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'pink']
    iValue = [0, 30, 45, 120, 180, 245, 300]

    for i in range(len(colours)):
        if text is None:
            take_command()
        elif colours[i] in text:
            return iValue[i]

def manual_commands():
    # Manual commands
    instruct = input('Enter instructions: \n'
                    'on -> turn on light\n'
                    'off -> turn off light\n'
                    's -> set colour manual\n'
                    'l -> set light mode manual\n')
                    
    if instruct == 's':
        colour = input('Enter colour [0 -> 360]\n')
        set_colour(colour)
    elif instruct == 'l':
        mode = input('Enter light mode [white, colour, scene, music]\n')
        light_mode(mode)
    elif instruct == 'on':
        light_state(True)
    elif instruct == 'off':
        light_state(False)
    elif instruct == 'exit':
        return False
    else:
        print('Inavlid, re-enter instructions: [s,l]\n')

def take_command():
    try:
        with sr.Microphone() as mic:
            print('Calibrating for ambient noise, wait fham...')
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            print('Done!')
            
            audio = recognizer.listen(mic)
            
            command = recognizer.recognize_google(audio)
            command = command.lower()

            print(f'Command announced: {command}')
            return command
    except:
        print('Exception')

def initiate_command(wordList):
    colours = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'pink']
    
    if 'on' in wordList:
        light_state(True)
    if 'off' in wordList:
        light_state(False)
    for i in range(len(colours)):
        if colours[i] in wordList:
            intColour = voice_to_colour(wordList)
            set_colour(intColour)
    if 'white' in wordList:
        light_mode('white')
    if 'manual'in wordList:
        manual_commands()


while True:
    statement = take_command()

    while statement is None:
        print(statement)
        statement = take_command()
    else:
        print(statement)
        if 'lights' or 'light' in statement:
            wordList = statement.split()
    
    initiate_command(wordList)
