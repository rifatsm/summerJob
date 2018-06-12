import os


def store_meta_content_in_file(content_list):
	filename = "/Users/rifatsm/Tasks/ejournals_meta_content.txt"
	file_data = ""
	data_text = [""]
	with open(filename) as f_read:
		file_data = f_read.read()
		if file_data:
			data_text = file_data.split("rifatsm_count: ")
			if data_text[1]:
				# print "data_text: " + data_text[1][0:]
				count = int(data_text[1][0:])
			else: 
				count = 1
		else: 
			count = 0
	with open(filename, "w+") as f_write:
		flag = 0
		f_write.write(data_text[0])
		f_write.write("\n")
		f_write.write(str(count))
		for content in content_list:
			if content not in file_data:
				f_write.write("\n")
				f_write.write(content)
				flag = 1
		if flag == 0:
			f_write.write("\n")
			f_write.write("rifatsm_count: " + str(count))
		else:
			f_write.write("\n")
			f_write.write("rifatsm_count: " + str(count+1))
		
	return True


def check_if_unique_content(content):

	return True

def list_to_string_with_newline(content_list):
	content_string = "\n\n<!--@rifatsm -- content insert -->\n\n"
	for content in content_list:
		content_string = content_string + content + "\n"
	return content_string

def insert_content(output_root_and_filename, content_string):
	new_file_data = ""
	with open(output_root_and_filename) as f_destination:
		file_data = f_destination.read()
		if "</title>" not in file_data:
			return False
		data_text = file_data.split("</title>")
		if content_string in data_text[1]:
			new_file_data = data_text[0]+"</title>" + data_text[1]
			# print "Already exists"
		else:
			new_file_data = data_text[0]+"</title>"+ content_string + data_text[1]
			# print "Content inserted"
		
	with open(output_root_and_filename,"w+") as f_write:	
		f_write.write(new_file_data)
	return True

def filename_match(filename, directory):
	for root, dirs, files in os.walk(directory):
		for f in files:
			if f == filename:
				return os.path.join(root, f)
	return "N/A"

def header_content_read(input_filename):
	meta_content_pattern = ("DC", "schema")
	# comment_pattern = ("<!--", "-->") # Excluding commented links might give raise to bugs. As for now, we are including them
	with open(input_filename) as f_read:
		file_data = f_read.read();
		# print file_data
		content_list = []
		count = 0

		if "</title>" in file_data:
			data_text = file_data.split("</title>")
		else:
			return content_list
		if "</head>" in data_text[1]:
			head_content = data_text[1].split("</head>")[0]
		else:
			return content_list

		for line in head_content.split("\n"):
			count = count + 1
			# if "http-equiv" or "stylesheet" or "script" in line:
			# 	print str(count) + " <discard>" + line
			if any( s in line for s in meta_content_pattern):
				# print str(count) + " [include]" + line
				content_list.append(line)
			# else:
				# print str(count) + " <discard>" + line

		# print content_list
	return content_list


def file_count(directory):
	count = 0
	for root, dirs, files in os.walk(directory):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" in filename:
				count = count + 1
				print "#" +str(count) + " input_filename: " + root_and_filename
	pass	



def automated_header_content_generate(directory1, directory2):
	count = 0
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" in filename:
				print "input_filename: " + root_and_filename
				output_root_and_filename = filename_match(filename, directory2)
				if output_root_and_filename == "N/A":
					print "Destination file not found"
					continue
				else:
					print output_root_and_filename
				content_list = header_content_read(root_and_filename)
				# print content_list
				content_string = list_to_string_with_newline(content_list)
				# print content_string
				insert_content(output_root_and_filename, content_string)
				store_meta_content_in_file(content_list)
				count = count + 1
				
				if count > 20:	# Regulating condition 
					break

	pass	


# file_count("/Users/rifatsm/scholar-ejournal-meta") # Count 4653 .html files
# file_count("/Users/rifatsm/ejournals_test_set") # Count 5309 .html files
# automated_header_content_generate("/Users/rifatsm/scholar-ejournal-meta/ALAN/fall94","/Users/rifatsm/ejournals_test_set/ALAN/fall94");
automated_header_content_generate("/Users/rifatsm/scholar-ejournal-meta","/Users/rifatsm/ejournals_test_set"); # Main data sample. The source is actual location. The destination is testing location 
