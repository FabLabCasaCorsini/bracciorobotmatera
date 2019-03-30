# -*- coding: utf-8 -*-
"""
Classe DrawingJob

La classe DrawingJob rappresenta un attività di disegno da realizzare
attraverso il controllo del braccio
"""
from pathlib import Path

class DrawingJob:
    
    """
     Costruttore.
     Parametro gcodepath: oggetto Path del file associato
    """
    def __init__(self, gcodepath):        
        self.gcodepath = gcodepath #oggetto Path                
        
    """
     Ritorna un oggetto Path che contiene il path
     completo del file gcode di questo disegno
    """
    def getGCodePath(self):
        return self.gcodepath
    
    def getGCodeName(self):
        return self.gcodepath.name
    
    """
     Ritorna la lista delle linee contenute nel file GCODE
     Le linee sono ripuilite da eventuali caratteri speciali o spazi
     
     Questo metodo può fallire, è necessario considerare la gestione dell'eccezione
     dal chiamante
    """
    def getGCodeFileLines(self):
        with self.gcodepath.open() as f:
            content = f.readlines()
            # Pulizia delle linee
            content = [x.strip() for x in content]
        return content

    """
     Sposta il file associato a questo drawing in una directory
    """    
    def moveGCodeFile(self, path_dest):
        dp = Path(path_dest).joinpath(self.gcodepath.name)
        self.gcodepath.rename(dp)
        
            
    """
     Cancella il file associato a questo drawing.
     Attenzione: dopo la cancellazione, il file non è recuperabile!
    """    
    def deleteGCodeFile(self):
        self.gcodepath.unlink()

    
# Fine definizione classe DrawingJob

