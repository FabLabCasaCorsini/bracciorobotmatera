#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Braccio Robotico Matera - Fanny
 MoveMaker daemon
 
 Il MoveMaker si occupa di:
     - Controllare GRBL sull'arduino di controllo del braccio
     - Controllare il movimento delle ruote via Arduino Taxi
"""
import signal, time
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

import DrawingJob

DL_FOLDER_PATH = '/opt/fanny/Downloader/dwgs/'
FIX_FOLDER_PATH = '/opt/fanny/MoveMaker/dwgs/'

#La coda dei disegni
coda_drawings_dl = []
lista_drawings_fissa = []
#sono previste due posizioni
posizione_carrello = 0

keep_on = True

# Gestore dei segnali SIGTERM & SIGINT
def signal_handler(_signo, _stack_frame):
    global keep_on
    # Shutdown the processes
    #print "Caught signal for shutdown: " + str(_signo)
    keep_on = False

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Logging
logger = logging.getLogger('Fanny.MoveMaker')
#log_hdlr = logging.StreamHandler(sys.stdout)
log_hdlr = TimedRotatingFileHandler('/opt/fanny/MoveMaker/movemaker.log', 'D', 1, 1)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
log_hdlr.setFormatter(formatter)
logger.addHandler(log_hdlr)
loglevel=eval('logging.DEBUG') #pronto per la gestione a stringa
logger.setLevel(loglevel)


"""
 Carica la lista dei disegni precaricati
"""
def carica_lista_fissa():
    global lista_drawings_fissa
    fix_path = Path(FIX_FOLDER_PATH)
    for f in fix_path.iterdir():        
        if f.suffix == '.gcode':
            #Crea un oggetto Drawingjob
            dwg = DrawingJob(f)
            lista_drawings_fissa.append(dwg)
            
    logger.info('Trovati '+ len(lista_drawings_fissa) + ' disegni precaricati' )

"""
 Carica la coda dei disegni scaricati
"""
def carica_coda_downloads():
    global coda_drawings_dl
    dl_path = Path(DL_FOLDER_PATH)
    for f in dl_path.iterdir():
        if f.suffix == '.gcode':
            #Crea un oggetto Drawingjob
            dwg = DrawingJob(f)
            coda_drawings_dl.append(dwg)
    
    logger.info('Trovati '+ len(coda_drawings_dl) + ' disegni scaricati' )

"""
 Muove il carrello nella posizione puntata dalla variabile 'posizione_carrello'
"""
def muovi_carrello():
    global posizione_carrello
    #1. Muove il carrello nella posizione libera
    if posizione_carrello == 1:
        posizione_carrello = 0
    else:
        posizione_carrello = 1
    ###
    ### Codice dello spostamento del carrello
    ###
    logger.info('Movimento carrello in posizione ' + str(posizione_carrello))

"""
 Legge un file GCODE del disegno ed invia i comandi a GRBL
 attraverso la seriale (USB)
"""
def invia_gcode_grbl(dwg):
    ###
    ### Codice dell'invio del GCODE a GRBL
    ###
    logger.info('Invio codici GCODE per il disegno ' + dwg.getGCodeName())

"""
 Processa un disegno, posizionando il carrello e poi
 muovedo il braccio
"""
def processa_disegno(dwg):
    muovi_carrello()
    #2. Esegue il disegno inviando i codici a GRBL
    invia_gcode_grbl(dwg)        

"""
 Task principale del daemon
"""
def main_task():
    global coda_drawings_dl, lista_drawings_fissa
    #Caricamento della lista dei disegni precaricati dalla directory 
    carica_lista_fissa()
    indice_lista_fissa = 0
    
    while keep_on:
        #Caricamento della coda dei disegni dalla directory dei downloads
        carica_coda_downloads()        
        while len(coda_drawings_dl):
            #processa il prossimo disegno dei download
            dwg = coda_drawings_dl[0]
            logger.info('Inizio esecuzione disegno ' + dwg.getGCodeName())
            processa_disegno(dwg)
            logger.info('Esecuzione disegno ' + dwg.getGCodeName() + ' terminata')
            #cancella il file dalla directory dei downloads
            dwg.deleteGCodeFile()
            #e poi lo rimuove dalla coda            
            coda_drawings_dl.remove(0)
            time.sleep(3)
        
        #A fine downloads, processa il prossimo disegno della lista fissa
        dwg = lista_drawings_fissa[indice_lista_fissa]
        logger.info('Inizio esecuzione disegno precaricato ' + dwg.getGCodeName())
        processa_disegno(dwg)
        logger.info('Esecuzione disegno precaricato ' + dwg.getGCodeName() + ' terminata')
        indice_lista_fissa += 1
        indice_lista_fissa %= len(lista_drawings_fissa)        
        time.sleep(3)

#Avvio del task principale.
#Questa chiamata è bloccante fino alla chiusura del daemon
logger.info('Avvio di Fanny.MoveMaker')
main_task()
            
print('Fanny.MoveMaker terminato.')