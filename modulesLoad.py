from connector import logging
import os

# Loading modules #
def load():
	jss=[]
	for path, subdirs, files in os.walk('./modules'):
		for name in files:
			if(not ".pyc" in name):
				if(not "init" in name):
					file = os.path.join(path, name).replace(".py","").replace("./","")
					logging.info(f"[LOAD MODULE]: @{file}")
