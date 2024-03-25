from flask import Flask, jsonify, send_file,request,request
from flask_cors import CORS
from StethoConnect import StethoConnect
import asyncio
import os,requests
from dotenv import load_dotenv
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Rest of the code...


load_dotenv()
FASTAPI_URL = "https://3c0f-152-58-219-66.ngrok-free.app"
HEADERS = {"ngrok-skip-browser-warning": "69420"}



@app.route('/signup',methods = ['POST'])
def signup():
    response = requests.post('https://api.chatengine.io/users/',
    data = {
        "username":request.get_json()['name'],
        "secret": request.get_json()['password'],
        "email":request.get_json()['email'],
        "first_name":request.get_json()['first_name'],
        "last_name":request.get_json()['last_name'],
    },
    headers={"Private-Key":"911d822a-a99a-4dc8-99f2-dd1094b523b9"}
    )
    return response.json()




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
