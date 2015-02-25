from globals import Globals

class Building(object): 

    def __init__(self, name, sequence, purpose, price=200000): 

        self.name = name                # Name of Building
        self.sequence = sequence        # Sequence number of space
        self.purpose = purpose          # Purpose of building (academic, sports, support, special)
        self.price = price              # Inital purchase price
        self.position = [0, 0]          # Row & column on the game board
        self.baseGrads = 10             # Base number of grad points earned
        self.owner = 'Unowned'          # Which dean 'owns' building (initially unowned)
        self.renovation = False         # Under Renovation (similar to mortgage)
        self.degreeLvl = 'Associate'    # Current degree level building grants
        self.costNonAcademic = 100      # Cost to other deans for non-academic building fees
        self.costAssociate = 100        # Cost to other deans for associate lvl classes
        self.costBachelor = 200         # Cost to other deans for bachelor lvl classes
        self.costMaster = 300           # Cost to other deans for master lvl classes
        self.costDoctorate = 400        # Cost to other deans for doctorate lvl classes
        
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

    def getPosition(self): 
        return self.position
        
    def setPosition(self, position):
        self.position = position

    def getSequence(self):
        return self.sequence    
        
    def getPurpose(self):
        return self.purpose
        
    def getColor(self):
        return self.color
    
    def setColor(self, color):
        self.color = color

    def getPrice(self): 
        return self.price 

    def getBaseGrads(self):
        return self.baseGrads
    
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

    def getDegreeLvl(self):
        return self.degreeLvl
        
    def setDegreeLvl(self, degLvl):
        self.degreeLvl = degLvl

    def getFeeAmount(self):
        if self.purpose != 'academic':
            return self.costNonAcademic
        elif self.degreeLvl == 'Associate':
            return self.costAssociate
        elif self.degreeLvl == 'Bachelor':
            return self.costBachelor
        elif self.degreeLvl == 'Master':
            return self.costMaster
        elif self.degreeLvl == 'Doctorate':
            return self.costDoctorate
