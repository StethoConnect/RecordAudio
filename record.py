import subprocess
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)








@app.route('/record', methods=['POST'])
def record():
    try:
        device_index = int(request.args.get('device_index', 1))  # Default device index is 1
        seconds = int(request.args.get('seconds', 10))  # Default recording duration is 10 seconds
    except ValueError:
        device_index = 1
        seconds = 10

    try:
        output_file = "recording.wav"
        command = f"arecord -D plughw:{device_index},0 -d {seconds} -f cd -t wav -r 44100 -c 1 {output_file}"
        subprocess.run(command, shell=True, check=True)
        return send_file(output_file, as_attachment=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during recording: {e}")
        return "Error occurred during recording", 500






@app.route('/download', methods=['GET'])
def download():
    try:
        return send_file("recording.wav", as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
