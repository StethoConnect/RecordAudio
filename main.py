from flask import Flask, jsonify
from flask_cors import CORS
from StethoConnect import StethoConnect
import asyncio

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/record', methods=['POST'])
def record():
    async def record_audio():
        steth = StethoConnect()
        await steth.record_audio()
        # return send_file("recording.wav",as_attachment=True)
    
    # Run the main coroutine
    asyncio.run(record_audio())

    # return send_file("recording.wav",as_attachment=True)
    return "Completed"

@app.route('/predictLungs', methods=['POST'])
def predictLungs():
    async def predict_lungs():
        print("fast api call ")
        # Perform lungs prediction
        prediction_data = {"result": "Lungs prediction result"}
        return jsonify(prediction_data)

    return asyncio.run(predict_lungs())

@app.route('/predictHeart', methods=['POST'])
def predictHeart():
    async def predict_heart():
        print("fast api call ")
        # Perform heart prediction
        prediction_data = {"result": "Heart prediction result"}
        return jsonify(prediction_data)

    return asyncio.run(predict_heart())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
