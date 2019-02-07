#!/usr/bin/env python

"""
 Braccio Robotico Matera
 Downloader daemon
"""

import urllib.request
from pathlib import Path
import time, signal, sys
import logging

folderPath = "/home/ale/gcodes/"
baseUrl = 'http://www.appius.it/matera/'
gcodesFolder = 'gcodes/'
fileListUrl = 'gcode_files'

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
log_hdlr = logging.StreamHandler(sys.stdout)
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

        time.sleep(2)
        try:
            logger.info('Lettura lista file da:' + baseUrl + fileListUrl)
            page = urllib.request.urlopen(baseUrl + fileListUrl)
            content = page.read()
            strContent = content.decode('utf-8')
            lines = strContent.splitlines()
            logger.info('Lista file scaricata. Numero files:'+str(len(lines)))

            for row in lines:
                if row == "":
                    continue

                my_file = Path(folderPath + row)
                if my_file.is_file():
                    logger.debug('File presente: '+row)                
                    continue;

                tempUrl = baseUrl + gcodesFolder + row;    
                logger.info('Richiesta download GCODE file: '+tempUrl)                
                pageGcode = urllib.request.urlopen(tempUrl)
                contentGcode = pageGcode.read()
                logger.debug('File scaricato: '+row)
                file = open(folderPath + row,"w")  
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
