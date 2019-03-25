# -*- coding: utf-8 -*-
"""
Classe DrawingJob

La classe DrawingJob rappresenta un attività di disegno da realizzare
attraverso il controllo del braccio
"""

class DrawingJob:
    
    #Initializer
    def __init__(self, gcodepath):                
        self.gcodepath = gcodepath
        
    """
     Ritorna un oggetto Path che contiene il path
     completo del file gcode di questo disegno
    """
    def getGCodePath(self):
        return self.gcodepath
    
    def getGCodeName(self):
        return self.gcodepath.name
    
    def deleteGCodeFile(self):
        self.gcodepath.unlink()

    
# Fine definizione classe DrawingJob

