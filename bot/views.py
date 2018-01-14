from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login
from django.core.exceptions import *
from .models import *
import urllib
import requests
from django.http import HttpResponse
import json,math
import os
from django.conf import settings
import pytesseract
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser
from os import listdir
from os.path import isfile, join
from xml.dom import minidom
import xml.etree.ElementTree as ET
import string
from pattern.text.en import singularize
from nltk.corpus import wordnet
from pycorenlp import StanfordCoreNLP
import pprint


nltk.download("reuters")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('brown')
#nltk.download("")
yesnowords = ["can","could", "would", "is", "does", "has", "was", "were", "had", "have", "did", "are", "will"]
commonwords = ["the", "a", "an", "is", "are", "were", "."]
questionwords = ["who", "what", "where", "when", "why", "how", "whose", "which", "whom"]

nlp = StanfordCoreNLP("http://localhost:9000")

#noise_list = ["is", "a", "this", "..."]
def wassup(request):
	mypath = 'D:\\MoneyControl\\New folder'
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

	##print len(onlyfiles)
	visited = []
	for f in onlyfiles:
		cat = findCategory(f)
		if cat not in visited:
			categories = Categories()
			categories.name = cat
			categories.save()
			visited.append(cat)
	return HttpResponse("BITCHHHHHHHHHHH")

def findCategory(file):
	tree = ET.parse('D:\\MoneyControl\\New folder\\'+file)
	root = tree.getroot()
	return (root[0].find("Category").text)

def scripting(request):
	lem = WordNetLemmatizer()
	mypath = 'D:\\MoneyControl\\New folder'
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

	##print len(onlyfiles)
	visited = []
	jsonn = {}
	jsonn['a'] = {}
	jsonn['b'] = {}
	jsonn['c'] = {}
	jsonn['d'] = {}
	jsonn['e'] = {}
	jsonn['f'] = {}
	jsonn['g'] = {}
	jsonn['h'] = {}
	jsonn['i'] = {}
	jsonn['j'] = {}
	jsonn['k'] = {}
	jsonn['l'] = {}
	jsonn['m'] = {}
	jsonn['n'] = {}
	jsonn['o'] = {}
	jsonn['p'] = {}
	jsonn['q'] = {}
	jsonn['r'] = {}
	jsonn['s'] = {}
	jsonn['t'] = {}
	jsonn['u'] = {}
	jsonn['v'] = {}
	jsonn['w'] = {}
	jsonn['x'] = {}
	jsonn['y'] = {}
	jsonn['z'] = {}

	#print json.dumps(jsonn)
	c = 0
	for f in onlyfiles:
		summary = findSummary(f)
		wordsWithoutNoise = remove_noise(summary)
		for word in wordsWithoutNoise:
			try:
				word = word.lower()
				word = word.replace("'","")
				word = word.replace('"',"")
				word = word.replace(",","")
				word = word.replace(".","")
				word = word.replace(":","")
				word = word.replace("!","")
				word = word.replace("?","")
				word = word.replace(";","")
				word = word.replace(")","")
				word = word.replace("(","")
				word = word.replace("&","")
				word = word.replace("#","")
				for i in range(10):
					word = word.replace(str(i),'')
				#print word
				if word is not "" and word[0] >= 'a' and word[0] <= 'z':
					try:
						word = lem.lemmatize(word)
						word = singularize(word)
						jsonn[''+(word[0])][''+word].append(f)	
					except KeyError:
						jsonn[''+(word[0])][''+word]=[]
						jsonn[''+(word[0])][''+word].append(f)
				else:
					#print "ignored"
					pass
			except UnicodeEncodeError:
				#print "FILEEEE"+f
				pass
				# c = 1
				# #print "TRIEDDDDDDDDDDDd	"
	##print(json.dumps(jsonn))
	f = open("data.json","w")
	#print c
	f.write(''+json.dumps(jsonn).encode("utf-8"))
	f.close()
	return HttpResponse("BITCHHHHHHHHHHH")

def findSummary(file):
	#print(file)
	try:
		tree = ET.parse('D:\\MoneyControl\\New folder\\'+file)
		root = tree.getroot()
		##print(root[0].find("Summary").text)
	except UnicodeEncodeError:
		pass
		##print "countttt = "+str(count)
	return (root[0].find("Summary").text + "" + root[0].find("Heading").text)

def findBody(file):
	##print(file)
	try:
		tree = ET.parse('D:\\MoneyControl\\New folder\\'+file)
		root = tree.getroot()
		##print(root[0].find("Body").text)
	except UnicodeEncodeError:
		pass
		##print "countttt = "+str(count)
	return (root[0].find("Body").text + " " + root[0].find("Heading").text)

def hackabot(request):
	return render(request, 'chats.html')

def questAnalysis(request):
	question = request.body[6:]
	question = urllib.unquote(question).decode('utf8')
	print question
	question = question.lower()
	question = question.replace("+"," ")
	question = question.replace("'s","")
	question = question.replace("?"," ")
	question = question.replace("!"," ")
	question = question.replace("."," ")
	question = question.replace(";"," ")
	question = question.replace("'","")
	question = question.replace('"',"")
	question = question.replace("-"," ")
	questWithoutNoise = remove_noise(question)
	questLemmatized = lemmatizing(questWithoutNoise)
	year = []
	if '2016' in questLemmatized:
		year.append('2016')
	if '2017' in questLemmatized:
		year.append('2017')
	fileList = []
	fileDict = {}
	missingWords = []
	foundWords = []
	wordDict = {}
	synonyms = []
	f = open("data.json","r")
	fileText = f.read()
	fileJsoned = json.loads(fileText)
	for word in questLemmatized:
		try:
			length = len(fileJsoned[""+word[0]][""+word])
			for i in range(0,length):
				fileName = fileJsoned[""+word[0]][""+word][i]
				if fileName not in fileList:
					fileList.append(fileName)
					fileDict[""+fileName] = {}
					fileDict[""+fileName]["count"] = 1
				else:
					fileDict[""+fileName]["count"] = (fileDict[""+fileName]["count"] + 1)
			foundWords.append(word)
		except KeyError:
			if word not in missingWords:
				missingWords.append(word)
	n = len(fileDict)
	for word in foundWords:
		df = len(fileJsoned[""+word[0]][""+word])
		idf = math.log(1.0*n/df)
		wordDict[""+word] = idf
	for file in fileList:
		tfidf = 0
		for word in foundWords:
			synonyms = []
			tf = 0
			for syn in wordnet.synsets(word):
			    for l in syn.lemmas():
        			synonyms.append(l.name())
			for syn in synonyms:
				tf = tf + findBody(file).count(syn)
			if word not in synonyms:
				tf = tf + findBody(file).count(word)
			for y in year:
				tf = tf + ((y and ('2016' in file))) + ((y and ('2017' in file)))
			tfidf = tfidf + 1.0*tf*wordDict[""+word]
		fileDict[""+file]["tfidf"] = tfidf
	maxFiles = []
	maxi = 0
	for file in fileList:
		#print file
		if maxi == fileDict[""+file]["tfidf"]:
			maxFiles.append(file)
		elif maxi < fileDict[""+file]["tfidf"]:
			maxFiles = []
			maxi = fileDict[""+file]["tfidf"]
			maxFiles.append(file)

	# if len(maxFiles) == 1:
	# 	#print maxFiles[0]
	# else:
	# 	#print maxFiles
	print('preparing '+str(len(maxFiles)))
	response_array = {}
	if len(maxFiles) is not 0:
		tree = ET.parse('D:\\MoneyControl\\New folder\\'+maxFiles[0])
		root = tree.getroot()
		response_array['success']='1'
		response_array['data']={}
		response_array['data']['heading'] = root[0].find("Heading").text
		response_array['data']['summary'] = root[0].find("Summary").text
		response_array['data']['url'] = root[0].find("URL").text
		response_array['data']['img'] = root[0].find("Image").text
	else:
		response_array['success'] = '1'
		response_array['data']={}
		response_array['data']['heading'] = "Google Search"
		response_array['data']['summary'] = "Do you want me to search google for you?"
		response_array['data']['img'] = 'https://www.blog.google/static/blog/images/google-200x200.7714256da16f.png'
		question = question.replace(" ","+")
		response_array['data']['url'] = 'https://www.google.com/search?q='+question
	return HttpResponse(json.dumps(response_array), status=200, content_type="application/json")

def trial(request):
	text = 'Raj is a boy. He is gay. He can never like girls.'

	output = nlp.annotate(text, properties={'annotators': 'tokenize,ssplit,pos,depparse,parse','outputFormat': 'json'})

	print [s['parse'] for s in output['sentences']]
	return HttpResponse("Done")

def bitch(request):
	text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
	a = text.similar('The woman bought over $150,000 worth of clothes.')
	return HttpResponse(a)

def hey(request):
	stri = "What is the GDP of India and is France developed?"
	stri2 = "Money allocated for education in this budget"
	words = remove_noise(stri)
	lemmatizedWords = lemmatizing(words)
	(type,target) = processquestion(stri.replace("?","").split(" "))
	#print(lemmatizedWords)
	grammarizedSent = grammarize(stri)
	# #print("-----------------------\n")
	# grammarizedSent = grammarize(stri2)
	return HttpResponse("type"+type+" ".join(target))
kuchtohkarnekliye = ""
def processquestion(qwords):
    
    # Find "question word" (what, who, where, etc.)
    questionword = ""
    qidx = -1

    typedict = {}
    typedict["who"] = "PERSON"
    typedict["what"] = "MISC"
    typedict["whose"] = "PERSON"
    typedict["whom"] = "PERSON"
    typedict["where"] = "PLACE"
    typedict["when"] = "TIME"
    typedict["how few"] = "QUANTITY"
    typedict["how little"] = "QUANTITY"
    typedict["how much"] = "QUANTITY"
    typedict["how many"] = "QUANTITY"
    typedict["how young"] = "TIME"
    typedict["how old"] = "TIME"
    typedict["how long"] = "TIME"
    for (idx, word) in enumerate(qwords):
        if word.lower() in questionwords:
            questionword = word.lower()
            qidx = idx
            break
        elif word.lower() in yesnowords:
            return ("YESNO", qwords)

    if qidx < 0:
        return ("MISC", qwords)

    #Removing questionword from question
    if qidx > len(qwords) - 3:
        target = qwords[:qidx]
    else:
        target = qwords[qidx+1:]

    type = "MISC"
    #target = [1,2,3]
    # Determine question type
    # if questionword in ["who", "whose", "whom"]:
    #     type = "PERSON"
    # elif questionword == "where":
    #     type = "PLACE"
    # elif questionword == "when":
    #     type = "TIME"
    # elif questionword == "how":
    #     if target[0] in ["few", "little", "much", "many"]:
    #         type = "QUANTITY"
    #         target = target[1:]
    #     elif target[0] in ["young", "old", "long"]:
    #         type = "TIME"
    #         target = target[1:]
    try:	
	    if questionword is "how":
	    	type = typedict[""+questionword+" "+target[0]]
	    else:
	    	type = typedict[""+questionword]
    except KeyError:
		kuchtohkarnekliye = questionword

    # Trim possible extra helper verb
    if questionword == "which":
        target = target[1:]
    if target[0] in yesnowords:
        target = target[1:]
    
    # Return question data
    return (type, target)

def remove_noise(input_text):
	from nltk.corpus import stopwords
	import string
	words = input_text.split()
	# noise_free_words = [word for word in words if word not in noise_list] 
	noise_free_words = [w for w in words if w.lower() not in stopwords.words('english') ]
	punctCombo = [c+"\"" for c in string.punctuation ]+ ["\""+c for c in string.punctuation ]
	noisePunct_free_words = [w for w in noise_free_words if w not in punctCombo]
	return noisePunct_free_words

def lemmatizing(words):
	lem = WordNetLemmatizer()
	counter = 0
	for word in words:
		words[counter] = lem.lemmatize(word)
		counter = counter + 1
	words = [singularize(plural) for plural in words]
	return words

def grammarize(sentence):
	# wordsssss = remove_noise(sentence)
	# sentence =""
	# for w in wordsssss:
	# 	sentence = sentence + w + " "
	path = 'D:\\MoneyControl\\stanford-corenlp-full-2017-06-09\\'
	path_to_jar = path + 'stanford-corenlp-3.8.0.jar'
	path_to_models_jar = path + 'stanford-corenlp-3.8.0-models.jar'
	dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar,path_to_models_jar=path_to_models_jar)
	os.environ['JAVAHOME'] = 'C:\\Program File\\Java\\jdk1.8.0_102'


	result = dependency_parser.raw_parse(sentence)
	dep = next(result)  # get next item from the iterator result
	for t in dep.triples():
		print(t)
		pass
	dep.root["word"]
	list(dep.tree())
	#subj, nmod
	return ''


