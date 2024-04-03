import subprocess
from flask import Flask, jsonify, send_file,request,request
from flask_cors import CORS
from StethoConnect import StethoConnect
import asyncio
import os,requests
from dotenv import load_dotenv
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={
    r"/signup": {"origins": "*"},
    r"/record": {"origins": "*"},
    r"/predictLungs": {"origins": "*"},
    r"/predictHeart": {"origins": "*"},
    r"/download": {"origins": "*"},
})



# CORS(app)
# Rest of the code...

load_dotenv()
FASTAPI_URL = "http://192.168.93.32:5321"




# Global variable to store loopback module ID
loopback_module_id = None

# Start loopback
def start_loopback():
    global loopback_module_id
    result = subprocess.run(['pactl', 'load-module', 'module-loopback', 'latency_msec=1', 'source=1', 'sink=0'], capture_output=True)
    output = result.stdout.decode().strip()
    if output.isdigit():
        loopback_module_id = int(output)
        return True
    else:
        return False

# Stop loopback
def stop_loopback():
    global loopback_module_id
    if loopback_module_id is not None:
        subprocess.run(['pactl', 'unload-module', str(loopback_module_id)])
        loopback_module_id = None
        return True
    else:
        return False

@app.route('/start_loopback', methods=['GET'])
def start_loopback_route():
    if start_loopback():
        return "Loopback started successfully"
    else:
        return "Failed to start loopback", 500

@app.route('/stop_loopback', methods=['GET'])
def stop_loopback_route():
    if stop_loopback():
        return "Loopback stopped successfully"
    else:
        return "Loopback is not running", 500




@app.route('/signup',methods = ['POST'])
def signup():
    response = requests.post('https://api.chatengine.io/users/',
    data = {
        "username":request.get_json()['name'],
        "secret": request.get_json()['password'],
        "email":request.get_json()['email'],
    },
    headers={"Private-Key":"911d822a-a99a-4dc8-99f2-dd1094b523b9"}
    )
    return response.json()



@app.route('/record', methods=['POST'])
def record():
    async def record_audio():
        steth = StethoConnect()
        output_file = await steth.record_audio(seconds=12)
        if output_file:
            return send_file(output_file, as_attachment=True)
        else:
            return "Error occurred during recording", 500

    asyncio.run(record_audio())
    return "Completed"

# @app.route('/predictLungs', methods=['POST'])
# def predictLungs():
#     with open("recording.wav", "rb") as f:
#         files = {"audio_file": f}
#         response = requests.post(f"{FASTAPI_URL}/classify_lung_audio", headers=HEADERS, files=files)
#         prediction_data = response.json()
#         print(f"Lung prediction response: {prediction_data}")
#     return jsonify(prediction_data)
#
#
#
#
@app.route('/predictLungs', methods=['POST'])
def predictLungs():
    try:
        patient_id = request.get_json()["patient_id"]
        token = request.get_json()["idToken"]
        HEADERS = {"accept": "application/json", "id-token": token}
        with open("recording.wav", "rb") as f:
            files = {"audio_file": f}
            response = requests.post(f"{FASTAPI_URL}/classify_lung_audio?patient_id={patient_id}", headers=HEADERS, files=files)
            prediction_data = response.json()
            print(f"Lung prediction response: {prediction_data}")
        return jsonify(prediction_data)
    except Exception as e:
        print(f"Error predicting lungs: {e}")
        return "Error predicting lungs", 500

@app.route('/predictHeart', methods=['POST'])
def predictHeart():
    data = request.get_json()
    patient_id = data.get("patient_id")
    token = data.get("idToken")
    HEADERS = {"id-token": token}
    with open("recording.wav", "rb") as f:
        files = {"audio_file": f}
        response = requests.post(f"{FASTAPI_URL}/classify_heart_audio?patient_id={patient_id}", headers=HEADERS, files=files)
        prediction_data = response.json()
        print(f"Heart prediction response: {prediction_data}")
    return jsonify(prediction_data)

@app.route('/download', methods=['GET'])
def download():
    return send_file("recording.wav", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
