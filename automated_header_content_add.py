import os

# This function is for storing the unique contents in a file for future analysis
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

# For metadata: This function is for converting content list to content string with newline
def list_to_string_with_newline_metadata(watermark_ri, content_list, metadata_type):
	content_string = "\n" + watermark_ri + "\n"
	if len(content_list) == 0:
		print "There is no "+ metadata_type+ " metadata in the file"
	if len(content_list) == 1:
		print "There is only 1 (one) "+ metadata_type+ " metadata in the file"
	if len(content_list) > 1:
		print "There is more than one "+ metadata_type+ " metadata in the file. Total "+ metadata_type+ " metadata: " + str(len(content_list))
	for content in content_list:
		content_string = content_string + "\n" + content
	content_string = content_string + "\n"
	return content_string

# For normal contents: This function is for converting content list to content string with newline
def list_to_string_with_newline(watermark_ri, content_list):
	if watermark_ri:
		content_string = "\n" + watermark_ri + "\n"
	else: 
		content_string = ""
	for content in content_list:
		content_string = content_string + "\n" + content
	content_string = content_string + "\n"
	return content_string

# For DOI contents: This function is for converting doi content list to content string with newline
def lists_to_string(left, right, doi):
	content_string = ""
	# right list
	if right: 	
		for content in right:
			content_string = content_string + "\n" + content
		content_string = content_string + "\n"
	# left list 
	if left:
		for content in left:
			content_string = content_string + "\n" + content
		content_string = content_string + "\n"
	# doi list
	if doi:
		for content in doi:
			content_string = content_string + "\n" + content
		content_string = content_string + "\n"

	return content_string

# This function is to add watermark to the content string 
def watermarking_string(watermark_ri, content_string):
	if watermark_ri:
		content_string = "\n" + watermark_ri + "\n" + content_string
	return content_string


# This function is for inserting the content in the destination file header
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

# This function is for matching the source file name (with parent folder) with destination file name (with parent folder)
def filename_match(source_path, destination_directory): # (done) We need to change this file matching. We need to consider the filepath along with filename. Multiple files with the same name exists. 
	for root, dirs, files in os.walk(destination_directory):
		for f in files:
			destination_full_path = os.path.join(root, f)
			destination_path = destination_full_path.split(destination_directory)[1]
			# print "destination_path: "+destination_path
			if destination_path == source_path:
				return destination_full_path
	return "N/A"

# This function is for reading the header meta content in a single source file  
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



# This function is for reading the header meta content in a single source file 
# Special case: for reading head contents in JARS index files 
def header_content_read_JARS(input_filename):
	meta_content_pattern = ("DC", "schema")
	# comment_pattern = ("<!--", "-->") # Excluding commented links might give raise to bugs. As for now, we are including them
	with open(input_filename) as f_read:
		file_data = f_read.read()
		# print file_data
		content_list = []
		count = 0

		if "<head>" in file_data:
			data_text = file_data.split("<head>")
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

# This function is for counting the total number of files in the source location
def file_count(directory):
	count = 0
	for root, dirs, files in os.walk(directory):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" or ".htm" in filename:
				count = count + 1
				print "#" +str(count) + " input_filename: " + root_and_filename
	pass	

# This function is for calculating missing files, i.e. files that are present in source location but not in destination location
def calculating_missing_files(directory1, directory2):
	count = 0
	missing_files_count = 0
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" or ".htm" in filename:
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

# This function is for automatically copying meta content in the header section of the source files to the destination files
def automated_header_content_generate(directory1, directory2):
	count = 0
	missing_files_count = 0
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" or ".htm" in filename:
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
				watermark_ri = "<!--@rifatsm -- content insert -->"
				content_string = list_to_string_with_newline_metadata(watermark_ri, content_list, "Dublin Core")
				# print content_string

				insert_content(output_root_and_filename, content_string)
				store_meta_content_in_file(content_list)
								
				# if count > 2:	# Regulating condition 
				# 	break

	pass	

# This function is for automatically copying meta content in the header section of the source files to the destination files
# Special Case for JARS files: These files have different extensions for the index files. 
# We consider both `index.htm` and `index.html` files as the same for JARS files
def automated_header_content_generate_JARS(directory1, directory2):
	count = 0
	missing_files_count = 0
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" or ".htm" in filename:
				count = count + 1
				source_filepath = root_and_filename.split(directory1)[1]
				print "#" + str(count) + " source_filepath: " + source_filepath
				if source_filepath.endswith("index.htm"):
					source_filepath = source_filepath + "l"
					print "#" + str(count) + " (new) source_filepath: " + source_filepath
				else:
					continue
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
				print "root_and_filename: " + root_and_filename
				content_list = header_content_read_JARS(root_and_filename)
				# print content_list
				watermark_ri = "<!--@rifatsm -- content insert -->"
				content_string = list_to_string_with_newline_metadata(watermark_ri, content_list, "Dublin Core")
				# print content_string

				insert_content(output_root_and_filename, content_string)
				store_meta_content_in_file(content_list)
								
				# if count > 2:	# Regulating condition 
				# 	break

	pass

# This function is to read the coins_content from a single source file 
def coins_z3988_content_read(input_filename):
	meta_content_pattern = "class=\"Z3988\""
	with open(input_filename) as f_read:
		file_data = f_read.read()
		content_list = []
		line_list = []
		count = 0
		if "<body>" in file_data:
			data_text = file_data.split("<body>")[1]
		else:
			return content_list
		newline = "\n"
		for line in data_text.split(newline):
			count = count + 1
			if meta_content_pattern in line:
				content_list.append(line) 
		return content_list


# This function is to read the missing doi contents from a single source file 
def doi_content_read(input_filename):
	doi_content_pattern = "<div class=\"doi\">"
	right_content_pattern = "<div style=\"float:right; font-weight:bold; margin-right:1.5em\">"
	left_content_pattern = "<div style=\"float:left; font-weight:bold; margin-left:1.5em\">"
	body_pattern_start = "<body>"
	content_string = ""

	with open(input_filename) as f_read:
		file_data = f_read.read()
		doi_content_list = []
		right_content_list = []
		left_content_list = []

		div_end = "</div>"
		flag_doi = 0
		flag_left = 0
		flag_right = 0

		if body_pattern_start in file_data:
			data_text = file_data.split(body_pattern_start)[1]
		else:
			return content_string
		newline = "\n"
		for line in data_text.split(newline):
			# DOI content
			if flag_doi:
				doi_content_list.append("<div class=\"doi\">")	
				doi_content_list.append(line)
				flag_doi = 0 
			if doi_content_pattern in line:
				flag_doi = 1
			# right styling content 
			if flag_right:
				right_content_list.append("<div style=\"float:right; font-weight:bold; margin-right:1.5em\">")	
				right_content_list.append(line)
				flag_right = 0 
			if right_content_pattern in line:
				flag_right = 1
			# left styling content 
			if flag_left:
				left_content_list.append("<div style=\"float:left; font-weight:bold; margin-left:1.5em\">")	
				left_content_list.append(line)
				flag_left = 0 
			if left_content_pattern in line:
				flag_left = 1

		if doi_content_list:
			doi_content_list.append(div_end)
		if left_content_list:	
			left_content_list.append(div_end)
		if right_content_list:	
			right_content_list.append(div_end)	

		content_string = lists_to_string(left_content_list, right_content_list, doi_content_list)
		if content_string:		
			content_string = watermarking_string("<!-- @ri missing doi + left/right content added -------------- -->",content_string)


	if content_string:
		print "content_string: "
		print content_string
	return content_string



# This function calculates the total number of COinS content in a single source file 
def coins_z3988_content_read_total_count(input_filename):
	meta_content_pattern = "class=\"Z3988\""
	length = 0
	with open(input_filename) as f_read:
		file_data = f_read.read()
		data_text = ""
		if "<body>" in file_data:
			data_text = file_data.split("<body>")[1]
			if meta_content_pattern in data_text:
				# print "COinS exists in " + input_filename 
				length = len(data_text.split("class=\"Z3988\""))
				if length > 1:
					print "length: " + str(length)
				# print coins_content
				return True
			else:
				return "N/A"
		else:
			return "N/B"
	return "File Error"

# This function is for inserting COinS content at the start of the body of the destination files
def insert_coins_z3988_content(output_root_and_filename, coins_content):
	data_text = []
	modified_text = ""
	with open(output_root_and_filename) as f_read:
		file_data = f_read.read()
		if coins_content in file_data:
			print "Error: coins already exists!"
			return False
		if "<body>" in file_data:
			data_text = file_data.split("<body>")
			modified_text = data_text[0] + "<body>" + "\n" + coins_content +  data_text[1]
		else:
			print "Error: No <body> found!"
			modified_text = file_data
	with open(output_root_and_filename, "w+") as f_write:
		f_write.write(modified_text) 
	return True

# This function is for inserting missing doi content at the start of the body of the destination files
def insert_doi_content(output_root_and_filename, doi_content):
	data_text = []
	modified_text = ""
	with open(output_root_and_filename) as f_read:
		file_data = f_read.read()
		if doi_content in file_data:
			print "Error: Missing DOI content already exists!"
			return False
		if "<body>" in file_data:
			data_text = file_data.split("<body>")
			if "<h2>" in data_text[1]:
				body_text = data_text[1].split("<h2>")
				modified_text = data_text[0] + "<body>" + body_text[0]  + "\n" + doi_content + "<h2>" + body_text[1]
			elif "</h1>" in data_text[1]:
				print "*=> Could not find Paragraph Header h2. Inserting DOI contents after <h1>"
				body_text = data_text[1].split("</h1>")
				modified_text = data_text[0] + "<body>" + body_text[0] + "</h1>" + "\n" + doi_content +  body_text[1]
			else:
				print "*==> Could not find Paragraph Header h2 & h1. Inserting DOI contents after <body>"
				modified_text = data_text[0] + "<body>" + "\n" + doi_content +  data_text[1]	
		else:
			print "Error: No <body> found!"
			modified_text = file_data
	with open(output_root_and_filename, "w+") as f_write:
		f_write.write(modified_text) 
	return True


def remove_line_without_coins_tag(filename, title_list):
	newline = "\n"
	file_data_list = []
	with open(filename) as f_read:
		file_data = f_read.read()
		file_data_list = file_data.split(newline)
		for line in file_data_list:
			for title in title_list:
				# Excluding Dublin Core (DC) metadata which contains title
				if title in line and "<meta name=\"" not in line:
					file_data_list.remove(line)
	modified_text = list_to_string_with_newline("", file_data_list)
	with open(filename, "w+") as f_write:
		f_write.write(modified_text)
	return True

def check_for_available_coins_z3988_content_sp_1(filename, coins_content):
	newline = "\n"
	title_without_coins_tag = []
	content_store = ""
	with open(filename) as f_read:
		file_data = f_read.read()
		for line in file_data.split(newline):
			if "title=\"" in line and "class=\"Z3988\"" in line: # We are checking title to match instead, we still need to add <class="Z3988"> tag where it is missing
				title = line.split("title=\"")[1]
				title = title.split("\">")[0]
				for content in coins_content:
					if title in content:
						# print "Already exists!!"
						coins_content.remove(content)
			# We are checking title to match instead, we still need to add <class="Z3988"> tag where it is missing
			if "title=\"" in line and "class=\"Z3988\"" not in line: 
				title = line.split("title=\"")[1]
				title = title.split("\">")[0]
				for content in coins_content:
					if title in content:
						# print "Already exists!!"
						title_without_coins_tag.append(title)
		if title_without_coins_tag:
			remove_line_without_coins_tag(filename, title_without_coins_tag)
	return coins_content


def check_for_available_coins_z3988_content(filename, coins_content):
	newline = "\n"
	coins_content_new = []
	content_store = ""
	with open(filename) as f_read:
		file_data = f_read.read()
		for line in file_data.split(newline):
			if "title=\"" in line: # We are checking title to match instead, we still need to add <class="Z3988"> tag where it is missing
				title = line.split("title=\"")[1]
				title = title.split("\">")[0]
				for content in coins_content:
					if title in content:
						# print "Already exists!!"
						coins_content.remove(content)
	return coins_content

# This function is for calculating the number of occurance of COinS pattern in all the files in the source
def automated_coins_z3988_content_total_length_calculation(directory1, directory2):
	count = 0
	missing_files_count = 0
	coins_content_err_msg = ("N/A", "N/B", "File Error")
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" or ".htm" in filename:
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
				coins_z3988_content = coins_z3988_content_read_total_count(root_and_filename)
				
	pass	

# This function is for automatically copying COinS content from source files to destination files. 
def automated_coins_z3988_content_generate(directory1, directory2):
	count = 0
	missing_files_count = 0
	coins_content_err_msg = ("N/A", "N/B", "File Error")
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" or ".htm" in filename:
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
				coins_z3988_content = coins_z3988_content_read(root_and_filename)
				# print "COinS: "+ str(coins_z3988_content)
				if not coins_z3988_content:
					print "Error: COinS list empty"
				else:
					
					# Insert the title check here
					coins_z3988_content_checked = check_for_available_coins_z3988_content(output_root_and_filename, coins_z3988_content)
				
					watermark_ri = "<!-- @ri coins Z3988 content added -------------- -->"
					coins_content_string = list_to_string_with_newline_metadata(watermark_ri, coins_z3988_content_checked, "COinS")
					insert_coins_z3988_content(output_root_and_filename, coins_content_string)

	pass

# Special Case 1: Where the coins metadata is present but without the `Z3988` tag in the line. For this special case, we need to delete
# line with the title
def automated_coins_z3988_content_generate_sp_1(directory1, directory2):
	count = 0
	missing_files_count = 0
	coins_content_err_msg = ("N/A", "N/B", "File Error")
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" or ".htm" in filename:
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
				coins_z3988_content = coins_z3988_content_read(root_and_filename)
				# print "COinS: "+ str(coins_z3988_content)
				if not coins_z3988_content:
					print "Error: COinS list empty"
				else:
					
					# Insert the title check here
					coins_z3988_content_checked = check_for_available_coins_z3988_content_sp_1(output_root_and_filename, coins_z3988_content)
					watermark_ri = "<!-- @ri coins Z3988 content added -------------- -->"
					coins_content_string = list_to_string_with_newline_metadata(watermark_ri, coins_z3988_content_checked, "COinS")
					insert_coins_z3988_content(output_root_and_filename, coins_content_string)

	pass	

# Issue Fixing: ALAN review missing DOI info add 
def automated_coins_z3988_content_missing_doi(directory1, directory2):
	count = 0
	missing_files_count = 0
	coins_content_err_msg = ("N/A", "N/B", "File Error")
	for root, dirs, files in os.walk(directory1):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" or ".htm" in filename:
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
				doi_content = doi_content_read(root_and_filename)
				if not doi_content:
					print "Error: DOI list empty"
				else:
					insert_doi_content(output_root_and_filename, doi_content)
	pass	



# file_count("/Users/rifatsm/scholar-ejournal-meta") # Count 4653 .html files
# file_count("/Users/rifatsm/ejournals_test_set") # Count 5309 .html files
# automated_header_content_generate("/Users/rifatsm/scholar-ejournal-meta/JARS/","/Users/rifatsm/JARS/")

# automated_coins_z3988_content_generate("/Users/rifatsm/scholar-ejournal-meta/ALAN/v28n1","/Users/rifatsm/ejournals_test_set/ALAN/v28n1")
# automated_coins_z3988_content_generate("/Users/rifatsm/scholar-ejournal-meta/JARS","/Users/rifatsm/ejournals_test_set/JARS")

# automated_coins_z3988_content_generate_sp_1("/Users/rifatsm/scholar-ejournal-meta/","/Users/rifatsm/ejournals_test_set/")

# Run the following function on the ALAN and JOTS files 
# automated_coins_z3988_content_missing_doi("/Users/rifatsm/scholar-ejournal-meta/ALAN/","/Users/rifatsm/ejournals_test_set/ALAN/")
# automated_coins_z3988_content_missing_doi("/Users/rifatsm/scholar-ejournal-meta/JOTS/","/Users/rifatsm/ejournals_test_set/JOTS/")

# automated_header_content_generate("/Users/rifatsm/scholar-ejournal-meta","/Users/rifatsm/ejournals_test_set") # Main data sample. The source is actual location. The destination is testing location 
# automated_coins_z3988_content_generate("/Users/rifatsm/scholar-ejournal-meta","/Users/rifatsm/ejournals_test_set") # Main data sample. The source is actual location. The destination is testing location 
# automated_coins_z3988_content_total_length_calculation("/Users/rifatsm/scholar-ejournal-meta","/Users/rifatsm/ejournals_test_set")
# calculating_missing_files("/Users/rifatsm/scholar-ejournal-meta","/Users/rifatsm/ejournals_test_set")
# coins_z3988_content_read("/Users/rifatsm/scholar-ejournal-meta/JTE/v22n1/index.html")

# Special case for JARS files: `index.htm` -> `index.html`
# automated_header_content_generate_JARS("/Users/rifatsm/scholar-ejournal-meta/JARS/","/Users/rifatsm/JARS/")

##################################
# Files that require manual edit:
## /JOTS/v42/v42n2/love.html -- after running the script automated_coins_z3988_content_missing_doi("/Users/rifatsm/scholar-ejournal-meta/JOTS/","/Users/rifatsm/ejournals_test_set/JOTS/")
## All the files (7) under ICC. Manually discard extra content from the COinS metadata 