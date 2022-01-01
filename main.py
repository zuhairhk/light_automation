# import statements
from tuya_connector import TuyaOpenAPI
import os

# env variables
ACCESS_ID = os.environ['ACCESS_ID']
ACCESS_KEY = os.environ['ACCESS_KEY']
API_ENDPOINT = os.environ['API_ENDPOINT']
LIGHTBULB_DEVICE_ID = os.environ['LIGHTBULB_DEVICE_ID']

# CONNECTION
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

#Function that changes colour of bulb
def set_colour(colour):
    commands = {'commands': [
                                { 
                                    'code': 'colour_data_v2', 
                                    'value': {'h': colour, 's': 1000, 'v': 1000}
                                }
                            ]
                }


    openapi.post(f'/v1.0/iot-03/devices/{LIGHTBULB_DEVICE_ID}/commands', commands)

def light_mode(mode):
    commands = {'commands': [
                                {
                                    'code': 'work_mode',
                                    'value': mode
                                }
                            ]
                }

    openapi.post(f'/v1.0/iot-03/devices/{LIGHTBULB_DEVICE_ID}/commands', commands)


while True:
    instruct = input('Enter instructions: [s, l]\n')

    if instruct == 's':
        colour = input('Enter colour [0 -> 360]\n')
        set_colour(colour)
    
    elif instruct == 'l':
        mode = input('Enter light mode [white, colour, scene, music]\n')
        light_mode(mode)

    elif instruct == 'exit':
        break
    
    else:
        print('Inavlid, re-enter instructions: [s,l]\n')