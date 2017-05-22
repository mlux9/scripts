import os
import sys
import xml.etree.ElementTree as et

def main():
    filepath = 'save.txt'

    if not os.path.exists(filepath):
        print('Error: File does not exist')
        sys.exit()

    tree = et.parse('save.txt')
    root = tree.getroot()

    for item in root.findall('player/craftingRecipes/item'):
        name = item.find('key/string').text
        amount = item.find('value/int').text
        print(amount.ljust(5), name) 
		# print('{:25} {}'.format(name, amount))

def printChildren(element):
    print(element.tag)
    if len(element) > 0:
        for child in element:
            printChildren(child)

if __name__ == "__main__":
    main()
