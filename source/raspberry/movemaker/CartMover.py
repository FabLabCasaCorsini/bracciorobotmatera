# -*- coding: utf-8 -*-
"""
Classe CartMover

La classe CartMover implementa l'interfaccia per muovere
il carrello di Fanny
"""
import time
from gpiozero import DigitalOutputDevice

POSITION_A = 'A'
POSITION_B = 'B'

PIN_A_SX = DigitalOutputDevice(17) # GPIO17 - PIN 11 - sesta fila SX
PIN_B_SX = DigitalOutputDevice(18) # GPIO18 - PIN 12 - sesta fila DX
PIN_A_DX = DigitalOutputDevice(22) # GPIO22 - PIN 15 - ottava fila SX
PIN_B_DX = DigitalOutputDevice(23) # GPIO23 - PIN 16 - ottava fila DX

# Passo di controllo ed eventuale modifica del livello dei pin
TIME_STEP = 0.5
# TODO: da verificare!!
STEPS = 10 #Tempo complessivo di movimento = TIME_STEP * STEPS.

class CartMover:
    
    """
     Costruttore
    """
    def __init__(self):
        # Sono previste due posizioni
        self.cart_position = POSITION_A
        # Tutti i pin inizializzati a spento
        PIN_A_SX.off()
        PIN_B_SX.off()
        PIN_A_DX.off()
        PIN_B_DX.off()
        
    """
     Metodo privato.
     Esegue la sequenza di movimento.
     @param dir_forward: True per la direzione in avanti, False indietro
    """
    def _seq_movement(self, dir_forward):        
        # All'ingresso della funzione, tutti i pin sono a zero!        
        if dir_forward:
            PIN_A_SX.on()
            PIN_A_DX.on()
        else:
            PIN_B_SX.on()
            PIN_B_DX.on()            
            
        for i in range(STEPS):
            #
            # QUI IL CODICE PER LA STERZATA
            #
            time.sleep(TIME_STEP)
        
        # Tutti i pin tornano a spento
        PIN_A_SX.off()
        PIN_B_SX.off()
        PIN_A_DX.off()
        PIN_B_DX.off() 
    
    """
     Muove il carrello in una delle due posizioni alternativamente
    """
    def move(self):
        if self.cart_position == POSITION_A:
            #Movimento verso la posizione B (Avanti)
            self._seq_movement(True)
            self.cart_position = POSITION_B
        else:
            #Movimento verso la posizione A (Indietro)
            self._seq_movement(False)
            self.cart_position = POSITION_A            
    
    """
     Ritorna la posizione attuale
    """
    def getCartPosition(self):
        return self.cart_position
        
    """
     Rilascia le risorse HW
    """
    def releaseHW(self):
        PIN_A_SX.close()
        PIN_B_SX.close()
        PIN_A_DX.close()
        PIN_B_DX.close()         

