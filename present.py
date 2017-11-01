import time
import serial
PortRF = serial.Serial('/dev/ttyAMA0',9600)

import subprocess
import time
import os
import signal

def start(station):
    process = subprocess.Popen("mplayer --quiet %s" % station, shell=True)

def stop():
    os.system('killall mplayer')

maxgone = 5
PortRF.timeout = 0.1
gone = 0 #countdown to token being gone
lastID = None

while True:
    ID = ""
    print("Blocked")
    read_byte = PortRF.read()
    if read_byte=="\x02":
        gone = maxgone #a token is still there, need to check later if it's the same station
        for Counter in range(12):
            read_byte=PortRF.read()
            ID = ID + str(read_byte)
        print ID
        if (ID==lastID):
            print("Same") #gone already reset
        else:
            print("Change")
            stop() #stop any playback
            time.sleep(0.1)
            if ID=='2100AC33209E':
                start('http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/nonuk/low/ak/bbc_radio_fourfm.m3u8') #start radio 4
            if ID=='2100AA021990':
                start('http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/nonuk/low/ak/bbc_radio_two.m3u8') #start radio 2
            if ID=='2100AC3A60D7':
                start('letitsnow.mp3')

        lastID = ID
    #keep subtracting until we get to zero
    if (gone>0):
        gone -= 1 #we've not had the signal for another iteration
        if gone==0:
            print("Stopping")
            lastID = None
            stop()
