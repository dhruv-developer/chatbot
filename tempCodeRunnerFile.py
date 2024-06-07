import pyaudio
import wave

# Record audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
frames = []

try:
    print("Recording...")
    for _ in range(0, int(44100 / 1024 * 2)):
        data = stream.read(1024)
        frames.append(data)
finally:
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

# Save recording
wf = wave.open('output.wav', 'wb')
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b''.join(frames))
wf.close()

# Play recording
wf = wave.open('output.wav', 'rb')
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
data = wf.readframes(1024)
while data:
    stream.write(data)
    data = wf.readframes(1024)

stream.stop_stream()
stream.close()
p.terminate()
