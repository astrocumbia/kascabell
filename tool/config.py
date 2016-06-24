#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

data = None

def load(filename):
    global data
    f = open(filename,"r")
    stream = f.read()
    data = json.loads(stream)
    f.close()

def getTelnet():
    global data
    return data['telnet']

def getDomotic():
    global data
    return data['domotic']

def getSerial():
    global data
    return data['serial']

def getPath():
    global data
    return data['path']

def getVlc():
    global data
    return data['vlc']
