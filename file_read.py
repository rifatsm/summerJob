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
	return

def main():
	cur_dir = "/Users/rifatsm/Extension Test/minutes"
	# print os.listdir(cur_dir) # lists the directories in the current directory
	os_walk = os.walk(cur_dir)
	md_list = []
	i=0
	regex = re.compile(".*(.md)")

	for root, dirs, files in os.walk(cur_dir):
		for filename in files:
			if ".md" in filename and "index" not in filename:
				print os.path.join(root, filename)
				top_section = ri_top(os.path.join(root, filename))
				if top_section:
					middle_section = ri_mid(os.path.join(root, filename))
	pass

# Calling main function 
main()	



# Reading from files and writing

# with open("august-9-1993.md") as f_read:
# 	with open("august-9-1993_out.md") as f_write:
# 		for line in f_read:
# 			f_write.write(line)