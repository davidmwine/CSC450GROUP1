# From http://www.pygame.org/wiki/TextWrapping?parent=CookBook
# Converts a string of text into a list containing the lines it would break
# down into for a certain font and width.
# pygame.init() 
# font=pygame.font.Font(None, 17)
# print wrapline("Now is the time for all good men to come to the aid of their country", font, 120)
# outputs: ['Now is the time for all', 'good men to come to', 'the aid of their', 'country'] 


from itertools import chain
 
def truncLine(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapLine(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
 
def wrapMultiLine(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)
