import urllib.request
from pathlib import Path
import time

folderPath = "/home/ale/gcodes/"
baseUrl = 'http://www.appius.it/matera/'
gcodesFolder = 'gcodes/'
fileListUrl = 'gcode_files'

index = 0;

while index < 1 :

	time.sleep(2)
	try:
		page = urllib.request.urlopen(baseUrl + fileListUrl)
		content = page.read()
		strContent = content.decode('utf-8')
		lines = strContent.splitlines()

		for row in lines:
			if row == "":
				continue
			
			tempUrl = baseUrl + gcodesFolder + row;
			
			pageGcode = urllib.request.urlopen(tempUrl)
			contentGcode = pageGcode.read()

			my_file = Path(folderPath + row)
			if my_file.is_file():
				continue;

			print ('row = ' + row);
			print (tempUrl);
			file = open(folderPath + row,"w")  
			file.write(contentGcode.decode('utf-8')) 
			file.close() 

	except:
		print ("Exception")
	
print ("fine");




