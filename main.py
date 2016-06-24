#!/usr/bin/python3
# -*- coding: utf-8 -*-

from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from bottle import route, post, get, run, template, static_file, request, response, redirect
import json
import time
import os
import eyed3
import hashlib
import subprocess

from tool import config
from tool import Arduino
from tool import vlc


#******************************#
#         Global elements      #
#******************************#
q = Queue() # For querys to arduino and vlc states
pool = ThreadPoolExecutor(10)
arduino_state = {} # for query to arduino module


#*************************************#
#                 ROUTES              #
#*************************************#
@get('/domotic')
def domotic():
	response.status = 200
	response.content_type = 'text/plain'
	response.body = 'true'
	return response

@get('/index')
def index():
	return template('views/index')

@get('/')
def index():
	global arduino_state
	response.status = 200
	response.content_type = 'json'
	response.body = json.dumps(arduino_state) #'domotic'#json.dumps( config )
	return response

@post('/upload')
def index():
    cover = request.files.get('cover')
    song = request.files.get('song')
    cname, cext = os.path.splitext(cover.filename)
    sname, sext = os.path.splitext(song.filename)

    hashname   = hashlib.sha224(sname.encode('utf-8')).hexdigest()
    songname  = hashname + sext
    covername = hashname + cext

    cover.save( os.path.abspath("store/imgs")+ "/" + covername )
    song.save( os.path.abspath("store/songs")+ "/" + songname )

    #vlc.add( "store/songs", songname.decode('utf-8'), covername.decode('utf-8') )
    #vlc.queue("store/songs/"+songname)
    q.put("queue "+"store/songs/"+songname)
    redirect('/index')
	#audio = eyed3.load("03-Decks-Dark.mp3")
    #return hashlib.sha224(song.filename.encode('utf-8')).hexdigest()

@get('/upload')
def index():
    return template('views/upload')

#  Regresar todos los archivos necesarios (img,css,js)
@route('<path:path>')
def server_static(path):
	return static_file(path,root='./')

@get('/music')
def index():
	return template('views/index')

@post('/music/volume')
def index():
    volume = request.forms.get('volume')
    q.put("volume "+volume)

@get('/music/play')
def play():
	print("======>>>>  WEB PLAYY")
	q.put("play")

@get('/music/next')
def next():
	q.put("next")

@get('/music/pause')
def pause():
	q.put("pause")

@get('/music/stop')
def stop():
	q.put('stop')

@get('/music/title')
def index():
	global arduino_state
	response.status = 200
	response.content_type = 'json'
	response.body = json.dumps({"title":vlc.getTitle()}) #'domotic'#json.dumps( config )
	return response

@get('/music/status')
def index():
	global arduino_state
	response.status = 200
	response.content_type = 'json'
	response.body = json.dumps(vlc.getStatus()) #'domotic'#json.dumps( config )
	return response



# ************************************#
# read info about localhost           #
# ************************************#

def readArduino():
    global arduino_state
    while True:
        arduino_state = Arduino.getState()
        print(arduino_state)

def runVLC():
	while True:
		command = q.get()
		vlc.exec( command )
		print("vlc [command]==> "+command)

def VlcGetStatus():
	while True:
		q.put("getInfo")
		time.sleep(5)
		print( vlc.getStatus() )

def addSongs():
	songs = os.listdir("store/songs")
	for item in songs:
		q.put("queue "+"store/songs/"+item)

def init():
	config.load('config.json')
	subprocess.Popen('tool/start.sh', shell=True, executable='/bin/bash')
	time.sleep(2)
	confVLC = config.getVlc()
	vlc.connect(confVLC['host'], confVLC['port'], confVLC['password'])
	Arduino.init( config.getSerial() )
	addSongs()


#*************************************#
#                  MAIN               #
#*************************************#
if __name__=="__main__":
	init()
	pool.submit(readArduino)
	pool.submit( run, server='paste' ,host='127.0.0.1', port=8000 )
	pool.submit( runVLC )
	pool.submit( VlcGetStatus )
