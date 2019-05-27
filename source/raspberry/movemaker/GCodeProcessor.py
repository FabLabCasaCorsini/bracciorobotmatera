# -*- coding: utf-8 -*-
"""
Classe GCodeProcessor

La classe GCodeProcessor implementa l'interfaccia per l'esecuzione
dei movimenti del braccio attraverso i comandi GCODE
"""
import sys, time
from pathlib import Path
import serial

SERIAL_PORT_PATTERN = '/dev/ttyACM?'
GRBL_SOFT_RESET = chr(24)
GRBL_UNLOCK = '$X\n'
GRBL_RESET_COORD_ZERO = 'G10 P0 L20 X0 Y0 Z0\n'
GRBL_GO_HOME = '$H\n'
#Numero di secondi da attendere per ogni unità di distanza
DELAY_FOR_UNIT = 0.3 #TODO: tuning
DRAWINGS_FOR_HOME = 2
DELAY_FOR_HOMING = 20

class GCodeProcessor:

    """
     Costruttore.
    """
    def __init__(self, log):
        self.serial_if = None
        self.ser_conn = False
        self.log = log
        self.last_point = (0,0)
        self.home_counter = 0

    """
     Individua il link di sistema alla prima porta seriale
     che abbia nome che inizia con SERIAL_PORT_ROOT.
     Se il link non viene trovato, ritorna None
    """
    def _find_serial(self):
        p = Path('/dev')
        for child in p.iterdir():
            if child.match(SERIAL_PORT_PATTERN):
                return str(child)            

    """
     Apre la connessione seriale verso GRBL.
     Assume che:
         Arduino crei una seriale del tipo /dev/ACMx, quindi originale
         Si sia solo un'Arduino connesso alla Raspberry
         
     Se la connessione non può essere stabilita, si avrà un'eccezione
    """
    def connect(self):
        self.ser_conn = False
        while not self.ser_conn:
            try:
                serial_port = self._find_serial()
                self.serial_if = serial.Serial(port=serial_port, baudrate=115200)
                self.ser_conn = True
                self.log.debug('collegato alla seriale.')
            except:
                self.log.error('Errore connessione GCode Processor:' + str(sys.exc_info()[1]) + '. Attesa...')

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
     Estrae un float da una stringa a partire da un certo
     indice fino al primo carattere non ammissibile
    """
    def _extract_float(self, s):
        rs=''
        for c in s:
            if c.isdigit() or c == '.':
                rs += c
            else:
                break
        return float(rs)

    """
     Estrae il punto di arrivo da una linea GCODE di tipo spostamento
     assoluto: G0Z<z>X<x>Y<y>F10
     Ritorna una tupla (x,y)
    """
    def _next_gcode_point(self, gline):
        #Trova la X
        ss = gline[gline.find('X')+1:]
        x = self._extract_float(ss)
        #Trova la Y
        ss = gline[gline.find('Y')+1:]
        y = self._extract_float(ss)        
        return (x,y)
        
    """
     Introduce un ritardo proporzionale alla distanza da percorrere
     tra l'ultimo punto ed il successivo
    """
    def _delay_to_next_point(self, next_point):
        d = max(abs(self.last_point[0]-next_point[0]), abs(self.last_point[1]-next_point[1]))
        delay = d * DELAY_FOR_UNIT
        self.log.debug('pausa di ' + str(delay))
        time.sleep(d*DELAY_FOR_UNIT)

    """
     Processa una lista di linee di comando GCODE.
     Se la scrittura seriale fallisce, si avrà un'eccezione
    """
    def process(self, command_lines):
        self.connect()
        if self.ser_conn:
            self.unblock()
            self.log.debug('Home Counter:'+str(self.home_counter))
            self.log.debug('Esecuzione HOMING')
            self.serial_if.write(GRBL_GO_HOME.encode('ascii'))        
            #self._delay_to_next_point((0,0))
            time.sleep(DELAY_FOR_HOMING)
            self.serial_if.write(GRBL_RESET_COORD_ZERO.encode('ascii'))
            self.last_point = (0,0)
            #Viene inviata ciascuna linea alla seriale, terminata da NEWLINE
            for linea in command_lines:
                self.log.debug('LINEA GCODE:'+linea)
                linea += '\n'
                self.serial_if.write(linea.encode('ascii'))
                self.serial_if.flush() 
                if linea.startswith('G0'):
                    #Introduce un ritardo propozionale alla distanza
                    next_point = self._next_gcode_point(linea)
                    self._delay_to_next_point(next_point)
                    self.last_point = next_point
                else:
                    time.sleep(0.4)

            #Assicura lo spegnimento del led a fine disegno
            self.serial_if.write('M5\n'.encode('ascii'))
            self.serial_if.flush()
            time.sleep(0.4)

            #self.home_counter = (self.home_counter + 1) % DRAWINGS_FOR_HOME
            time.sleep(10)
            self.serial_if.close()
            self.serial_if = None
            self.ser_conn = False
