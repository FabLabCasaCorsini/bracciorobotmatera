# -*- coding: utf-8 -*-
"""
Classe GCodeProcessor

La classe GCodeProcessor implementa l'interfaccia per l'esecuzione
dei movimenti del braccio attraverso i comandi GCODE
"""
import time,serial

SERIAL_PORT = '/dev/ttyACM0'

class GCodeProcessor:
    
    """
     Costruttore.        
    """
    def __init__(self):                
        self.serial_if = None
        
    """
     Apre la connessione seriale verso GRBL
     Se la connessione non può essere stabilita, si avrà un'eccezione
    """
    def connect(self):           
        self.serial_if = serial.Serial(port=SERIAL_PORT, baudrate=115200)

    """
     Processa una lista di linee di comando GCODE.
     Se la scrittura seriale fallisce, si avrà un'eccezione
    """
    def process(self, command_lines):
        #Viene inviata ciascuna linea alla seriale, terminata da NEWLINE
        for linea in command_lines:
            linea += '\n'
            self.serial_if.write(linea)
            self.serial_if.flush()
            time.sleep(0.1)