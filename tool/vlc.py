import os
import telnetlib
import time
from tool import mongo
import eyed3

#host = "127.0.0.1"
#password = "test"
#port = 4212
nt = None
title = "None"
songfile = "None"
volume = 0
active = False

#def connect( host, port, password):
def connect(host, port, password):
    global nt

    nt = telnetlib.Telnet( host, port )
    #nt.write(password+"\n")
    telnet_write(password)
    read_line()
    read_line()
    read_line()

def telnet_write( command ):
    global nt
    nt.write(bytes(command+"\n", 'utf-8'))
    time.sleep(0.1)

def read_line():
    global nt
    value = nt.read_until(bytes("\n", 'utf-8'))
    return value.decode('utf-8')

def queue( name ):
    path = os.path.abspath( name )
    telnet_write("enqueue " + path)


def add( path, mysong , cover ):
    #path = os.path.abspath( "public/songs/"+name )
    #telnet_write("enqueue " + path)
    print( "PATH: "+path )
    print("MYSONG: "+mysong)
    print("COVER: "+cover)
    print("EYED3:" + os.path.abspath(  path+"/"+mysong ) )
    song = eyed3.load( os.path.abspath(  path+"/"+mysong ) )

    #data = { "file":mysong ,"artist":song.tag.artist } #"cover":cover, "album":song.tag.album, "title":song.tag.title }
#    mongo.insert(data)


def play():
    telnet_write("play")

def stop():
    telnet_write("stop")


def pause():
    telnet_write("pause")

def next():
    telnet_write("next")

def prev():
    telnet_write("prev")

def getVolume():
    telnet_write("volume")
    return read_line().replace(">","").replace("\r\n","").replace(" ","")

def setVolume( value ):
    telnet_write( "volume " + value )

def exec(query):
    print("====> VLCQUERY " + query)

    l = query.split()

    command = l[0]
    if len(l) > 1 :
        arg = l[1]
        print(command)
        print(arg)
    if command == "play":
        print("=========> PLAY")
        play()
    if command == "pause":
        pause()
    if command == "stop":
        stop()
    if command == "next":
        next()
    if command == "prev":
        prev()
    if command == "getInfo":
        getInfo()
    if command == "queue":
        queue(arg)
    if command == "volume":
        print("SET VOLUME")
        setVolume( arg )


def __getTitle():
    telnet_write("get_title")
    title = read_line().replace(">","").replace("\n","").replace("\r","")
    return title

def __getNameSong():
    telnet_write("status")
    name = read_line()
    print("INFO2  "+ name)
    name = name.replace(">","").replace(")","").replace(" ","").replace("\n","").replace("\r","")
    read_line()
    read_line()

    print("INFO2  "+ name)
    name = name.replace("(newinput:file:///home/alumnos/Projects/amenizador/store/songs/","").replace(".mp3","")
    print("INFO2  "+ name)

    return name


def getInfo():
    global title, songfile
    global volume
    global active
    if isPlaying():
        title = __getTitle()
        songfile = __getNameSong()
        volume = getVolume()
        active = isPlaying()
    else:
        title = "dafult"
        songfile = "default"
        volume = 20
        active = False


def isPlaying():
    telnet_write("is_playing")
    s = int( read_line().replace("> ","") )
    print(s)
    if s == 1:
        return True
    return False


def getTitle():
    return title

def getFile():
    return img

def getStatus():
    global title
    global songfile
    global volume
    global active
    return {"title": title, "filesong": songfile, "img":"store/imgs/"+songfile+".jpg" , "volume":int(volume), "active":active }
