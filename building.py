
class Building(object):

    def __init__(self, name, abbr, position, price=200000, rent=16000):
        self.name = name
        self.abbr = abbr
        self.position = position
        self.price = price
        self.rent = rent

    def getName(self):
        return self.name

    def getAbbr(self):
        return self.abbr

    def getPosition(self):
        return self.position

    def getPrice(self):
        return self.price

    def getRent(self):
        return self.rent

    
