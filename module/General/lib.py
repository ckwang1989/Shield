import os

def check_folder(path):
	if os.path.exists(path):
		pass
	else: 
		os.makedirs(path)