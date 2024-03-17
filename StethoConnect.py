import pyaudio
import wave


class StethoConnect:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    async def record_audio(self, seconds):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate = self.RATE,
                        input = True,
                        frames_per_buffer=self.CHUNK)
        print("Recording ......")

        frames = []


        while len(frames) < int(self.RATE / self.CHUNK * seconds):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("recording stopped!!")

        stream.stop_stream()
        stream.close()
        p.terminate()
        try:
            with wave.open("recording.wav", "wb") as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
            print("File recording.wav generated!")
        except Exception as e:
            print(f"File generation failed: {e}")

