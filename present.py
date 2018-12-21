#!/usr/bin/python

import time
import serial
PortRF = serial.Serial('/dev/ttyAMA0',9600)
import datetime
import subprocess
import time
import os
import signal

def start(station):
    #process = subprocess.Popen("mplayer --quiet %s" % station, shell=True)
    process = subprocess.Popen("cvlc %s --norm-max-level 100 --sout-raop-volume 255 --gain 1" % station, shell=True)

def startmplayer(station):
    process = subprocess.Popen("mplayer --quiet %s" % station, shell=True)

def stop():
    os.system('killall mplayer')
    os.system('killall vlc')

os.system('amixer -c 0 set PCM 4dB')

maxgone = 5
PortRF.timeout = 0.1
gone = 0 #countdown to token being gone
lastID = None

while True:
    ID = ""
#    print("Blocked")
    read_byte = PortRF.read()
    if read_byte=="\x02":
        gone = maxgone #a token is still there, need to check later if it's the same station
        for Counter in range(12):
            read_byte=PortRF.read()
            ID = ID + str(read_byte)
        #print ID
        if (ID==lastID):
            pass
#            print("Same") #gone already reset
        else:
            print("Change")
            print(ID)
            stop() #stop any playback
            time.sleep(0.1)
            if ID=='2100ACB1D2EE': #nuthatch
                start('http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/nonuk/low/ak/bbc_radio_fourfm.m3u8') #start radio 4
            if ID=='2100AA021990':
                pass
            if ID=='2100AC83757B': #dipper
                start('http://media-ice.musicradio.com/ClassicFM?amsparams=playerid:UKRP;skey:1513453514;') #classic fm
            if ID=='2100A9DCAFFB': #blackbird
                start('http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/uk/sbr_high/ak/bbc_radio_three.m3u8') #radio 3
            if ID=='2100AA11EB71': #snowman
                startmplayer('/home/pi/christmas_squirrel/letitsnow.mp3')
            if ID=='2100ABFDB6C1': #robin
                startmplayer('/home/pi/christmas_squirrel/all_i_want.mp3')
                #start('http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/nonuk/low/ak/bbc_radio_two.m3u8') #start radio 2
            if ID=='2100ACCEECAF': #christmas tree
                startmplayer('/home/pi/christmas_squirrel/christmas_tree.mp3')
            if ID=='2100AC33209E': #christmas pudding
                startmplayer('/home/pi/christmas_squirrel/home_alone.mp3')
            if ID=='2100AE9C392A': #violin
                now = datetime.datetime.now()
                filename = "/home/pi/christmas_squirrel/yow/%d-%d.webm" % (now.month,now.day)
                print("Playing %s" % filename)
                start(filename)
            if ID=='2100AC783DC8': #yesterday
                yesterday = datetime.datetime.now()-datetime.timedelta(1)
                filename = "/home/pi/christmas_squirrel/yow/%d-%d.webm" % (yesterday.month,yesterday.day)
                print("Playing %s" % filename)
                start(filename)


        lastID = ID
    #keep subtracting until we get to zero
    if (gone>0):
        gone -= 1 #we've not had the signal for another iteration
        if gone==0:
            print("Stopping")
            lastID = None
            stop()
