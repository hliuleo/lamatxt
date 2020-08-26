import os, sys
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
src_dir = sys.argv[1] if len(sys.argv) >= 2 else '../html'
dirpath = os.getcwd()
log_files = dirpath+"/result.txt"
log_imgs = dirpath+"/imgs.txt"
imgs_dir = "images"
fw = open(log_files, "w")
fw_img_log = open(log_imgs, "w")
zhibei_fowang = 'https://www.zhibeifw.com'
count = 0
images_done = []
print(src_dir)
for root, dirs, files in os.walk(src_dir):
	if len(dirs)==0:
		fw.write(root+" contains "+str(len(files))+" files.\n")
		count += len(files)
		# if count>100:
		# 	break
		for file in files:
			filepath = os.path.join(root, file)
			f = open(filepath, 'r')
			soup = BeautifulSoup(f.read(), 'html.parser')
			images = soup.findAll('img')
			for image in images:
				#print image source
				# print image['src']
				src = image['src']
				if src in images_done:
					continue
				images_done.append(src)
				fw_img_log.write(src+"\n")
				filepath = src
				filepath = filepath.replace('/export/sites/default/.galleries','')
				fw_img_log.write(filepath+"\n")
				splits = filepath.split("/")
				filename = splits[-1]
				filepath = filepath.replace(filename,'')
				file_dir = imgs_dir+filepath
				os.makedirs(file_dir, exist_ok=True)
				target_file = file_dir+"/"+filename
				fw_img_log.write(target_file+"\n")
				fw_img = open(target_file, "wb")
				url = zhibei_fowang+src
				fw_img.write(urlopen(url).read())
				fw_img.close()
				#print alternate text
				# print image['alt']
				fw_img_log.write(image['alt']+"\n")
	else:
		fw.write(root+" contains " +str(len(dirs))+" directories and " +str(len(files))+" files.\n")
print("Total number of files: "+str(count))
print("Finished!")
