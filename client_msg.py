"""
████████╗████████╗███████╗               █████╗ ██████╗ ██╗
╚══██╔══╝╚══██╔══╝██╔════╝              ██╔══██╗██╔══██╗██║
   ██║      ██║   ███████╗    █████╗    ███████║██████╔╝██║
   ██║      ██║   ╚════██║    ╚════╝    ██╔══██║██╔═══╝ ██║
   ██║      ██║   ███████║              ██║  ██║██║     ██║
   ╚═╝      ╚═╝   ╚══════╝              ╚═╝  ╚═╝╚═╝     ╚═╝
   
Description:
    This is the client side to the tts_server.py file. 
    Run this script in a seperate terminal to test the functionality of the API before building further.
"""

import requests

url = 'http://127.0.0.1:5000/error'
msg = {}

if __name__ == '__main__':

    while True:

        msg2send = input('what would you like to send? ')
        msg['msg'] = msg2send
        reply = requests.post(url, json=msg)
