import urllib.request
from pytube import YouTube

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
try:
    yt = YouTube(url)
    print(yt.title)
except Exception as e:
    print(repr(e))
