import lib

# Prints HTML header
def printHeader():
	header = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Simple Catalog</title>
  </head>
  <body><font face="Consolas">"""
	return header

# Prints out HTML footer
def printFooter():
	footer = """  </font></body>
</html>"""
	return footer

# Prints data and download link of 'book'
def printBook(book):
	title = "Title: " + book['title'] + "<br>"
	author = "Author: " + book['author'] + "<br>"
	publisher = "Publisher: " + book['publisher'] + "<br>"
	link = "Link: " + book['link'] + "<br>"
	return (title + author + publisher + link)

# Prints data and download link of all books from bookList
def printBookList():
	text = """
	<h3>Calibre Library</h3>
"""
	bookList = lib.getBookList()
	for book in bookList:
		text = text + "<p>" + printBook(book) + "</p>"
	return text

# Prints download link of all files from fileList
def printFileList():
	text = """
	<h3>Files</h3>
"""
	fileList = lib.getFileList()
	for file in fileList:
		text = text + "<p>" + file['name'] + " " + file['link'] + "</p>" 
	return text