import json,datetime,sys
sys.setrecursionlimit(3000)
import numpy as np
from sklearn import preprocessing
np.set_printoptions(suppress=True)

class BinaryTree():

    def __init__(self,nodeValue,movieList):
        self.left = None
        self.right = None
        self.nodeValue = nodeValue
        self.movieList = movieList

    def insertRight(self,node):
        self.right = node

    def insertLeft(self,node):
        self.left = node

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

def questionScore(x_train,q_no):
    numberOfOnes = 0
    for a in x_train[:,q_no]:
        if a == 1:
            numberOfOnes = numberOfOnes + 1

    score = float(numberOfOnes)/float((len(x_train[:,q_no])))

    return ((score-0.5)**2)

def findQuestion(x_train):
    print("findQ")
    print(x_train)
    print("Ending findQ")
    # Checks for last movie
    if(len(x_train[1:,0]) <= 1):
        print("movieIf")
        return -1

    # Checks for last question
    if(len(x_train[0,1:]) <= 1):
        print("qeustionIf")
        return -1
   
    questionScores = {}
    for x in range(len(x_train[0,:])-1):
        questionScores[str(x+1)] = str(questionScore(x_train[1:,1:],x))

    #Selecting the question with minimum score in the Dictionary
    questionNumberidx = min(questionScores, key=questionScores.get)
    intQuest = int(questionNumberidx)
    questionNumber = x_train[0,intQuest]
    return questionNumber


def splitting(x_train , questionNumber):

    idx = []
    idx.append(0)
    yes_idx = []
    yes_idx.append(0)
    no_idx = []
    no_idx.append(0)
    q_idx = -1

    counter = 1
    for x in x_train[0,1:]:
        if x != float(questionNumber):
            idx.append(counter)
        else:
            q_idx = counter
        counter = counter + 1
    counter = 1
    for i in x_train[1:,q_idx]:
        if i == 1.0:
            yes_idx.append(counter)
        else:
            no_idx.append(counter)
        counter = counter + 1
    left_x_train = x_train[np.ix_(no_idx,idx)]
    right_x_train = x_train[np.ix_(yes_idx,idx)]

    return (left_x_train , right_x_train)

def simplifying(left_x_train,right_x_train,rootNode,movieList):
    findQL = findQuestion(left_x_train)
    findQR = findQuestion(right_x_train)
    if (findQL == -1) and (findQR == -1):
        #print("Firt if")
        node = BinaryTree("Leaf",left_x_train[1:,0])
        rootNode.insertLeft(node)
        node = BinaryTree("Leaf",right_x_train[1:,0])
        rootNode.insertRight(node)
        return
    elif (findQL == -1) and ( not (findQR == -1)):
        #insert a node with a value "Leaf" to the left
        node = BinaryTree("Leaf",left_x_train[1:,0])
        rootNode.insertLeft(node)
        #code for right subtree
        rightValue = findQR
        node = BinaryTree(rightValue,right_x_train[1:,0])
        rootNode.insertRight(node)
        ( left_right_x_train , right_right_x_train ) = splitting( right_x_train , rightValue )
        simplifying(left_right_x_train,right_right_x_train,node,right_x_train[1:,0])
        return
    elif ( not (findQL == -1)) and (findQR == -1):
        #insert a node with a value "Leaf" to the right
        node = BinaryTree("Leaf",right_x_train[1:,0])
        rootNode.insertRight(node)
        #code for left subtree
        leftValue = findQL
        node = BinaryTree(leftValue,left_x_train[1:,0])
        rootNode.insertLeft(node)
        ( left_left_x_train , right_left_x_train ) = splitting( left_x_train , leftValue )
        simplifying(left_left_x_train,right_left_x_train,node,left_x_train[1:,0])
        return
    else:
        #code for right subtree
        rightValue = findQR
        node = BinaryTree(rightValue,right_x_train[1:,0])
        rootNode.insertRight(node)
        ( left_right_x_train , right_right_x_train ) = splitting( right_x_train , rightValue )
        simplifying(left_right_x_train,right_right_x_train,node,right_x_train[1:,0])

        #code for left subtree
        leftValue = findQL
        node = BinaryTree(leftValue,left_x_train[1:,0])
        rootNode.insertLeft(node)
        ( left_left_x_train , right_left_x_train ) = splitting( left_x_train , leftValue )
        simplifying(left_left_x_train,right_left_x_train,node,left_x_train[1:,0])
        return

f= open("data.txt","r")
fileText=f.read()
fileJson=json.loads(fileText)
movieCount = len(fileJson["json"])
movies = fileJson["json"]
noOfQuestions = 30
matrix = [[0 for y in range(noOfQuestions + 1)] for x in range(movieCount + 1)]

#adding question indices into matrix
for x in range(noOfQuestions):
    matrix[0][x + 1] = x + 1

for row in range(movieCount):

    #initialize id into 2d array
    matrix[row + 1][0] = fileJson["json"][row]["id"]

    #build up current movie cast List
    castList = []
    for cast in movies[row]["cast"]:
        castList.append(cast["name"])

    #start matrix filling
    #vote Feature
    score = float(movies[row]["votes"])/(float(datetime.datetime.now().year+1) - float(movies[row]["releasedate"]))
    matrix[row + 1][1] = score

    #Grossing features
    if (float(movies[row]["revenue"])-float(movies[row]["budget"]))>0 :
        matrix[row + 1][2] = 1

    #Time based features
    if float(movies[row]["releasedate"])<2000:
        matrix[row + 1][3] = 1
    if float(movies[row]["releasedate"])>=2000 and float(movies[row]["releasedate"])<2010 :
        matrix[row + 1][4] = 1
    if float(movies[row]["releasedate"])>=2010:
        matrix[row + 1][5] = 1

    if float(movies[row]["userrating"])>=7:
        matrix[row + 1][6] = 1
    if float(movies[row]["runtime"])<=100:
        matrix[row + 1][7] = 1

    #Genre Features
    if "Action" in movies[row]["genres"]:
        matrix[row + 1][8] = 1
    if "Adventure" in movies[row]["genres"]:
        matrix[row + 1][9] = 1
    if "Animation" in movies[row]["genres"]:
        matrix[row + 1][10] = 1
    if "Comedy" in movies[row]["genres"]:
        matrix[row + 1][11] = 1
    if "Crime" in movies[row]["genres"]:
        matrix[row + 1][12] = 1
    if "Documentary" in movies[row]["genres"]:
        matrix[row + 1][13] = 1
    if "Drama" in movies[row]["genres"]:
        matrix[row + 1][14] = 1
    if "Family" in movies[row]["genres"]:
        matrix[row + 1][15] = 1
    if "Fantasy" in movies[row]["genres"]:
        matrix[row + 1][16] = 1
    if "History" in movies[row]["genres"]:
        matrix[row + 1][17] = 1
    if "Horror" in movies[row]["genres"]:
        matrix[row + 1][18] = 1
    if "Music" in movies[row]["genres"]:
        matrix[row + 1][19] = 1
    if "Mystery" in movies[row]["genres"]:
        matrix[row + 1][20] = 1
    if "Love" in movies[row]["genres"]:
        matrix[row + 1][21] = 1
    if "Science Fiction" in movies[row]["genres"]:
        matrix[row + 1][22] = 1
    if "Thriller" in movies[row]["genres"]:
        matrix[row + 1][23] = 1
    if "War" in movies[row]["genres"]:
        matrix[row + 1][24] = 1

    #Cast Check for popular actors
    if "Henry Cavill" in castList:
        matrix[row + 1][25] = 1
    if "Dwayne Johnson" in castList:
        matrix[row + 1][26] = 1
    if "Emma Watson" in castList:
        matrix[row + 1][27] = 1
    if "Brad Pitt" in castList:
        matrix[row + 1][28] = 1
    if "Jennifer Lawrence" in castList:
        matrix[row + 1][29] = 1
    if "Tom Hardy" in castList:
        matrix[row + 1][30] = 1
f.close()

#type casting entire matrix into float
x_train = np.array(matrix).astype(np.float)

#################################################################
#           MIN MAX SCALING                                     #
# ###############################################################
# X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0)) #
# X_scaled = X_std * (max - min) + min                          #
#          {This gives values between 0 AND 1 }                 #
#################################################################
min_max_scaler = preprocessing.MinMaxScaler()
x_train_minmax = min_max_scaler.fit_transform(x_train[1:,1])
x_scaled = min_max_scaler.transform(x_train[1:,1])
counterscale = 0
for x in x_scaled:
    if x > 0.5 :
        x_scaled[counterscale] = 1
    else:
        x_scaled[counterscale] = 0
    counterscale = counterscale + 1

# puting scaled column back into train data
x_train[1:,1] = x_scaled

#creating the first root node
rootQuestion = findQuestion(x_train)
rootNode = BinaryTree(rootQuestion,x_train[1:,0])
( left_x_train , right_x_train ) = splitting( x_train , rootQuestion )
simplifying(left_x_train,right_x_train,rootNode,x_train[1:,0])

from sklearn.externals import joblib
joblib.dump(rootNode, 'tree.pkl')
