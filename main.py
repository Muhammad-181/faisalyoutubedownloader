from pytube import YouTube



url = YouTube('https://www.youtube.com/watch?v=sbCUP85vIHI')
streams = url.streams

for i in streams:
    print(str(i.resolution))