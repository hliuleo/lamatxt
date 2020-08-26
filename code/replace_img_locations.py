import os, sys
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
src_dir = sys.argv[1] if len(sys.argv) >= 2 else '../html'
dirpath = os.getcwd()
log_files = dirpath+"/result.txt"
log_imgs = dirpath+"/imgs.txt"
log_replacements = dirpath+"/img_path_replacements.txt"
imgs_dir = "images"
files_dir = "files"
os.makedirs(files_dir, exist_ok=True)
fw_log = open(log_files, "w")
fw_img_log = open(log_imgs, "w")
fw_replacements_log = open(log_replacements, "w")
zhibei_fowang = 'https://www.zhibeifw.com'
count = 0
replacement_count = 0
print(src_dir)
for root, dirs, files in os.walk(src_dir):
	if len(dirs)==0:
		fw_log.write(root+" contains "+str(len(files))+" files.\n")
		count += len(files)
		# if count>100:
		# 	break
		for file in files:
			filepath = os.path.join(root, file)
			fr = open(filepath, 'r')
			s = fr.read()
			if '/export/sites/default/.galleries' in s:
				replacement_count += 1
				print(str(replacement_count))
				fw_replacements_log.write(filepath+'\n')
				s = s.replace('/export/sites/default/.galleries','/images')
				# fw = open(files_dir+'/'+filepath.split("/")[-1], 'w')
				fw = open(filepath, 'w')
				fw.write(s)
				fw.close()
			fr.close()
	else:
		fw_log.write(root+" contains " +str(len(dirs))+" directories and " +str(len(files))+" files.\n")
print("Total number of files: "+str(count))
print("Finished!")
