import os


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
		data_text = file_data.split("</title>")
		if content_string in data_text[1]:
			new_file_data = data_text[0]+"</title>" + data_text[1]
			print "Already exists"
		else:
			new_file_data = data_text[0]+"</title>"+ content_string + data_text[1]
			print "Content inserted"
		
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
		data_text = file_data.split("</title>")
		head_content = data_text[1].split("</head>")[0]
		count = 0
		content_list = []

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


def automated_header_content_generate(directory1, directory2):
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
				

				break

	pass	


automated_header_content_generate("/Users/rifatsm/scholar-ejournal-meta/ALAN/fall94","/Users/rifatsm/ejournals_test_set/ALAN/fall94");