class Craft(object):
    def __init__(self, lat=0, lng=0, alt=0, roll=0, pitch=0, yaw=0):
        self.data = {}
        self.data['lat'] = [lat, True]
        self.data['lng'] = [lng, True]
        self.data['alt'] = [alt, True]
        self.data['roll'] = [roll, True]
        self.data['pitch'] = [pitch, True]
        self.data['yaw'] = [yaw, True]

    def update(self, lat=0, lng=0, alt=0, roll=0, pitch=0, yaw=0):
        if lat != self.lat:
            self.data['lat'][1] = True
            self.data['lat'][0] = lat
        if lng != self.lng:
            self.data['lng'][1] = True
            self.data['lng'][0] = lng
        if alt != self.alt:
            self.data['alt'][1] = True
            self.data['alt'][0] = alt
        if roll != self.roll:
            self.data['roll'][1] = True
            self.data['roll'][0] = roll
        if pitch != self.pitch:
            self.data['pitch'][1] = True
            self.data['pitch'][0] = pitch
        if yaw != self.yaw:
            self.data['yaw'][1] = True
            self.data['yaw'][0] = yaw

    def getLat(self):
        val = self.data['lat'][:]
        self.data['lat'][1] = False
        return val

    def getLng(self):
        val = self.data['lng'][:]
        self.data['lng'][1] = False
        return val

    def getAlt(self):
        val = self.data['alt'][:]
        self.data['alt'][1] = False
        return val

    def getRoll(self):
        val = self.data['roll'][:]
        self.data['roll'][1] = False
        return val

    def getPitch(self):
        val = self.data['pitch'][:]
        self.data['pitch'][1] = False
        return val

    def getYaw(self):
        val = self.data['yaw'][:]
        self.data['yaw'][1] = False
        return val
