## Copy the contents of one file to another

import re

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


# ri 
def ri(input_filename):
	with open(input_filename) as f_read:
	# print f_read.read()
		tag = "title"
		header = str(scrape_header(tag, f_read.readline()))
		crumbtile_date = str(scrape_crumbtile(header))
		temp = input_filename.split(".")
		output_file = temp[0] + "_out." + temp[1]
		write_top_section_in_file(header, crumbtile_date, output_file)
	return



def main():
	ri("august-9-1993.md")
	pass

# Calling main function 
main()	



# Reading from files and writing

# with open("august-9-1993.md") as f_read:
# 	with open("august-9-1993_out.md") as f_write:
# 		for line in f_read:
# 			f_write.write(line)