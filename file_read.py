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
		output_file = temp[0] + "_out." + temp[1]
		write_top_section_in_file(header, crumbtile_date, output_file)
	return True

# ri_mid: formats the middle section of the file 
def ri_mid(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()
		tag = "pre>"
		data_text = file_data.split(tag)[1][:-2]
		temp = input_filename.split(".")
		output_file = temp[0] + "_out." + temp[1]
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
				data_text = data_text + link[0]+link[1]+"</a>" + "\n"
		# print data_text

		temp = input_filename.split(".")
		output_file = temp[0] + "_out." + temp[1]
		write_middle_section(data_text, output_file)
	return True

def add_line_break(input_filename):
	with open(input_filename) as f_read:
		file_data = f_read.read()
		# print file_data[106:]
		# print file_data[:107]
		modified_data = file_data[108:].replace("\n\n", "<br>\n")
		# print modified_data
		temp = input_filename.split(".")
		output_file = temp[0] + "_2." + temp[1]
		with open(output_file, "w") as f_write:
			f_write.write(file_data[:107])
			f_write.write(modified_data)
	return True

def main(directory):
	for root, dirs, files in os.walk(directory):
		for filename in files:
			root_and_filename = os.path.join(root, filename)
			if ".md" in filename and "index" not in filename:
				print root_and_filename
				top_section = ri_top(root_and_filename)
				if top_section:
					middle_section = ri_mid(root_and_filename)
			if "index.md" in filename:
				print "**************************"
				print root_and_filename
				top_section = ri_top(root_and_filename)
				if top_section:
					index_files = ri_index(root_and_filename) 
	pass

# Calling main function 
# main("/Users/rifatsm/Extension Test/minutes")
add_line_break("august-9-1993_out.md")
# ri_index("index.md")	



# Reading from files and writing

# with open("august-9-1993.md") as f_read:
# 	with open("august-9-1993_out.md") as f_write:
# 		for line in f_read:
# 			f_write.write(line)