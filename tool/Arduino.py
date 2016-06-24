#!/usr/bin/python3
# -*- coding: utf-8 -*-
import serial
import json

ser = None

def init(device):
    global ser
    ser = serial.Serial(port=device, baudrate=9600)

def getState():
    global ser
    response = ser.readline()
    return json.loads( response.decode("utf-8") )
