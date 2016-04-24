import requests

url = "http://127.0.0.1:5000/upload"
files = {'file': open('../../../../Desktop/08 Homecoming.mp3', 'rb'), 'filename': 'Homecoming'}
r = requests.post(url, files=files)
