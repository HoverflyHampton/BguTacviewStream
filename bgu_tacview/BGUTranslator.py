import numpy as np
import time
from bgu_tacview.Craft import Craft

class BGUTranslator(object):
    def __init__(self, bguFile, id=101):
        self.data = np.genfromtxt(bguFile, delimiter=',', 
                    dtype=(str, str, str, int, int, str, 
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, int, int, int, int, int, int,
                    int, int, int, int, str),
                    names=True)
        print(self.data)
        print(self.data.dtypes.names)
        self.id = id
        self.startTime = self.data['Timestamp'][0]+'z'
        self.startSecs = self.getSecs(0)
        self.currentOffset = 0
        self.name = self.data[' BGU FW Version'][0]
        self.craft = Craft()
        self.finishedFile = False

    def getSecs(self, indx):
        secs = float(self.data[' Milli'][indx])* 0.001

    def updateFromLine(self, indx):
        self.currentOffset = self.getSecs(indx) - self.startSecs
        lat = self.data[' Blended Lat'][indx]
        lng = self.data[' Blended Lon'][indx]
        alt = self.data[' Altitude'][indx]
        roll = self.data[' craft Roll'][indx]
        pitch = self.data[' craft Pitch'][indx]
        yaw = self.data[' craft Heading'][indx]
        self.craft.update(lat, lng, alt, roll, pitch, yaw)

    def startCraftLoop(self):
        for indx in range(len(self.data)):
            if indx == len(self.data)-1:
                pass
            self.updateFromLine(indx)
            time.sleep(self.getSecs(indx+1)-self.getSecs(indx))
        
        self.finishedFile = True

    def getLat(self):
        return self.craft.getLat()[0]
    
    def getLng(self):
        return self.craft.getLng()[0]

    def getAlt(self):
        return self.craft.getAlt()[0]

    def getRoll(self):
        return self.craft.getRoll()[0]

    def getPitch(self):
        return self.craft.getPitch()[0]

    def getYaw(self):
        return self.craft.getYaw()[0]

    def getID(self):
        return self.id

    def getStartTime(self):
        return self.startTime

    def getCurrentSeconds(self):
        return self.currentOffset

    def getName(self):
        return self.name


    
