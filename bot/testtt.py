import re
import os, nltk
from nltk.parse.stanford import StanfordDependencyParser
path = 'D:\\MoneyControl\\stanford-corenlp-full-2017-06-09\\'
path_to_jar = path + 'stanford-corenlp-3.8.0.jar'
path_to_models_jar = path + 'stanford-corenlp-3.8.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar,path_to_models_jar=path_to_models_jar)
os.environ['JAVAHOME'] = 'C:\\Program File\\Java\\jdk1.8.0_102'

regexpSubj = re.compile(r'neg')
regexpObj = re.compile(r'obj')
regexNouns = re.compile("^N.*|^PR.*")
#root = dep.root["word"]
sentences = ["What does the budget have in for a shopkeeper?","The finance ministry came out with a clarification after reports suggested that some unscrupulous elements posing as GST officers have tried to fleece shopkeepers and customers in the name of GST"]
# A random selection of sentences with different styles, domains etc
# ulysses = "In the last budget, Finance Minister Arun Jaitley had said that the first and foremost pillar of his tax proposals was to effectively deal with the problem of black money.Jaitley promised that the government would crackdown on tax evaders and bring back illegal wealth stashed abroad. Progress on this front has been limited so far. The one-time black money compliance window netted barely Rs 3800 crore in 638 declarations. The government has sworn action against those who have not disclosed unaccounted assets abroad. Some stringent measures towards this end can be expected in the Budget. In addition to offense, the FM may also work on defense measures to curb black money through measures to boost cashless transactions. These could include scrapping of convenience fee charged by government departments, slashing merchant discount rate on card transactions, and incentives to promote mobile banking."

# doc = nltk.sent_tokenize(ulysses)
# for s in doc:
#    sentences.append(s)

# sentences = ["He watched the dark eyeslits narrowing with greed till her eyes were green stones",
#             "When will the Oracle 12.2 database be released?",
#             "Coherence is an in-memory grid cluster for Java code",
#             "Oracle 12.2 will be released in March 2017",
#             "PyData community gathers to discuss how best to apply languages and tools to continuously evolving challenges in data management, processing, analytics, and visualization.",
#             "Arsenal are a football team in North London",
#             "When will Arsenal ever win a match?"]

def get_compounds(triples, word):
   compound = []
   for t in triples:
       if t[0][0] == word:
           if regexNouns.search(t[2][1]):
               compound.append(t[2][0])
   return compound

for sentence in sentences:
   
   result = dependency_parser.raw_parse(sentence)
   dep = next(result)
   root = [dep.root["word"]]
   root.append(get_compounds(dep.triples(), root))
   subj = []
   obj = []
   
   for t in dep.triples():
       if regexpSubj.search(t[1]):
           subj.append(t[2][0])
           subj.append(get_compounds(dep.triples(),t[2][0]))
       if regexpObj.search(t[1]):
           obj.append(t[2][0])
           obj.append(get_compounds(dep.triples(),t[2][0]))
   print("\n",sentence)
   print("Subject:",subj, "\nTopic:", root, "\nObject:",obj)