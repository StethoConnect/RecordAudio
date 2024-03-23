from flask import Flask, jsonify, send_file,request
from flask_cors import CORS
from StethoConnect import StethoConnect
import asyncio
import os,requests
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
load_dotenv()
FASTAPI_URL = "https://3c0f-152-58-219-66.ngrok-free.app"
HEADERS = {"ngrok-skip-browser-warning": "69420"}

@app.route('/record', methods=['POST'])
def record():
    async def record_audio():
        steth = StethoConnect()
        await steth.record_audio(seconds=12)
        # return send_file("recording.wav", as_attachment=True)

    asyncio.run(record_audio())
    return "Completed"

@app.route('/predictLungs', methods=['POST'])
def predictLungs():
    with open("recording.wav", "rb") as f:
        files = {"audio_file": f}
        response = requests.post(f"{FASTAPI_URL}/classify_lung_audio", headers=HEADERS, files=files)
        prediction_data = response.json()
        print(f"Lung prediction response: {prediction_data}")
    return jsonify(prediction_data)

@app.route('/predictHeart', methods=['POST'])
def predictHeart():
    with open("recording.wav", "rb") as f:
        files = {"audio_file": f}
        response = requests.post(f"{FASTAPI_URL}/classify_heart_audio", headers=HEADERS, files=files)
        prediction_data = response.json()
        print(f"Heart prediction response: {prediction_data}")
    return jsonify(prediction_data)

@app.route('/download', methods=['GET'])
def download():
    return send_file("recording.wav", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
