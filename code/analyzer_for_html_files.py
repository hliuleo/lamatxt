import os, sys
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
src_dir = sys.argv[1] if len(sys.argv) >= 2 else '../'
dirpath = os.getcwd()
log_files = dirpath+"/result.txt"
log2_files = dirpath+"/result-general.txt"
dirpath_for_tags = dirpath + "/../"
fw = open(log_files, "w")
fw2 = open(log2_files, "w")
count = 0
tags = {'html'}
clean_tags = {'u','a','h','table','tr','b','t','title','i','p','meta','fimg','ti','td','z','img','sec','hr','st','em','sup','zz','sub','style','zs','h4','kp','h3','hi','font','tbody','sc','br',}

def get_all_tags():
	for root, dirs, files in os.walk(src_dir):
		if len(dirs)==0:
			fw.write(root+" contains "+str(len(files))+" files.\n")
			for file in files:
				if '.html' not in file or '.htm' not in file:
					continue
				filepath = os.path.join(root, file)
				f = open(filepath, 'r')
				soup = BeautifulSoup(f.read(), 'html.parser')
				for tag in soup.find_all(True):
					tags.add(tag.name)
	print(tags)

def mismatched_tags():
	'''
	{'html', 'body', 'head', 'strong', 'p', 'div', 'sub', 'span'}
	'''
	tags_for_matching = {'html', 'body', 'head', 'strong', 'div', 'span'}
	for root, dirs, files in os.walk(src_dir):
		if root.startswith('../code') or root.startswith('../zhibei'):
			continue
		if len(dirs)==0:
			# fw.write(root+" contains "+str(len(files))+" files.\n")
			for file in files:
				if '.html' not in file or '.htm' not in file:
					continue
				filepath = os.path.join(root, file)
				f = open(filepath, 'r')
				soup = BeautifulSoup(f.read(), 'html.parser')
				source = str(soup)
				mismatched_found = False
				mismatched_found2 = False
				for tag in tags_for_matching:
					# print(tag+' '+str(source.count('<'+tag)) + ' == '+str(source.count('</'+tag)))
					if source.count('<'+tag)!=source.count('</'+tag):
						mismatched_found = True
						fw.write(tag+"\n")
					if source.count(tag)%2!=0:
						mismatched_found2 = True
						fw2.write(tag+' = '+str(source.count(tag))+"\n")
				if mismatched_found:
					fw.write(filepath+"\n")
				if mismatched_found2:
					fw2.write(filepath+"\n")
			# break

def retrieve_content_for_all_tags():
	tag_files_html = {}
	tag_files_txt = {}
	for tag in clean_tags:
		out = dirpath_for_tags+"/tags-html/"+tag+".html"
		w = open(out, "w")
		tag_files_html[tag] = w
		out = dirpath_for_tags+"/tags-txt/"+tag+".txt"
		w = open(out, "w")
		tag_files_txt[tag] = w
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
				# for tag in soup.find_all(True):
				# 	tags.add(tag.name)
				for tag in clean_tags:
					try:
						list_contents = soup.find_all(tag)
						if len(list_contents) == 0:
							continue
						tag_files_html[tag].write(filepath+"<p/>\n")
						tag_files_txt[tag].write(filepath+"\n")
						for content in list_contents:
							tag_files_html[tag].write(str(content)+"<p/>\n")
							tag_files_txt[tag].write(str(content)+"\n")
					except:
						tag_files_html[tag].write("error at tag "+tag+" in "+file+"<p/>\n")
						tag_files_txt[tag].write("error at tag "+tag+" in "+file+"\n")
						pass
		else:
			fw.write(root+" contains " +str(len(dirs))+" directories and " +str(len(files))+" files.\n")
	for tag in tags:
		fw.write("\'"+tag+"\',")
	print("Total number of files: "+str(count))
	print("Finished!")

mismatched_tags()