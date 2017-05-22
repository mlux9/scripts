import os
import urllib.request
import re

# Initialise global variables
def globalIni():
	global bodyText
	bodyText = ""
	global bookList
	bookList = []
	global fileList
	fileList = []
	global publicDir
	publicDir = ""
	global filterList
	filterList = []
	# global ignoreField
	# ignoreField = ""
	# global ignoreString
	# ignoreString = ""
	return

def setPublicDir(path):
	global publicDir
	publicDir = path
	return

def getBookList():
	return bookList

def getFileList():
	return fileList

def setFilter(f, s):
	filterDict = {'field': f, 'string': s};
	filterList.append(filterDict)

# Initialise and return an empty book dict
def newBookDict():
	new = {}
	new['title'] = ""
	new['author'] = ""
	new['publisher'] = ""
	new['filepath'] = ""
	new['link'] = ""
	new['calibreID'] = -1
	return new

# Goes through directories in the Calibre root directory
# These should be the Author directories
def traverseAuthorDirs(path):
	for authorDir in os.listdir(path):
		authorDirPath = os.path.join(path, authorDir)
		if (authorDir == "_simple-catalog"): # Ignore script folder
			continue
		if os.path.isdir(authorDirPath):
			traverseTitleDirs(authorDirPath)
		else: # Individual file
			addFileList(authorDirPath)
	return

# Goes through directories in the Author directories
# These should be the (book) Title directories
def traverseTitleDirs(path):
	for titleDir in os.listdir(path):
		titleDirPath = os.path.join(path, titleDir)
		if os.path.isdir(titleDirPath): # Level 2: books
			traverseBookDir(titleDirPath)
		# Shouldn't be anything outside of a folder... ignore if so
	return

# Goes through the files in the Title directory
# These should contain the book files and metadata
def traverseBookDir(path):
	for file in os.listdir(path):
		filepath = os.path.join(path, file)
		if (file.endswith(".mobi") or file.endswith(".azw3") or file.endswith(".azw") or file.endswith(".pdf")):
			book = getMetadata(filepath)
			if isFiltered(book):
				continue
			inList = checkBookList(book)
			if not inList:
				bookList.append(book)
			else:
				book = inList
			book['filepath'] = " ".join([book['filepath'], filepath])
			book['link'] = " ".join([book['link'], getLink(filepath)])
	return

# Extracts information from metadata file
# 'filepath' refers to filepath to book
# Information includes: title, author, publisher, calibre ID
def getMetadata(filepath):
	book = newBookDict()
	# Check if metadata file 'metadata.opf' exists in same directory
	dirPath = os.path.dirname(filepath) # Get parent directory path
	metaPath = os.path.join(dirPath, "metadata.opf") # Add metadata.opf to path
	if os.path.exists(metaPath):
		f = open(metaPath, 'r')
		for line in f:
			s = re.search(r'<dc:identifier opf:scheme="calibre" id="calibre_id">(\d+)</dc:identifier>', line)
			if s:
				book['calibreID'] = s.group(1)
			s = re.search(r'<dc:title>(.*)?</dc:title>', line)
			if s:
				book['title'] = s.group(1)
			s = re.search(r'<dc:creator.*?>(.*)?</dc:creator>', line)
			if s:
				book['author'] = s.group(1)
			s = re.search(r'<dc:publisher>(.*)?</dc:publisher>', line)
			if s:
				book['publisher'] = s.group(1)
		f.close()
	return book

# Returns Dropbox link to file with 'filepath'
# Hardcoded Dropbox Public URL for now
# Hypertext is the file extension
def getLink(filepath):
	file = os.path.basename(filepath)
	s = re.search(r'.*\.(.*$)', file)
	if s:
		file = s.group(1)
	base = "https://dl.dropboxusercontent.com/u/NUMBER/"
	tail = os.path.relpath(filepath, publicDir)
	# urllib.request.pathname2url url encodes the file name
	link = "<a href=\"" + base + urllib.request.pathname2url(tail) + "\">" + file + "</a>"
	return link

def addFileList(path):
	name = os.path.basename(path)
	s = re.search(r'(.*)\..*$', name)
	if s:
		name = s.group(1)
	file = {'name': name, 'link': getLink(path)};
	fileList.append(file)
	return

# Checks the book list to see if it has already been added
# Happens when there are multiple book formats in the directory
def checkBookList(new):
	for book in bookList:
		if (book['calibreID'] == new['calibreID']):
			return book
	return

# Default sort is by Author name
def sort(type):
	if (type == "title"):
		# Sort by book title / file name (have to convert to same case to sort properly)
		bookList.sort(key=lambda b: str.lower(b.get('title')))
		fileList.sort(key=lambda f: str.lower(f.get('name')))
	return

# Check whether any filters apply to book
def isFiltered(book):
	for filterDict in filterList:
		if (book.get(filterDict.get('field')) == filterDict.get('string')):
			return True
	return False

# Return the directory structure starting from 'path' as a string
# 'level' refers to directory depth (for indenting)
def getDirTree(path, level):
	tabs = ""
	for i in range(level):
		tabs = tabs + "---"
	nextLevel = level + 1

	text = ""
	if (level == 0):
		text = "[ROOT] @ " + path + "<br>"

	for filename in os.listdir(path):
		filepath = os.path.join(path, filename)
		if (filename == "_simple-catalog"): # Ignore script folder
			continue
		if os.path.isdir(filepath):
			text = text + tabs + "[D]" + filename + "<br>"
			text = text + getDirTree(filepath, nextLevel)
		else:
			text = text + tabs + "[F]" + filename + "<br>"
	return text