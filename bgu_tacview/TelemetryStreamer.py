#!/usr/bin/env python3

import socket
import time

class TelemetryStreamer(object):
    def __init__(self, bguStream, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.bguStream = bguStream
        self.telemSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.telemSocket.bind((self.host, self.port))
        self.clientConn = None
        self.clientAddr = None
        self.clientUsername = None
        self.quit = False
        self.connected = False


    def connect(self):
        self.telemSocket.listen()
        self.clientConn, self.clientAddr = self.telemSocket.accept()
    
    def sendString(self, stringToSend):
        stringToSend = stringToSend+'\n'
        self.clientConn.sendAll(stringToSend.encode('utf-8'))

    def getString(self):
        return self.clientConn.recv(4096).decode('utf-8')

    def handshake(self):
        # Send handshake
        self.sendString("XtraLib.Stream.0")
        self.sendString("Tacview.RealTimeTelemetry.0")
        self.sendString("Host BGUStream")
        self.sendString("")
        
        # Returning handshake
        if not self.getString() == "XtraLib.Stream.0\n":
            print("ERROR: Bad Stream Type")
            self.closeAll()
            return False
        if not self.getString() == "Tacview.RealTimeTelemetry.0\n":
            print("ERROR: Bad Tacview Type")
            self.closeAll()
            return False
        self.clientUsername = self.getString()[7:-2]
        # skip password check
        self.getString()
        return True

    def sendHeader(self):
        self.sendString("FileType=text/acmi/tacview")
        self.sendString("FileVersion=2.2")

    def sendRefTime(self):
        refString = "0,ReferenceTime={}".format(self.bguStream.getStartTime())
        self.sendString(refString)
    def sendName(self):
        self.sendString("{id},Name={name}".format(id=self.bguStream.getID(), name=self.bguStream.getName()))

    def sendPosition(self):
        offsetSeconds = "#{0:0.2f}".format(self.bguStream.getCurrentSeconds())
        position = "{id},T={lat:07.f}|{lng:0.7f}|{alt:0.2f}|{roll:0.2f}|{pitch:0.2f}|{yaw:0.2f}".format(
            id=self.bguStream.getID(),
            lat=self.bguStream.getLat(),
            lng=self.bguStream.getLng(),
            alt=self.bguStream.getAlt(),
            roll=self.bguStream.getRoll(),
            pitch=self.bguStream.getPitch(),
            yaw=self.bguStream.getYaw()
        )
        self.sendString(offsetSeconds)
        self.sendString(position)

    def closeAll(self):
        self.clientConn.close()
        self.telemSocket.close()
        self.connected = False

    def start(self, loopRate=10):
        self.connect()
        if not self.handshake():
            return
        self.connected = True
        self.sendHeader()
        self.sendRefTime()
        lastTime = time.time()
        rate = 1.0/loopRate
        try:
            while not self.quit:
                if time.time() > lastTime + rate:
                    lastTime = time.time()
                    self.sendPosition()
                sleepTime = rate - (time.time()-lastTime)
                if sleepTime > 0:
                    time.sleep(sleepTime)
            self.closeAll()
        except KeyboardInterrupt:
            self.closeAll()




    

