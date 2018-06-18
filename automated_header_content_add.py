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

def filename_match(source_path, destination_directory): # We need to change this file matching. We need to consider the filepath along with filename. Multiple files with the same name exists. 
	for root, dirs, files in os.walk(destination_directory):
		for f in files:
			destination_full_path = os.path.join(root, f)
			destination_path = destination_full_path.split(destination_directory)[1]
			# print "destination_path: "+destination_path
			if destination_path == source_path:
				return destination_full_path
	return "N/A"

def header_content_read(input_filename):
	meta_content_pattern = ("DC", "schema")
	# comment_pattern = ("<!--", "-->") # Excluding commented links might give raise to bugs. As for now, we are including them
	with open(input_filename) as f_read:
		file_data = f_read.read()
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

def calculating_missing_files(directory1, directory2):
	count = 0
	missing_files_count = 0
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" in filename:
				count = count + 1
				source_filepath = root_and_filename.split(directory1)[1]
				print "#" + str(count) + " source_filepath: " + source_filepath
				output_root_and_filename = filename_match(source_filepath, directory2)
				destination_path = ""
				if directory2 in output_root_and_filename:
					destination_path = output_root_and_filename.split(directory2)[1]
				else:
					destination_path = output_root_and_filename
					missing_files_count = missing_files_count + 1
				print "destination_path: "+destination_path
	print "total matched files: " + str(count)
	print "total missed files: " + str(missing_files_count)

	pass	


def automated_header_content_generate(directory1, directory2):
	count = 0
	missing_files_count = 0
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" in filename:
				count = count + 1
				source_filepath = root_and_filename.split(directory1)[1]
				print "#" + str(count) + " source_filepath: " + source_filepath
				output_root_and_filename = filename_match(source_filepath, directory2)
				destination_path = ""
				if directory2 in output_root_and_filename:
					destination_path = output_root_and_filename.split(directory2)[1]
				else:
					destination_path = output_root_and_filename
					missing_files_count = missing_files_count + 1
				print "destination_path: "+destination_path
				
				if output_root_and_filename == "N/A":
					print "Destination file not found"
					continue
				else:
					print "Output_filename: " + output_root_and_filename
				content_list = header_content_read(root_and_filename)
				# print content_list
				content_string = list_to_string_with_newline(content_list)
				# print content_string

				insert_content(output_root_and_filename, content_string)
				store_meta_content_in_file(content_list)
								
				# if count > 2:	# Regulating condition 
				# 	break

	pass	

def coins_z3988_content_read(input_filename):
	meta_content_pattern = "class=\"Z3988\""
	with open(input_filename) as f_read:
		file_data = f_read.read()
		data_text = ""
		if "<body>" in file_data:
			data_text = file_data.split("<body>")[1]
			if meta_content_pattern in data_text:
				# print "COinS exists in " + input_filename 
				temp_text = data_text.split("<span class=\"Z3988\"")[1]
				temp_text = temp_text.split("</span>")[0]
				coins_content = "<span class=\"Z3988\"" + temp_text + "</span>"
				# print coins_content
				return coins_content
			else:
				return "N/A"
		else:
			return "N/B"
	return "File Error"

def insert_coins_z3988_content(output_root_and_filename, coins_content):
	data_text = []
	ri_comment = "<!-- @ri coins Z3988 content added -------------- -->"
	modified_text = ""
	with open(output_root_and_filename) as f_read:
		file_data = f_read.read()
		if coins_content in file_data:
			print "Error: coins already exists!"
			return False
		if "<body>" in file_data:
			data_text = file_data.split("<body>")
			modified_text = data_text[0] + "<body>" + "\n" + ri_comment + "\n" + coins_content + data_text[1]
		else:
			print "Error: No <body> found!"
			modified_text = file_data
	with open(output_root_and_filename, "w+") as f_write:
		f_write.write(modified_text) 
	return True

def automated_coins_z3988_content_generate(directory1, directory2):
	count = 0
	missing_files_count = 0
	coins_content_err_msg = ("N/A", "N/B", "File Error")
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" in filename:
				count = count + 1
				source_filepath = root_and_filename.split(directory1)[1]
				print "#" + str(count) + " source_filepath: " + source_filepath
				output_root_and_filename = filename_match(source_filepath, directory2)
				destination_path = ""
				if directory2 in output_root_and_filename:
					destination_path = output_root_and_filename.split(directory2)[1]
				else:
					destination_path = output_root_and_filename
					missing_files_count = missing_files_count + 1
				print "destination_path: "+destination_path
				
				if output_root_and_filename == "N/A":
					print "Destination file not found"
					continue
				else:
					print "Output_filename: " + output_root_and_filename
				coins_z3988_content = coins_z3988_content_read(root_and_filename)
				# print coins_z3988_content_list
				if any( s in coins_z3988_content for s in coins_content_err_msg):
					print "Error: " + coins_z3988_content
				else:
					insert_coins_z3988_content(output_root_and_filename, coins_z3988_content)
								
				# if count > 2:	# Regulating condition 
				# 	break

	pass	


# file_count("/Users/rifatsm/scholar-ejournal-meta") # Count 4653 .html files
# file_count("/Users/rifatsm/ejournals_test_set") # Count 5309 .html files
# automated_header_content_generate("/Users/rifatsm/scholar-ejournal-meta/ALAN/fall94","/Users/rifatsm/ejournals_test_set/ALAN/fall94");
automated_coins_z3988_content_generate("/Users/rifatsm/scholar-ejournal-meta/ALAN/winter96","/Users/rifatsm/ejournals_test_set/ALAN/winter96");
# automated_header_content_generate("/Users/rifatsm/scholar-ejournal-meta","/Users/rifatsm/ejournals_test_set"); # Main data sample. The source is actual location. The destination is testing location 
# calculating_missing_files("/Users/rifatsm/scholar-ejournal-meta","/Users/rifatsm/ejournals_test_set"); 
# coins_z3988_content_read("/Users/rifatsm/scholar-ejournal-meta/ALAN/spring99/kaiser.html")
