from flask import Flask
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
    
    # Run the main coroutine
    asyncio.run(record_audio())

    return "Recording started"

if __name__ == '__main__':
    app.run(debug=True)
