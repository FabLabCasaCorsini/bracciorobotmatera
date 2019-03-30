#!/usr/bin/env python

"""
 Braccio Robotico Matera - Fanny
 Downloader daemon
"""

import urllib.request
from pathlib import Path
import time, signal
import logging
from logging.handlers import TimedRotatingFileHandler

FOLDER_PATH = '/opt/fanny/Drawings/downloads/'
BASE_URL = 'http://www.appius.it/matera/'
GCODE_FOLDER = 'gcodes/'
FILE_LIST_URL = 'gcode_files'

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
logger = logging.getLogger('Fanny.Downloader')
#log_hdlr = logging.StreamHandler(sys.stdout)
log_hdlr = TimedRotatingFileHandler('/opt/fanny/Downloader/downloader.log', 'D', 1, 1)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
log_hdlr.setFormatter(formatter)
logger.addHandler(log_hdlr)
loglevel=eval('logging.DEBUG') #pronto per la gestione a stringa
logger.setLevel(loglevel)

#
# Task principale del daemon
#
def main_task():

    while keep_on:

        time.sleep(5)
        try:
            logger.info('Lettura lista file da:' + BASE_URL + FILE_LIST_URL)
            page = urllib.request.urlopen(BASE_URL + FILE_LIST_URL)
            content = page.read()
            strContent = content.decode('utf-8')
            lines = strContent.splitlines()
            logger.info('Lista file scaricata. Numero files:'+str(len(lines)))

            for row in lines:
                if row == "":
                    continue

                my_file = Path(FOLDER_PATH + row)
                if my_file.is_file():
                    logger.debug('File presente: '+row)                
                    continue;

                tempUrl = BASE_URL + GCODE_FOLDER + row;    
                logger.info('Richiesta download GCODE file: '+tempUrl)                
                pageGcode = urllib.request.urlopen(tempUrl)
                contentGcode = pageGcode.read()
                logger.debug('File scaricato: '+row)
                file = open(FOLDER_PATH + row,"w")  
                file.write(contentGcode.decode('utf-8')) 
                logger.debug('Scrittura completata: '+row)
                file.close() 

        except:
            import traceback
            logger.error('Eccezione in Downloader: ' + traceback.format_exc())
    
#Avvio del task principale.
#Questa chiamata è bloccante fino alla chiusura del daemon
logger.info('Avvio di Fanny.Downloader')
main_task()
            
print('Fanny.Downloader terminato.')
