import time
from flask import Flask, Response
from flask_cors import CORS
import pyaudio
from StethoConnect import StethoConnect
import asyncio

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

audio = pyaudio.PyAudio()

# Set up audio stream
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

@app.route('/record', methods=['POST'])
def record():
    async def record_audio():
        steth = StethoConnect()
        await steth.record_audio()
    
    # Run the main coroutine
    asyncio.run(record_audio())

    return "Recording started"


@app.route('/stream_audio')
def stream_audio():
    def generate_audio():
        while True:
            # Read audio data from the stream
            data = stream.read(1024)
            yield data
            time.sleep(0.1)  # Adjust delay as needed

    return Response(generate_audio(), mimetype='audio/x-wav')


if __name__ == '__main__':
    app.run(debug=True)
