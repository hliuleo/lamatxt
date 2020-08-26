import os, sys
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
src_dir = sys.argv[1] if len(sys.argv) >= 2 else '../html'
dirpath = os.getcwd()
log_files = dirpath+"/remove_space_result.txt"
count = 0
fw = open(log_files, "w")
print(src_dir)
for root, dirs, files in os.walk(src_dir):
	if len(dirs)==0:
		fw.write(root+" contains "+str(len(files))+" files.\n")
		count += len(files)
		for file in files:
			filepath = os.path.join(root, file)
			f = open(filepath, 'r')
			soup = BeautifulSoup(f.read(), 'html.parser')
			print(soup.get_text().rstrip().strip().replace(' ','').replace('\t','').replace('\n',''))
			divs = soup.find_all('div')
			result = ''.join([div.find('p').text.replace('\n','') for div in divs])
			print(result)
			print(filepath)
			break
		if count>1:
			break
	else:
		fw.write(root+" contains " +str(len(dirs))+" directories and " +str(len(files))+" files.\n")
print("Total number of files: "+str(count))
print("Finished!")
