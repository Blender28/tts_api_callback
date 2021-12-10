"""
████████╗████████╗███████╗               █████╗ ██████╗ ██╗
╚══██╔══╝╚══██╔══╝██╔════╝              ██╔══██╗██╔══██╗██║
   ██║      ██║   ███████╗    █████╗    ███████║██████╔╝██║
   ██║      ██║   ╚════██║    ╚════╝    ██╔══██║██╔═══╝ ██║
   ██║      ██║   ███████║              ██║  ██║██║     ██║
   ╚═╝      ╚═╝   ╚══════╝              ╚═╝  ╚═╝╚═╝     ╚═╝

Description:
    This very basic POST call is to demonstrate the capabilities of the pyttsx3 library,
    while also building something handy for future projects
   
"""

import threading
from collections import deque
from time import sleep

import pyttsx3
from flask import Flask, Response, request

# creat flask applicaiton
app = Flask(__name__)

# empty queue for incoming msgs
msgs2speak = deque([])

# handle incoming post requests @ /error


@app.route("/error", methods=["POST"])
def speach() -> Response:

    # TODO
    # error handling for absence of json packet

    # grab message
    msg = request.json

    # if msg blank return no data error
    if len(msg['msg']) < 1:
        return Response("No Data", status=204, mimetype='application/json')
    else:
        msgs2speak.append(msg['msg'])

    return Response("Success", status=202, mimetype='application/json')

# TTS loop looking for messages in msgs2speak


def tts() -> None:
    global msgs2speak

    # init tts engine
    tts_engine = pyttsx3.init()

    while True:

        if len(msgs2speak) != 0:
            speak = msgs2speak.popleft()
            tts_engine.say(speak)
            tts_engine.runAndWait()
        else:
            sleep(1)


if __name__ == '__main__':

    speach_thread = threading.Thread(target=tts)
    speach_thread.setDaemon(True)
    speach_thread.start()

    app.run(debug=False)
