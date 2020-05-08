# -*- coding: utf-8 -*-
"""
Classe CartMover

La classe CartMover implementa l'interfaccia per muovere
il carrello di Fanny
"""
import time
from pathlib import Path
from gpiozero import DigitalOutputDevice

POSITIONS = ('A', 'B', 'C')
NUM_POSITIONS = len(POSITIONS)

LAST_POS_FILE = '/opt/fanny/movemaker/lastpos'

PIN_EN_MOV = DigitalOutputDevice(17) # GPIO17 - PIN 11 - sesta fila SX
PIN_DIR_MOV = DigitalOutputDevice(18) # GPIO18 - PIN 12 - sesta fila DX

# Passo di controllo ed eventuale modifica del livello dei pin
TIME_STEP = 0.5
#Tempo complessivo di movimento = TIME_STEP * STEPS.
# TODO: da verificare!!
STEPS = 36
# Importante che steps sia divisibile per NUMPOSITIONS-1 
STEPS_SHORT = int(STEPS / (NUM_POSITIONS-1))
#Fattore di modifica del tempo di ritorno in posizione A
REVERSE_CORRECTION = 1

class CartMover:
    
    """
     Costruttore
    """
    def __init__(self):
        # Sono previste due posizioni        
        self.cart_position = 0
        # Tutti i pin inizializzati a off 
        PIN_EN_MOV.off()
        PIN_DIR_MOV.off()
        
    """
     Legge l'ultima posizione in cui si trovava il cart dopo
     l'ultimo spostamento.
     La posizione viene salvata nel file /opt/fanny/movemaker/lastpos
     Se il file non viene trovato, si assume posizione A
    """
    def load_last_position(self):
        self.cart_position = 0
        lastpos_file = Path(LAST_POS_FILE)
        if lastpos_file.is_file():
            s = lastpos_file.read_text()
            for p in POSITIONS:
                if s.startswith(p):
                    self.cart_position = POSITIONS.index(p)
                

    """
     Salva l'ultima posizione in cui si trovava il cart dopo
     l'ultimo spostamento.
     La posizione viene salvata nel file /opt/fanny/movemaker/lastpos     
    """
    def _save_last_position(self):
        lastpos_file = Path(LAST_POS_FILE)
        lastpos_file.write_text(POSITIONS[self.cart_position])
        
    """
     Metodo privato.
     Esegue la sequenza di movimento.
     @param target_pos: indice della posizione da raggiungere
    """
    def _seq_movement(self, target_pos):        
        # All'ingresso della funzione, tutti i pin sono a on        
        if target_pos > 0:
            PIN_EN_MOV.on()
            PIN_DIR_MOV.off()
            nsteps = STEPS_SHORT
        else:
            PIN_EN_MOV.on()
            PIN_DIR_MOV.on()
            nsteps = STEPS            
            
        for i in range(nsteps):
            #Correzione per il ritorno
            if target_pos > 0:
                time.sleep(TIME_STEP)
            else:
                time.sleep(TIME_STEP*REVERSE_CORRECTION)
        
        # Tutti i pin tornano a spento
        PIN_EN_MOV.off()
        PIN_DIR_MOV.off()
    
    """
     Muove il carrello in una delle due posizioni alternativamente
    """
    def move(self):
        new_pos = (self.cart_position+1) % NUM_POSITIONS
        self._seq_movement(new_pos)
        self.cart_position = new_pos            
        #Salva l'ultima posizione di movimento
        self._save_last_position()            
    
    """
     Ritorna la posizione attuale
    """
    def getCartPosition(self):
        return POSITIONS[self.cart_position]
        
    """
     Rilascia le risorse HW
    """
    def releaseHW(self):
        PIN_EN_MOV.close()
        PIN_DIR_MOV.close()

