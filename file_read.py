## Copy the contents of one file to another

# import os

def scrape_header(tag, line):
	if tag in line:
		header = line.split(tag)[1]
		return header[1:-2].replace(": ", " - ")

def scrape_crumbtile(header):
	print header



# Diagnosting

with open("august-9-1993.md") as f_read:
	# print f_read.read()
	tag = "title"
	print "Header: " + str(scrape_header(tag, f_read.readline()))
	# for line in f_read:
	# 	print "Call Func: " + str(scrape_data_inside_tag(tag, line))



# Reading from files and writing

# with open("august-9-1993.md") as f_read:
# 	with open("august-9-1993_out.md") as f_write:
# 		for line in f_read:
# 			f_write.write(line)