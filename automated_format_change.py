## Copy the contents of one file to another

import os, re 

def scrape_header(tag, line):
	if tag in line:
		header = line.split(tag)[1]
		return header[1:-2].replace(": ", " - ")

def scrape_crumbtile(header):
	return header.split(" - ")[1]


def write_top_section_in_file(header, crumbtile_date, output_file):
	bar = "---"
	layout = "layout: strict-rr"
	title = "title: " + header
	crumbtitle = "crumbtitle: " + crumbtile_date
	with open(output_file, "w") as f_write:
		f_write.write(bar)
		f_write.write("\n")
		f_write.write(layout)
		f_write.write("\n")
		f_write.write(title)
		f_write.write("\n")
		f_write.write(crumbtitle)
		f_write.write("\n")
		f_write.write(bar)
		f_write.write("\n")
	return

def write_middle_section(text, output_file):
	with open(output_file, "a+") as f_write:
		f_write.write("\n")
		f_write.write("\n")
		f_write.write(text)
	return


# ri_top: formats the top section of the file 
def ri_top(input_filename):
	with open(input_filename) as f_read:
		# print f_read.read()
		tag = "title"
		header = str(scrape_header(tag, f_read.readline()))
		if " - " in header:
			crumbtile_date = str(scrape_crumbtile(header))
		else:
			return False
		temp = input_filename.split(".")
		output_file = temp[0] + ".md" #+ temp[1]
		# output_file = input_filename
		write_top_section_in_file(header, crumbtile_date, output_file)
	return True

# ri_mid: formats the middle section of the file 
def ri_mid(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()
		tag = "pre>"
		data_text = file_data.split(tag)[1][:-2]
		temp = input_filename.split(".")
		output_file = temp[0] + ".md" # + temp[1]
		# output_file = input_filename
		write_middle_section(data_text, output_file)
	return True

def ri_index(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()
		# link_list = re.search(r'(<li><a href=) .* (</a>)', file_data)
		link_list = re.findall(r'(<li><a href=)([^<]*)', file_data)
		data_text = ""
		if link_list:
			for link in link_list:
				temp_link = link[1]
				temp_link = temp_link.replace("++","-")
				temp_link = temp_link.replace("+","-")
				temp_link = temp_link[0] + temp_link[1].lower() + temp_link[2:]
				data_text = data_text + link[0]+temp_link+"</a>" + "\n"
		# print data_text

		temp = input_filename.split(".")
		output_file = temp[0] + ".md" # + temp[1]
		# output_file = input_filename
		write_middle_section(data_text, output_file)
	return True

# deprecated 
def add_line_break(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()

		# print file_data[106:]
		# print file_data[:107]

		# #############################
		modified_data = file_data[108:].replace("\n\n \n\n", "<br>\n")
		temp = input_filename.split(".")
		output_file = temp[0] + "_2." + temp[1]
		with open(output_file, "w") as f_write:
			f_write.write(file_data[:107])
			f_write.write(modified_data)
		# #############################
	return True

def auto_design_change(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()
		data_text = file_data.split("\n---\n")
		if "Present:" in data_text[1]:
			end_text = data_text[1].split("Present:")
			modified_data = data_text[0] + "\n---\n\n" + "<p><strong>" + end_text[0][5:].replace("  ","").replace("\n\n","<br>") + "<br></strong></p>" + "<br>" + "Present:" + end_text[1]
		elif "PRESENT:" in data_text[1]:
			end_text = data_text[1].split("PRESENT:")
			modified_data = data_text[0] + "\n---\n\n" + "<p><strong>" + end_text[0][5:].replace("  ","").replace("\n\n","<br>") + "<br></strong></p>" + "<br>" + "PRESENT:" + end_text[1]
			# print data_text[1]
			# print data_text
			# print end_text
		else:
			print "@@@@ " +  input_filename
			return False
		
		# print modified_data
		# temp = input_filename.split(".")
		# output_file = temp[0] + "_auto." + temp[1]
		# with open(output_file, "w") as f_write:
		with open(input_filename, "w") as f_write:
			f_write.write(modified_data)
	return True

# Files where paragraph starts with `Minutes` and ends with `Attending`
def unsupported_files_design_change(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()
		data_text = file_data.split("\n---\n")
		if "Attending:" in data_text[1]:
			end_text = data_text[1].split("Attending:")
			modified_data = data_text[0] + "\n---\n\n" + "<p><strong>" + end_text[0][5:].replace("  ","").replace("\n\n","<br>") + "<br></strong></p>" + "<br>" + "Attending:" + end_text[1]
		else:
			print "$$$$ " + input_filename
			return False
		with open(input_filename, "w") as f_write:
			f_write.write(modified_data)
	return True

# A script for automatically reduce the number of breakpoints in the files. 
def reduce_break_points(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()
		modified_data = file_data.replace("<br> <br>", "<br> ")
		modified_data = modified_data.replace("<br>  <br>", "<br> ")
		modified_data = modified_data.replace("<br> <br>", "<br>")

		# temp = input_filename.split(".")
		# output_file = temp[0] + "_out." + temp[1]
		with open(input_filename, "w") as f_write:
			f_write.write(modified_data)
	return True


# Replace ampersand character
def replace_ampersand_char(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()
		if "&amp;" in file_data:
			modified_data = file_data.replace("&amp;", "&")
			print input_filename
		else: 
			modified_data = file_data
		with open(input_filename, "w") as f_write:
			f_write.write(modified_data)
	return True

def main(directory):
	for root, dirs, files in os.walk(directory):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".html" in filename and "index" not in filename:
				print root_and_filename
				top_section = ri_top(root_and_filename)
				if top_section:
					middle_section = ri_mid(root_and_filename)
			if "index.html" in filename:
				print "**************************"
				print root_and_filename
				top_section = ri_top(root_and_filename)
				if top_section:
					index_files = ri_index(root_and_filename) 
	pass

def main_for_auto_design_change(directory):
	count = 0
	failed_file_list = []
	for root, dirs, files in os.walk(directory):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".md" in filename and "index" not in filename:
				print root_and_filename
				result = auto_design_change(root_and_filename)
				if not result:
					count = count + 1
					failed_file_list.append(root_and_filename)
	with open("/Users/rifatsm/jekyll-test/services/archives/failed_file_list.txt", "w") as f_write:
		f_write.write("failed count: " + str(count) + "\n")
		f_write.write("failed file list: \n")
		for file in failed_file_list:
			f_write.write(str(file))
			f_write.write("\n")
	print "failed count: " + str(count)
	print "failed file list: " + str(failed_file_list)
	pass

def main_for_reduce_breakpoints(directory):
	for root, dirs, files in os.walk(directory):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".md" in filename and "index" not in filename:
				# print root_and_filename
				result = reduce_break_points(root_and_filename)
				if not result:
					print root_and_filename
	pass


def main_for_replace_ampersand(directory):
	for root, dirs, files in os.walk(directory):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".md" in filename and "index" not in filename:
				# print root_and_filename
				result = replace_ampersand_char(root_and_filename)
				if not result:
					print "### " + root_and_filename
	pass

def files_count(directory):
	count = 0
	for root, dirs, files in os.walk(directory):
		for filename in files:
			count = count + 1 
	print count 
			
	pass
# Calling main function 
# Testing location 
# main("/Users/rifatsm/Extension Test/minutes")

# Actual location 
# main("/Users/rifatsm/jekyll-test/services/archives/minutes")
# Auto Design Change Main
# main_for_auto_design_change("/Users/rifatsm/Extension Test/auto_design_change_data/minutes")
# main_for_auto_design_change("/Users/rifatsm/jekyll-test/services/archives/minutes")
# main_for_replace_ampersand("/Users/rifatsm/jekyll-test/services/archives/minutes")
# files_count("/Users/rifatsm/jekyll-test/services/archives/minutes")


# reduce_break_points("august-9-1993.md")



# auto_design_change("august-9-1993.md")

# add_line_break("august-9-1993_out.md")
# ri_index("index.html")	 



# Reading from files and writing

# with open("august-9-1993.md") as f_read:
# 	with open("august-9-1993_out.md") as f_write:
# 		for line in f_read:
# 			f_write.write(line)