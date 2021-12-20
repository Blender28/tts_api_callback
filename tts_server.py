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

import simpleaudio
import pyttsx3
from flask import Flask, Response, request

# load sounds
wav_err = simpleaudio.WaveObject.from_wave_file("sound/errsound.wav")

# host HTTPS or HTTP
isHTTPS = True

# creat flask applicaiton
app = Flask(__name__)

# empty queue for incoming msgs
msgs2speak = deque([])

# handle incoming post requests @ /error


@app.route("/error", methods=["POST"])
def speach() -> Response:

    # grab message
    msg = request.json

    # if msg blank return no data error
    if not msg or len(msg['msg']) < 1:
        return Response("No Data", status=204, mimetype='application/json')
    else:
        msgs2speak.append(msg['msg'])

    return Response("Success", status=202, mimetype='application/json')


# error warning sound
def grabAttention() -> None:
    play_obj = wav_err.play()
    play_obj.wait_done()


# TTS loop looking for messages in msgs2speak
def tts() -> None:
    global msgs2speak

    # init tts engine
    tts_engine = pyttsx3.init()

    # set voic params
    tts_engine.setProperty("rate", 130)

    while True:

        if len(msgs2speak) != 0:

            # pull the oldest msg out to speak
            speak = msgs2speak.popleft()

            # grab attention of opperator before error msg
            grabAttention()
            sleep(.5)

            # speak err msg
            tts_engine.say(speak)
            tts_engine.runAndWait()
        else:
            sleep(1)


if __name__ == '__main__':

    # start speach thread
    speach_thread = threading.Thread(target=tts)
    speach_thread.setDaemon(True)
    speach_thread.start()

    # TODO
    # Fix ssl certs
    # These are basic self sigend certs for temp purposes
    context = ('certs/server.crt', 'certs/server.key')

    if isHTTPS:
        app.run(debug=False, port=5010, ssl_context=context)
    else:
        app.run(debug=False, port=5010)
