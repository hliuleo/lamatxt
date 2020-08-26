# -*- coding: utf-8 -*-
import os
import sys
import difflib
import re
from bs4 import BeautifulSoup

log_file = 'tmp'+os.sep+'cmp_results.txt'

diff_root_dir = 'tmp'+os.sep+'diff'
current_root_dir = '..'+os.sep
original_root_dir = '..'+os.sep+'zhibei'+os.sep

def cleanMe(html):
	html = re.sub(r'\d+','',html)
	soup = BeautifulSoup(html,'html.parser') # create a new bs4 object from the html data loaded
	for script in soup(["script", "style"]): # remove all javascript and stylesheet code
		script.extract()

	chunks = []
	for tag in soup.findAll('p'):
		chunk = tag.getText().replace('\n','').replace('\r','').replace('\t','').replace(' ','')
		chunks.append(chunk)
	text = '\n'.join(chunk for chunk in chunks if chunk)
	# print(text)
	return text

def readfile(filename):
	try:
		fileHandle=open(filename,'r')
		lines=cleanMe(fileHandle.read()).splitlines()
		fileHandle.close()
		return lines
	except IOError as error:
		print('读取文件错误：'+str(error))
		sys.exit()

def text_similar(t1, t2):
    return difflib.SequenceMatcher(None, t1, t2).quick_ratio()

def most_similar_file(cfile, original_dir, original_files):
    tfile1_lines=readfile(cfile)
    sim = 0
    sim_file = None
    for ofile in original_files:
        tfile2_lines=readfile(original_dir+os.sep+ofile)
        s = text_similar(tfile1_lines,tfile2_lines)
        if s>0.9:
            return {'file':ofile, 'sim': s}
        if s>sim:
            sim = s
            sim_file = ofile
    return {'file':sim_file, 'sim': sim}

def diff(ofile, cfile, odir, cdir, diff_dir):
    old_str='charset=ISO-8859-1'
    new_str='charset=UTF-8'
    tfile1_lines=readfile(odir+os.sep+ofile)
    tfile2_lines=readfile(cdir+os.sep+cfile)
    d=difflib.HtmlDiff()
    q=d.make_file(tfile1_lines,tfile2_lines,context=True,numlines=0).replace(' nowrap=\"nowrap\"','')
    with open(diff_dir+os.sep+'diff-'+cfile,'w') as f_new:
        f_new.write(q.replace(old_str,new_str))

def cmp_dirs(current_dir,original_dir,diff_root_dir,fw_log):
    current_files = []
    original_files = []
    
    the_dir = current_dir.split(os.sep)[-1]

    diff_dir = diff_root_dir+os.sep+the_dir
    if not os.path.exists(diff_dir):
        os.makedirs(diff_dir)

    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if not file.startswith('.'):
                current_files.append(file)

    for root, dirs, files in os.walk(original_dir):
        for file in files:
            if not file.startswith('.'):
                original_files.append(file)

    for cfile in current_files:
        sim = most_similar_file(current_dir+os.sep+cfile, original_dir, original_files)
        if not sim['file']:
            continue
        diff(sim['file'],cfile, original_dir, current_dir, diff_dir)
        log = cfile+': '+str(sim)
        print(log)
        fw_log.write(log+"\n")


# entry of the program
dir_pairs = []
for root, dirs, files in os.walk(original_root_dir):
    if 'code' in root or '..'+os.sep+'.' in root or len(files)==0:
        continue
    dir_pair = {}
    dir_pair['original'] = root
    dir_pair['current'] = root.replace('zhibei'+os.sep,'')
    dir_pairs.append(dir_pair)

# print(cmp_dirs)

fw = open(log_file, "w")
count = 0
total = len(dir_pairs)
for pair in dir_pairs:
    count += 1
    print('comparing progress '+str(count)+'/'+str(total))
    cmp_dirs(pair['current'],pair['original'],diff_root_dir,fw)

