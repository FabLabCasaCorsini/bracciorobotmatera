# -*- coding: utf-8 -*-
"""
Classe GCodeProcessor

La classe GCodeProcessor implementa l'interfaccia per l'esecuzione
dei movimenti del braccio attraverso i comandi GCODE
"""
import time,serial

SERIAL_PORT = '/dev/ttyACM0'
GRBL_SOFT_RESET = chr(24)
GRBL_UNLOCK = '$X\n'
GRBL_RESET_COORD_ZERO = 'G10 P0 L20 X0 Y0 Z0\n'
GRBL_GO_HOME = '$H\n'

class GCodeProcessor:

    """
     Costruttore.
    """
    def __init__(self, log):
        self.serial_if = None
        self.log = log

    """
     Apre la connessione seriale verso GRBL
     Se la connessione non può essere stabilita, si avrà un'eccezione
    """
    def connect(self):
        self.serial_if = serial.Serial(port=SERIAL_PORT, baudrate=115200)

    """
     Resetta e sblocca il GRBL
    """
    def unblock(self):
        #Soft reset
        self.serial_if.write(GRBL_SOFT_RESET.encode('ascii'))
        time.sleep(1)
        #Unlock
        self.serial_if.write(GRBL_UNLOCK.encode('ascii'))
        time.sleep(1)

    """
     Processa una lista di linee di comando GCODE.
     Se la scrittura seriale fallisce, si avrà un'eccezione
    """
    def process(self, command_lines):
        self.unblock()
        self.serial_if.write(GRBL_GO_HOME.encode('ascii'))
        self.serial_if.write(GRBL_RESET_COORD_ZERO.encode('ascii'))
        #Viene inviata ciascuna linea alla seriale, terminata da NEWLINE
        for linea in command_lines:
            self.log.debug('LINEA GCODE:'+linea)
            linea += '\n'
            self.serial_if.write(linea.encode('ascii'))
            self.serial_if.flush()
            #time.sleep(2)
