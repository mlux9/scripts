# A program that finds all books in the given directory and builds a simple catalog in HTML.
# NOTE: Directory structure is assumed to be ../Dropbox/Public/<calibre root dir>/<script dir>
# NOTE: Working book extensions are: .mobi .azw .azw3 .pdf

import os
import re
import lib
import html

def main():
	# Get file path to the script
	cwd = os.getcwd()
	# Get parent directory of cwd (assumed to be Calibre root directory)
	rootDir = os.path.dirname(cwd) 
	# Get parent directory of rootdir (assumed to be Dropbox Public folder)
	publicDir = os.path.dirname(rootDir)

	# print("cwd is ", cwd)
	# print("rootDir is ", rootDir)
	# print("publicDir is ", publicDir)

	# Checks whether directory structure is in the expected format
	s = re.search(r'Dropbox\/Public$', publicDir)
	if not s:
		print ("Error: Directory structure must be \'../Dropbox/Public/<Calibre Root Directory>/_simple-catalog\'")
		print ("Current directory is \'" + cwd + "\'")
		print ("Exiting")
		return

	lib.globalIni()
	lib.setPublicDir(publicDir)

	lib.setFilter("publisher", "PUBLISHER_NAME") # Basic ignore function

	# Generate bookList and fileList
	lib.traverseAuthorDirs(rootDir)
	lib.sort("title") # Sort by book title

	# Create an HTML catalog file
	f = open('index.html','w')
	f.write(html.printHeader())
	f.write(html.printBookList())
	f.write(html.printFileList())
	f.write(html.printFooter())
	f.close()

	return

if __name__ == "__main__":
    main()