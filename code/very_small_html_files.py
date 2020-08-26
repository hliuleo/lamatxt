import os, sys
# -*- coding: utf-8 -*-

src_dir = sys.argv[1] if len(sys.argv) >= 2 else '../'
dirpath = os.getcwd()
log_files = dirpath+"/result.txt"
count = 0
fw = open(log_files, "w")
print(src_dir)
for root, dirs, files in os.walk(src_dir):
	if 'code' in root or '../.' in root:
		continue
	# new_dir = 'zhibei/'+root.replace('../','')
	# print(new_dir)
	# if not os.path.exists(new_dir):
	# 	os.makedirs(new_dir)
	count += len(files)
	for file in files:
		filepath = os.path.join(root, file)
		f = open(filepath, 'r')
		if os.path.getsize(filepath)<300:
			fw.write(filepath+"\n")
			print(filepath)
print("Total number of files: "+str(count))
print("Finished!")
