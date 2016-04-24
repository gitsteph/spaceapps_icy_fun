import speech_recognition as sr

import os
from os import path
import subprocess


def convert_to_wav(name, audio_name):


	
    f_name = name.split('.')[0]

    # c = 'avconv -i ./uploads/{}.3gp -c:a libmp3lame ./uploads/{}.wav'.format(f_name,f_name)
    #c2 = 'mv ./uploads/{}.mp3 ./uploads/{}.mp3'.format(f_name, audio_name.split('.')[0])
    # os.system(c)
    #os.system(c2)
    source = './uploads/{}.mp3'.format(f_name)
    destination = './uploads/{}.wav'.format(audio_name.split('.')[0])
    os.rename(source, destination)


def speech_converter(file_name):
	# transcribe WAV, RFF or FLAC format
	AUDIO_FILE = os.path.join(path.dirname(path.realpath(__file__)), file_name)

	r = sr.Recognizer()
	with sr.AudioFile(AUDIO_FILE) as source:
		audio = r.record(source) # read the entire audio file

	# obtain audio from the microphone
	# with sr.Microphone() as source:
	# 	print "Say something!" 
	# 	audio = r.listen(source)

	# recognize speech using Google Speech Recognition
	try:
	# for testing purposes, we're just using the default API key
	# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
	# instead of `r.recognize_google(audio)`
		print "Google Speech Recognition thinks you said " + r.recognize_google(audio)
	except sr.UnknownValueError:
		print "Google Speech Recognition could not understand audio"
	except sr.RequestError as e:
		print "Could not request results from Google Speech Recognition service; {0}".format(e)
