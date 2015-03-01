from globals import Globals

class Building(object):

    def __init__(self, name, sequence, purpose):
        self.name = name            # Name of Building
        self.sequence = sequence    # Sequence number of space
        self.purpose = purpose      # Purpose of building (academic, sports, support, special)
        self.position = [0, 0]      # Row & column on the game board
        self.rect = None            # Rect object where its space is located on the board

        if purpose == 'academic':
            self.color = Globals.lightGray 
        elif purpose == 'special':
            self.color = Globals.blue 
        elif purpose == 'sports':
            self.color = Globals.green 
        elif purpose == 'support':
            self.color = Globals.white 

    def getName(self): 
        return self.name

    def getSequence(self):
        return self.sequence

    def getPurpose(self):
        return self.purpose

    def getPosition(self): 
        return self.position
        
    def setPosition(self, position):
        self.position = position

    def getRect(self): 
        return self.rect
        
    def setRect(self, rect):
        self.rect = rect   

    def getColor(self):
        return self.color
    
    def setColor(self, color):
        self.color = color    
        

class OwnableBuilding(Building):    
    def __init__(self, name, sequence, purpose, price=200000):
        Building.__init__(self, name, sequence, purpose)
        self.owner = None           # Which dean 'owns' building
        self.price = price          # Inital purchase price
        self.renovation = False     # Under Renovation (similar to mortgage)

    def getPrice(self): 
        return self.price

    def getOwner(self):
        return self.owner
    
    def setOwner(self, owner):
        self.owner = owner

    def getRenovation(self): 
        return self.renovation
        
    def setRenovation(self):            # Toggles value of renovation (True/False)
        if self.renovation == False:
            self.renovation = True
        elif self.renovation == True:
            self.renovation = False    
        

class NonAcademicBuilding(OwnableBuilding):

    def __init__(self, name, sequence, purpose, price=200000):
        OwnableBuilding.__init__(self, name, sequence, purpose)
        self.costNonAcademic = 10000     # Cost to other deans for non-academic building fees

    def getFeeAmount(self):
        return self.costNonAcademic

    
class AcademicBuilding(OwnableBuilding):

    def __init__(self, name, sequence, price=200000):
        OwnableBuilding.__init__(self, name, sequence, 'academic')
        self.degreeLvl = 'Associate'
        self.baseGrads = 10             # Base number of grad points earned
        self.costAssociate = 10000      # Cost to other deans for associate lvl classes
        self.costBachelor = 20000       # Cost to other deans for bachelor lvl classes
        self.costMaster = 30000         # Cost to other deans for master lvl classes
        self.costDoctorate = 40000      # Cost to other deans for doctorate lvl classes

    def getDegreeLvl(self):
        return self.degreeLvl
        
    def setDegreeLvl(self, degLvl):
        self.degreeLvl = degLvl

    def getFeeAmount(self):
        if self.degreeLvl == 'Associate':
            return self.costAssociate
        elif self.degreeLvl == 'Bachelor':
            return self.costBachelor
        elif self.degreeLvl == 'Master':
            return self.costMaster
        elif self.degreeLvl == 'Doctorate':
            return self.costDoctorate


