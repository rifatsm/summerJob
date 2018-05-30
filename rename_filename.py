import os
 
def rename_filename(cur_dir, sub_dirs=False):
    print cur_dir
    if sub_dirs:
        for root, dirs, files in os.walk(cur_dir):
            for filename in files:
                print "before: "+filename
                # os.rename(filename, filename.replace("++","+"))
                oldname = os.path.join(root, filename)
                print "oldname: "+oldname
                newfile = filename.replace("+","-").lower()
                newfile = os.path.join(root, newfile)
                print "mid: "+newfile
                os.rename(oldname, newfile)
                print "after: "+filename
    else:
        files = os.listdir(cur_dir)
        print files
        for filename in files:
            print "before: "+filename
            # os.rename(filename, filename.replace("++","+"))
            oldname = os.path.join(root, filename)
            print "oldname: "+oldname
            newfile = filename.replace("+","-").lower()
            newfile = os.path.join(root, newfile)
            print "mid: "+newfile
            os.rename(oldname, newfile)
            print "after: "+filename


# Test Link:
# change_file_ext('/Users/rifatsm/Extension Test', True)

# Actual Link:
rename_filename('/Users/rifatsm/Extension Test/minutes', True)
# change_file_ext('/Users/rifatsm/jekyll-test/services/archives/minutes', True)