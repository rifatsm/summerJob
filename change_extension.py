import os
 
def change_file_ext(cur_dir, old_ext, new_ext, sub_dirs=False):
    if sub_dirs:
        for root, dirs, files in os.walk(cur_dir):
            for filename in files:
                file_ext = os.path.splitext(filename)[1]
                if old_ext == file_ext:
                    oldname = os.path.join(root, filename)
                    newname = oldname.replace(old_ext, new_ext)
                    os.rename(oldname, newname)
    else:
        files = os.listdir(cur_dir)
        for filename in files:
            file_ext = os.path.splitext(filename)[1]
            if old_ext == file_ext:
                newfile = filename.replace(old_ext, new_ext)
                os.rename(filename, newfile)

# Test Link:
# change_file_ext('/Users/rifatsm/Extension Test', '.html', '.md', True)

# Actual Link:
# change_file_ext('/Users/rifatsm/jekyll-test/services/archives/minutes', '.html', '.md', True)
# change_file_ext('/Users/rifatsm/jekyll-test/services/archives/minutes', '.md', '.html', True)
change_file_ext('/Users/rifatsm/jekyll-test/services/archives/minutes/bcm', '.html', '.md', True)