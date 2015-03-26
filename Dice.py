import pygame, sys, random





class Dice():
    #parent is the game area
    def __init__(self, parent):
        self.parent = parent
        self.width = self.parent.get_width()//8
        self.height = self.parent.get_width()//16
        self.area = parent.subsurface((self.parent.get_width()//2) - (self.width//2),
                                      (23*self.parent.get_height()//32) - (self.height//2),
                                      self.width, self.height)
        #self._width = int(self._area.get_width())
        self.halfWidth = self.width//2
        #self._height = int(self._area.get_height())
        self.halfHeight = self.height//2

        self.rollCount = 4

        self.numbers = [self.one, self.two, self.three, self.four,
                         self.five, self.six] #Method variables to display each value on dice

    def rect(self):
        return pygame.Rect(self.parent.get_width()//2, self.parent.get_height()//2,
                    self.parent.get_width()/8,self.parent.get_width()//16)
    
    def one(self,side):
        
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side+self.width//4 ,self.halfHeight),
                           int(self.height//10))

    def two(self,side):
        
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side+self.halfWidth*3//10 ,self.height*3//10),
                           int(self.height//10))
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side+self.halfWidth*7//10 ,self.height*7//10),
                           int(self.height//10))

    def three(self,side):
        
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side+self.halfWidth*3//10 ,self.height*7//10),
                           int(self.height//10))
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side +self.halfWidth*7//10 ,self.height*3//10),
                           int(self.height//10))
        self.one(side)


    def four(self, side):
        
        self.two(side)
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side+self.halfWidth*7//10 ,self.height*3//10),
                           int(self.height//10))
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side +self.halfWidth*3//10 ,self.height*7//10),
                           int(self.height//10))

    def five(self,side):
        
        self.two(side)
        self.three(side)

    def six(self, side):
        self.four(side)
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side + self.halfWidth*3//10 ,self.height*5//10),
                           int(self.height//10))
        pygame.draw.circle(self.area,(0,0,0),
                           (self.halfWidth*side + self.halfWidth*7//10 ,self.height*5//10),
                           int(self.height//10))
        

    def displayDice(self, r1, r2):
        self.area.fill((255, 255, 255))
        #draw 2 black borders around each half of the rect
        pygame.draw.rect(self.area, (0,0,0),(0,0, self.area.get_width()//2,
                                              self.area.get_height()), 5)
        pygame.draw.rect(self.area, (0,0,0),(self.area.get_width()//2,0,
                                              self.area.get_width()//2,
                                              self.area.get_height()), 5)
        # print the dots on the dice
        self.numbers[r1-1](0)   
        self.numbers[r2-1](1)


    def roll(self):
        if self.rollCount <= 0:
            self.rollCount = 4
        
        r1, r2 = random.randint(1,6), random.randint(1,6)
        self.displayDice(r1, r2)
     
        self.rollCount -= 1
        return (self.rollCount>0, r1, r2)


def main():
    pygame.init()
    area = pygame.display.set_mode((1000, 1000))
    dice = Dice(area)
    dice.roll()
    pygame.display.flip()
    
    
if __name__ == '__main__':
    main() 
