import pygame, sys, random





class Dice():
    #parent is the game area
    def __init__(self, parent):
        self._parent = parent
        
        
        self._parent = parent
        self._area = parent.subsurface((self._parent.get_width()//2, self._parent.get_height()//2,
                    self._parent.get_width()/8,self._parent.get_width()//16))
        self._width = int(self._area.get_width())
        self._half_width = self._width//2
        self._height = int(self._area.get_height())
        self._half_height = self._height//2

        self._roll_count = 4

        self._numbers = [self.one, self.two, self.three, self.four,
                         self.five, self.six]

    def rect(self):
        return pygame.Rect(self._parent.get_width()//2, self._parent.get_height()//2,
                    self._parent.get_width()/8,self._parent.get_width()//16)
    
    def one(self,side):
        
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side+self._width//4 ,self._half_height),
                           int(self._height//10))

    def two(self,side):
        
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side+self._half_width*3//10 ,self._height*3//10),
                           int(self._height//10))
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side+self._half_width*7//10 ,self._height*7//10),
                           int(self._height//10))

    def three(self,side):
        
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side+self._half_width*3//10 ,self._height*7//10),
                           int(self._height//10))
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side +self._half_width*7//10 ,self._height*3//10),
                           int(self._height//10))
        self.one(side)


    def four(self, side):
        
        self.two(side)
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side+self._half_width*7//10 ,self._height*3//10),
                           int(self._height//10))
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side +self._half_width*3//10 ,self._height*7//10),
                           int(self._height//10))

    def five(self,side):
        
        self.two(side)
        self.three(side)

    def six(self, side):
        self.four(side)
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side + self._half_width*3//10 ,self._height*5//10),
                           int(self._height//10))
        pygame.draw.circle(self._area,(0,0,0),
                           (self._half_width*side + self._half_width*7//10 ,self._height*5//10),
                           int(self._height//10))
        


    def roll(self):
        if self._roll_count <= 0:
            self._roll_count = 4
        self._area.fill((255, 255, 255))
        #draw 2 black boarders around each have of the rect
        pygame.draw.rect(self._area, (0,0,0),(0,0, self._area.get_width()//2,
                                              self._area.get_height()), 5)
        pygame.draw.rect(self._area, (0,0,0),(self._area.get_width()//2,0,
                                              self._area.get_width()//2,
                                              self._area.get_height()), 5)
        #get roll value as list indicies
        r1, r2 = random.randint(0,5), random.randint(0,5)
        print(r1+1, r2+1, self._roll_count)
        self._numbers[r1](0)
        self._numbers[r2](1)
        self._roll_count -= 1
        return (self._roll_count>0,r2+r1, self._area)


def main():
    pygame.init()
    area = pygame.display.set_mode((1000, 1000))
    dice = Dice(area)
    dice.roll()
    pygame.display.flip()
    
    
if __name__ == '__main__':
    main() 
