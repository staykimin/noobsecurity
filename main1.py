import speech_recognition as sr
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence

r = sr.Recognizer()

def get_text(path):
	audio = AudioSegment.from_wav(path)
	sin = split_on_silence(audio, 
		min_silence_len = 500,
		silence_thresh = audio.dBFS-14,
		keep_silence=500,
		)
	folder = "ram_audio"
	if not os.path.isdir(folder):
		os.mkdir(folder)
	
	text = ""
	
	for i, chunk in enumerate(sin, start=1):
		filename = os.path.join(folder, f"ram{i}.wav")
		chunk.export(filename, format="wav")
		
		with sr.AudioFile(filename) as sumber:
			suara = r.record(sumber)
			try:
				tulis = r.recognize_google(suara,  language="en-US")
			except sr.UnknownValueError as e:
				print("Error : ", str(e))
			else:
				tulis = f"{tulis.capitalize()}. "
				print(filename, ":", tulis)
				text += tulis
	return text

path = "sampel3.wav"
print("\nText : ", get_text(path))
