import os, sys
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import AdvancedHTMLParser
import numpy as np

src_dir = sys.argv[1] if len(sys.argv) >= 2 else '../'
dirpath = os.getcwd()
log_files = dirpath+"/result.txt"
fw = open(log_files, "w")

excludes = set(['code', 'resource', '新添加'])

def mismatched_tags():
	for root, dirs, files in os.walk(src_dir):
		dirs[:] = [d for d in dirs if d not in excludes]
		if len(dirs)==0:
			# fw.write(root+" contains "+str(len(files))+" files.\n")
			for file in files:
				if '.html' not in file or '.htm' not in file:
					continue
				filepath = os.path.join(root, file)
				f = open(filepath, 'r')
				print(filepath)
				soup = BeautifulSoup(f.read(), 'html.parser')
				source = str(soup)

				try:
					AdvancedHTMLParser.Validator.ValidatingAdvancedHTMLParser(filepath)
				except Exception as e:
					fw.write(filepath+"\n")
					fw.write(str(e))
					fw.write("\n")
				try:
					contents = [c for c in soup.body.contents if c!='\n']
					if soup.div != None:
						contents.extend([c for c in soup.div.contents if c!='\n'])
					if any([c.name == None for c in contents]):
						fw.write(filepath+"\n")
						fw.write("text not wrapped\n")
						for t in np.array(contents)[[True if c.name==None else False for c in contents]]:
							fw.write(t+"\n")
				except AttributeError:
					fw.write(filepath+"\n")
					fw.write("text has no body tag\n")
			# break

mismatched_tags()
print("Finished!")
