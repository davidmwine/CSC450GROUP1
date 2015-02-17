class Building(object): 

    def __init__(self, name, sequence, purpose, color=(80, 0, 0), price=200000, rent=16000): 
        
        MAROON   = (80, 0, 0)               # RGB code for Maroon       (University color - background)
        LTGRAY   = (200, 200, 200)          # RGB code for light Gray   (Unowned)
        PURPLE   = (128, 0, 128)            # RGB code for Purple       (Arts & Letters)
        RED      = (255, 0, 0)              # RGB code for Red          (Business)
        LTBLUE   = (173, 216, 230)          # RGB code for Light Blue   (Education)
        ORANGE   = (255, 140, 0)            # RGB code for Orange       (Health & Human Services)
        PEACOCK  = (0, 128, 128)            # RGB code for Peacock Blue (Humanities & Public Affairs)
        GOLDEN   = (255, 215, 0)            # RGB code for Golden Yellow (Natural and Applied Science)
        LTGREEN  = (0, 128, 0)              # RGB code for Green        (Agriculture)
        BLACK    = (0, 0, 0)                # RGB code for Black        
        WHITE    = (255, 255, 255)          # RGB code for White        
        BLUE     = (0, 0, 255)              # RGB code for Blue         
        GREEN    = (0, 255, 0)              # RGB code for Green

        self.name = name                # Name of Building
        self.sequence = sequence        # Sequence number of space
        self.purpose = purpose          # Purpose of building (academic, sports, support, special)
        self.color = color              # Color of building (Initially MAROON)
        self.price = price              # Inital purchase price
        self.baseGrads = 10             # Base number of grad points earned
        self.owner = 'Unowned'          # Which dean 'owns' building (initially unowned)
        self.renovation = False         # Under Renovation (similar to mortgage)
        self.degreeLvl = 'Associate'    # Current degree level building grants
        self.costAssociate = 100        # Cost to other deans for associate lvl classes
        self.costBachelor = 200         # Cost to other deans for bachelor lvl classes
        self.costMaster = 300           # Cost to other deans for master lvl classes
        self.costDoctorate = 400        # Cost to other deans for doctorate lvl classes
        
        if purpose == 'academic':
            self.color = (200, 200, 200)    #LTGRAY
        elif purpose == 'special':
            self.color = (0, 0, 255)        #BLUE
        elif purpose == 'sports':
            self.color = (0, 255, 0)        #GREEN
        elif purpose == 'support':
            self.color = (255, 255, 255)    #WHITE
                
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
        
    def setRenovation(self):            # Toggles value of renovation (TRUE/FALSE)
        if self.renovation == FALSE:
            self.renovation = TRUE
        elif self.renovation == TRUE:
            self.renovation = FALSE

    def getDegreeLvl(self):
        return self.degreeLvl
        
    def setDegreeLvl(self, degLvl):
        self.degreeLvl = degLvl