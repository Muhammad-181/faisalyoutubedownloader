from django.shortcuts import render
from django.http import HttpResponse
from pytube import YouTube
import os
from wsgiref.util import FileWrapper



def ytd(request):
    return render(request, 'ytd.html')

def download_page(request):
    global url
    url = request.GET.get('url')

    yt = YouTube(url)
    global streams
    streams = yt.streams

    res = []
    ores = []
    for i in streams:
        onlyres = i.resolution

        string = str(i.resolution) + ' ' + str(i.filesize_approx // 1048576) + 'mb'

        res.append(string)
        ores.append(onlyres)
    ores = list(dict.fromkeys(ores))


    try:
        for j in range(len(ores)):
            if ores[j] == None:
                ores.pop(j)
    except:
        pass

    for k in range(len(ores)):
        ores[k] = ores[k] + ' ' + str(streams.filter(res=ores[k]).first().filesize // 1048576) + 'mb'

    title = yt.title
    author = yt.author
    length = str(yt.length//60) + ' minutes'
    if length == 0:
        length = str(yt.length) + 'seconds'
    

    thumbnail = yt.thumbnail_url
    print(thumbnail)

    context = {
        'onlyres': ores,
		'res': res,
		'title': title,
		'author': author,
		'length': length,
		'thumbnail': thumbnail,
    }
    res = list(dict.fromkeys(res))
    return render(request, 'download.html', context)



def success(request, res):
    global url

    homedir = os.path.expanduser("~")

    dirs = homedir + '/Downloads'

    yt = YouTube(url)
    title = yt.title
    print(title)
    res,b = res.split()
    size = streams.filter(res=res).first().filesize // 1048576
    print(size)
    if request.method =='POST' and size < 900:
        streams.filter(res=res).first().download(output_path = dirs, filename = "video.mp4")
        file = FileWrapper(open(f'{dirs}/video.mp4', 'rb'))
        response = HttpResponse(file, content_type = 'application/vnd.mp4')
        response['Content-Disposition'] = 'attachment; filename = "video.mp4"'
        os.remove(f'{dirs}/video.mp4')
        return response

    else:
        return render(request, 'error.html')


def about(request):
    return render(request, 'about.html')



def music(request):
    return render(request, 'music.html')



def download_music(request):
    url = request.GET.get('url')
    yt = YouTube(url)
    title = yt.title

    stream = yt.streams.filter(only_audio=True).first()


    homedir = os.path.expanduser('~')

    dirs = homedir + '/downloads'
    size = stream.filesize // 104576


    if request.method =='POST' and size < 900:
        streams.download(outputpath=dirs, filename=f'{title}.mp3')
        file = FileWrapper(open(f'{dirs}/{title}.mp3', 'rb'))
        response = HttpResponse(file, content_type = 'audio.mp3')
        response['Content-Disposition'] = f'attachment; file = "{title}.mp3"'
        os.remove(f'{dirs}/{title}.mp3')
        return response
    else:
        return render(request, 'error.html')