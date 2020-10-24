

def iterate_directories(path):
	import os
	rootdir = 'path'
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			print(os.path.join(subdir, file))


def iterate_folder(directory):
	import os
	files = {}
	key =  directory[-13:-6]
	file_list=[]
	for filename in os.listdir(directory):
	    if filename.endswith(".xml"): 
	        # print(os.path.join(directory, filename))
	        file_list.append(os.path.join(directory, filename))
	        continue
	    else:
	        continue
	files[key] = file_list
	return files
 