import os
from os import listdir
from os.path import isfile, join
from .models import *
from xml.dom import minidom

mypath = 'D:\\MoneyControl\\New folder'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#print len(onlyfiles)
visited = []
for f in onlyfiles:
	categories = Categories()
	categories.name = findCategory(f)


def findCategory(file):
	xmldoc = minidom.parse(file)
	itemlist = xmldoc.getElementsByTagName('Category')
	print itemlist[0]
	