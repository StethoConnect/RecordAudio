import subprocess
import wave
import pyaudio


class StethoConnect:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    async def record_audio(self, seconds, device_index=1):
        try:
            output_file = "recording.wav"
            command = f"arecord -D plughw:{device_index},0 -d {seconds} -f cd -t wav -r {self.RATE} -c {self.CHANNELS} {output_file}"
            subprocess.run(command, shell=True, check=True)
            print("File recording.wav generated!")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during recording: {e}")
            return None
