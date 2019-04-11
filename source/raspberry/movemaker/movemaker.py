#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Braccio Robotico Matera - Fanny
 MoveMaker daemon

 Il MoveMaker si occupa di:
     - Controllare GRBL sull'arduino di controllo del braccio
     - Controllare il movimento delle ruote via Arduino Taxi

 Attenzione: richiede la libreria pySerial
"""
import sys, signal, time
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

from DrawingJob import DrawingJob
from GCodeProcessor import GCodeProcessor
from CartMover import CartMover

gcode_proc = GCodeProcessor()
cart_mover = CartMover()

DL_FOLDER_PATH = '/opt/fanny/Drawings/downloads/'
FIX_FOLDER_PATH = '/opt/fanny/Drawings/staged/'
ARCHIVE_FOLDER_PATH = '/opt/fanny/Drawings/archived/'

#La coda dei disegni
coda_drawings_dl = []
lista_drawings_fissa = []

keep_on = True

# Gestore dei segnali SIGTERM & SIGINT
def signal_handler(_signo, _stack_frame):
    global keep_on
    # Shutdown the processes
    #print('Caught signal for shutdown: ' + str(_signo))
    keep_on = False

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Logging
logger = logging.getLogger('Fanny.MoveMaker')
#log_hdlr = logging.StreamHandler(sys.stdout)
log_hdlr = TimedRotatingFileHandler('/opt/fanny/movemaker/movemaker.log', 'D', 1, 1)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
log_hdlr.setFormatter(formatter)
logger.addHandler(log_hdlr)
loglevel=eval('logging.DEBUG') #pronto per la gestione a stringa
logger.setLevel(loglevel)


"""
 Carica una lista di disegni da una directory
"""
def carica_lista(lst, loc):
    files_path = Path(loc)
    for f in files_path.iterdir():
        if f.suffix == '.gcode':
            #Crea un oggetto Drawingjob
            dwg = DrawingJob(f)
            lst.append(dwg)

    logger.info('Trovati ' + str(len(lst)) + ' files .gcode in ' + loc )

"""
 Muove il carrello nella posizione puntata dalla variabile 'posizione_carrello'
"""
def muovi_carrello():
    logger.info('Movimento carrello')
    cart_mover.move()
    logger.info('Carrello in posizione '+cart_mover.getCartPosition())

"""
 Legge un file GCODE del disegno ed invia i comandi al processatore
"""
def invia_gcode(dwg):
    linee_gcode = []
    try:
        #Carica le linee dal file
        linee_gcode = dwg.getGCodeFileLines()
    except:
        # Se c'è errore, non è stato possibile legggere il file, per cui viene annullato
        logger.error('Errore nel caricamento del file ' + str(dwg.getGCodePath()) + ':' + str(sys.exc_info()[1]))
        logger.warning('Non è stato possibile caricare il file ' + str(dwg.getGCodePath()))
        return

    if len(linee_gcode):
        logger.info('Invio codici GCODE per il disegno ' + dwg.getGCodeName())
        try:
            gcode_proc.process(linee_gcode)
        except:
            # Se c'è errore, bisogna purtroppo terminare il programma per riavviarlo
            logger.error('Errore nel processamento GCODE:' + str(sys.exc_info()[1]) + '. Uscita.')
            sys.exit(1)

        logger.info('Invio codici GCODE per il disegno ' + dwg.getGCodeName() + ' terminato.')
    else:
        logger.warning('Il file disegno ' + dwg.getGCodeName() + ' non ha contenuto.')

"""
 Processa un disegno, posizionando il carrello e poi muovedo il braccio
"""
def processa_disegno(dwg):
    #1. Muove il carrello nella posizione libera
    muovi_carrello()
    time.sleep(1)
    #2. Esegue il disegno inviando i codici a GRBL
    invia_gcode(dwg)

"""
 Task principale del daemon
"""
def main_task():
    global coda_drawings_dl, lista_drawings_fissa

    #Inizializzazione connessione GCODE
    try:
        gcode_proc.connect()
        logger.info('GCode Processor collegato.')
    except:
        # In caso di errore il programma esce. Il riavvio può provare a ricollegare la seriale
        logger.error('Errore connessione GCode Processor:' + str(sys.exc_info()[1]) + '. Uscita.')
        sys.exit(1)

    #Caricamento della lista dei disegni precaricati dalla directory
    carica_lista(lista_drawings_fissa, FIX_FOLDER_PATH)
    NUM_DWGS_LISTA_FISSA = len(lista_drawings_fissa)
    indice_lista_fissa = 0

    while keep_on:
        #Caricamento della coda dei disegni dalla directory dei downloads
        carica_lista(coda_drawings_dl, DL_FOLDER_PATH)
        if len(coda_drawings_dl):
            while len(coda_drawings_dl):
                #processa il prossimo disegno dei download
                dwg = coda_drawings_dl[0]
                logger.info('Inizio esecuzione disegno ' + dwg.getGCodeName())
                processa_disegno(dwg)
                logger.info('Esecuzione disegno ' + dwg.getGCodeName() + ' terminata')
                #cancella il file dalla directory dei downloads
                dwg.moveGCodeFile(ARCHIVE_FOLDER_PATH)
                #e poi lo rimuove dalla coda
                del coda_drawings_dl[0]
                time.sleep(3)

        elif NUM_DWGS_LISTA_FISSA:
            #A fine downloads, processa il prossimo disegno della lista fissa
            dwg = lista_drawings_fissa[indice_lista_fissa]
            logger.info('Inizio esecuzione disegno precaricato ' + dwg.getGCodeName())
            processa_disegno(dwg)
            logger.info('Esecuzione disegno precaricato ' + dwg.getGCodeName() + ' terminata')
            indice_lista_fissa += 1
            indice_lista_fissa %= NUM_DWGS_LISTA_FISSA

        time.sleep(3)

#Avvio del task principale.
logger.info('Avvio di Fanny.MoveMaker')
#Questa chiamata è bloccante fino alla chiusura del daemon
main_task()
#Rilascio risorse HW
cart_mover.releaseHW()
print('Fanny.MoveMaker esecuzione terminata.')
