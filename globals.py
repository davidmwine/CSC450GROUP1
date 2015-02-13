from building import Building

class Globals(object):
    
    maroon = (80, 0, 0)
    lightGray = (200, 200, 200)

    collegeColors = {'Arts and Letters': (128, 0, 128),  # Purple
                   'Business': (255, 0, 0),           # Red
                   'Education': (173, 216, 230),           # Light Blue
                   'Health and Human Services': (255, 140, 0),  # Orange
                   'Humanities and Public Affairs': (0, 128, 128),  # Peacock Blue
                   'Natural and Applied Sciences': (255, 215, 0),   # Golden Yellow
                   'Agriculture': (0, 128, 0)}         # Green

    collegeAbbr = {'Arts and Letters': 'Arts & Letters',
                   'Business': 'Business',
                   'Education': 'Education',
                   'Health and Human Services': 'Health & Hum Serv',
                   'Humanities and Public Affairs': 'Hum & Pub Affairs',
                   'Natural and Applied Sciences': 'Nat & App Sci',
                   'Agriculture': 'Agriculture'}

    
    buildings = []
    buildings.append( Building('Carrington', 'CARR', 0) )
    buildings.append( Building('Siceluff', 'SICL', 1) )
    buildings.append( Building('Cheek', 'CHEEK', 2) )
    buildings.append( Building('Bookstore', 'BOOK', 3) )
    buildings.append( Building('Plaster Student Union', 'PSU', 4) )
    buildings.append( Building('McDonald Arena', 'MCDA', 5) )
    buildings.append( Building('Meyer Library', 'LIBR', 6) )
    buildings.append( Building('Foster Recreation Center', 'FRC', 7) )
    buildings.append( Building('Hammons Field', 'HAMM', 8) )
    buildings.append( Building('Brick City', 'BRICK', 9) )
    buildings.append( Building('Bear Park North', 'BPN', 10) )
    buildings.append( Building('Juanita K Hammons', 'JKH', 11) )
    buildings.append( Building('JQH Arena', 'JQH', 12) )
    buildings.append( Building('Hammons Student Center', 'HSC', 13) )
    buildings.append( Building('Allison South', 'ALL', 14) )
    buildings.append( Building('Glass', 'GLASS', 15) )
    buildings.append( Building('Strong', 'STRO', 16) )
    buildings.append( Building('Bear Park South', 'BPS', 17) )
    buildings.append( Building('Kemper', 'KEMP', 18) )
    buildings.append( Building('Temple', 'TEMP', 19) )
    buildings.append( Building('Plaster Stadium', 'PLAS', 20) )
    buildings.append( Building('Karls', 'KARL', 21) )
    buildings.append( Building('Pummil', 'PUMM', 22) )
    buildings.append( Building('Craig', 'CRAIG', 23) )
    buildings.append( Building('Ellis', 'ELLIS', 24) )
    buildings.append( Building('Hill', 'HILL', 25) )

    


    
