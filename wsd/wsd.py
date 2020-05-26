'''

Info: Jeremy Bailey April 2020

Model: Decision List

Accuracy is: 84.13% 

Most frequent sense baseline: 0.68%

Confusion matrix:

True       phone  product

Predicted               
          
phone         69       17
product        3       37

1) In computational linguistics, word-sense disambiguation is a 
    problem concerned with identifying which sense of a word is used in a sentence. 
    An example of this would be the sentence: "He is right." Depending on the conte-
    xt, this could be refering to the person being correct or the person being the in
    the direction opposite to left. While humans have a natural instinct to understanding this, 
    computers have a difficult time. 

2) For this project we will use two files: wsd.py and scorer.py. The wsd.py will contain a machine learning model 
    that will take in input three files: a training dataset, a test dataset and the model it learns. An example input 
    is as follows: 
                        python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

    python3 is the program used to run the model. The line-train.txt is the training data and should be 
    in an XML format containing the context AND the sense of the word we are trying to figure out (in this case
    "line" is the word we are trying to figure the sense of, line as in product line or line as in phone).
    The line-test.txt is the test data and will be use to see test the model. It also must be in XML format with the context 
    of the word but WITHOUT the sense. The my-model.txt will contain the outputted model and is meant for debugging.
    The my-line-answers.txt will be the STDOUT results of the model.

    

3) To solve this issue I used the decision list model to decide the sense of said word. In the code below you can see
    that the first step was to take training data that had already had it's word sense defined. Using the training data, we extract features including but
    not limited to: the word to the left of the sense, the word to the right of the sense, and all the words in both left and right window "k" number
    away from the sense. For all these features, their frequency was saved. Using these probabilities I was able to calculate the sense given the feature 
    for every feature and every sense. From there I could calculate the Log-Likelihood Ranking of each feature and sense to determine what features best
    determined what sense based on their calculated Log-Likelihood Ranking. Using these Log-Likelihood Ranking we could then test the generated model
    in test data, this test data would have the context but not the senseID. Going through the context we would grab all the features we can from the test data
    and compare it to the generated features from the training data. Because our features are ranked based on their Log-Likelihood we find the highest ranked feature
    that we find in the training data and assign the senseID based on that feature. If no feature in a test context exist in the training feature then we assign the sense
    ID to whatever majority senseID we found in the training data was.

'''

from sys import argv
import re
import math
import operator

#Grab file paths
train = str(argv[1])
test = str(argv[2])

# Open the training data and start parsing it
File = open(train, 'r')
trainList = File.read()
trainList = re.sub(r'<[/]?context>\s|</instance>\s','', trainList)
trainList = trainList.splitlines()

trainList = trainList[2:len(trainList)-2]

newTrainList = []

# Initalize value we will use
sense_x = "<head>line</head>" 
k = 2
list_sense = []
test_sense = []
train_context = []
test_context = []
list_instanceId = []
numerator_dict = {}
denominator_dict = {}
product_feq = 0
phone_freq = 0
major_freq = ""

# Grab all the sense ids in our training set
for x in trainList[1::3]:
    senseID = re.findall('senseid="([^"]*)"', x)
    list_sense.append(senseID[0])
    if senseID[0] == "product":
      product_feq += 1
    else:
      phone_freq += 1

# Set our majority sense based on how many we counted
if phone_freq >= product_feq:
  major_freq = "phone"
else:
  major_freq = "product"

# Grab and clean the context of each training datum
for x in trainList[2::3]:
    x = x.replace('<s>', '')
    x = x.replace('</s>', '')
    x = x.replace('<@>', '')
    x = x.replace('<p>', '')
    x = x.replace('</p>', '')
    x = re.sub( r"\<head\>lines\<\/head\>", "<head>line</head>", x )
    train_context.append(x)


# Begin training the model
for i in range(0, len(train_context)):
    sense = list_sense[i]
    context = train_context[i].split()

    # Find where the sense is located in the context
    for j in range(0, len(context)):
        if context[j] == sense_x:
            pos = j

    # Get the features
    if (pos-1) >= 0:
        left_word = "L: " + context[pos-1]
        
        #Initialize dictionaires
        if sense not in numerator_dict:
            numerator_dict[sense] = {}
        
        if left_word not in numerator_dict[sense]:
            numerator_dict[sense][left_word] = 0
            
        if left_word not in denominator_dict:
            denominator_dict[left_word] = 0
        
        #Increase frequency of found feature
        numerator_dict[sense][left_word] += 1
        denominator_dict[left_word] += 1
    if (pos + 1) < len(context):
        right_word = "R: " + context[pos+1]

        #Initialize dictionaires
        if sense not in numerator_dict:
            numerator_dict[sense] = {}
        
        if right_word not in numerator_dict[sense]:
            numerator_dict[sense][right_word] = 0
            
        if right_word not in denominator_dict:
            denominator_dict[right_word] = 0
        
        #Increase frequency of found feature
        numerator_dict[sense][right_word] += 1
        denominator_dict[right_word] += 1
    if (pos-2) >= 0:
        two_left_word = "2L: " + " ".join(context[pos-2:pos])
        
        #Initialize dictionaires
        if sense not in numerator_dict:
            numerator_dict[sense] = {}
        
        if two_left_word not in numerator_dict[sense]:
            numerator_dict[sense][two_left_word] = 0
            
        if two_left_word not in denominator_dict:
            denominator_dict[two_left_word] = 0
        
        #Increase frequency of found feature
        numerator_dict[sense][two_left_word] += 1
        denominator_dict[two_left_word] += 1

    
    if (pos+2) < len(context):
        two_right_word = "2R: " + " ".join(context[pos+1:pos+3])
        
        #Initialize dictionaires
        if sense not in numerator_dict:
            numerator_dict[sense] = {}

        if two_right_word not in numerator_dict[sense]:
            numerator_dict[sense][two_right_word] = 0
            
        if two_right_word not in denominator_dict:
            denominator_dict[two_right_word] = 0
        
        #Increase frequency of found feature
        numerator_dict[sense][two_right_word] += 1
        denominator_dict[two_right_word] += 1

     
    if (pos-1) >= 0 and (pos + 1) < len(context):
        leftRightPair = "LR: " + context[pos-1] + " " + context[pos+1]
        
        #Initialize dictionaires
        if sense not in numerator_dict:
            numerator_dict[sense] = {}

        if leftRightPair not in numerator_dict[sense]:
            numerator_dict[sense][leftRightPair] = 0
            
        if leftRightPair not in denominator_dict:
            denominator_dict[leftRightPair] = 0
        
        #Increase frequency of found feature
        numerator_dict[sense][leftRightPair] += 1
        denominator_dict[leftRightPair] += 1



    # K-Windowing Algorithm
    start_index = pos - k
    end_index = pos + k + 1
    window_features = context[start_index:end_index]
    for feature in window_features:
        if not re.search( r'\<head', feature ):
            feature = "W: " + feature
            
            #Initialize dictionaires
            if sense not in numerator_dict:
                numerator_dict[sense] = {}
        
            if feature not in numerator_dict[sense]:
                numerator_dict[sense][feature] = 0
                
            if feature not in denominator_dict:
                denominator_dict[feature] = 0
            
            #Increase frequency of found feature
            numerator_dict[sense][feature] += 1
            denominator_dict[feature] += 1

total_num_of_feature = 0
number_of_unique_features = len( denominator_dict )

for feature in denominator_dict:
    total_num_of_feature += denominator_dict[feature]


# Calculate Probabilities
for sense in numerator_dict:
    for feature in denominator_dict:
        denominator = denominator_dict[feature]
        probability = 0
        
        if feature in numerator_dict[sense]:
            numerator = numerator_dict[sense][feature]
            probability = numerator / denominator
        else:
            probability = 1 / (total_num_of_feature + number_of_unique_features)
        
        numerator_dict[sense][feature] = probability

# Calculate Log-Likelihood Ranking
ranking_list = {}

for feature in denominator_dict:
    probs = []
    
    predicted_sense = None
    highest_prob = 0
    
    for sense in numerator_dict:
         probability = numerator_dict[sense][feature]
         probs.append( probability )
         
         if probability > highest_prob:
            highest_prob = probability
            predicted_sense = sense
    
    rank_value = abs( math.log( probs[0] / probs[1] ) )
    
    ranking_list[feature + " <E>|</E> " + predicted_sense] = rank_value

# Sort Values In Descending Order
sorted_ranking_list = dict( sorted(ranking_list.items(), key=operator.itemgetter(1),reverse=True))  

# Write model to file
with open(argv[3], "w") as file:
    for x in sorted_ranking_list:
        file.write(str(x) + " " + str(sorted_ranking_list[x]) + "\n")


# Open the testing data and start parsing it
testfile = open(test, 'r')
testList = testfile.read()
testList = re.sub(r'<[/]?context>\s|</instance>\s','', testList)
testList = testList.splitlines()
testList = testList[2:len(testList)-2]
pos = None

# Grab all the instance IDs to compare accuracy later
for x in testList[::2]:
    instanceId = re.findall('"([^"]*)"', x)
    list_instanceId.append(instanceId)

# Grab and clean the context of each datum
for x in testList[1::2]:
    x = x.lower()
    x = x.replace('<s>', '')
    x = x.replace('</s>', '')
    x = x.replace('<@>', '')
    x = x.replace('<p>', '')
    x = x.replace('</p>', '')
    x = re.sub( r"\<head\>lines\<\/head\>", "<head>line</head>", x )
    test_context.append(x)

# Go through context and use features to predict sense 
for i in range(0, len(test_context)):
    context = test_context[i].split()
    for j in range(0, len(context)):
        if context[j] == sense_x:
            pos = j

# Grab all the features we can
    if (pos-1) >= 0:
        left_word = "L: " + context[pos-1]
        
    if (pos + 1) < len(context):
        right_word = "R: " + context[pos+1]

    if (pos-2) >= 0:
        two_left_word = "2L: " + " ".join(context[pos-2:pos])

    if (pos+2) < len(context):
        two_right_word = "2R: " + " ".join(context[pos+1:pos+3])

    if (pos-1) >= 0 and (pos + 1) < len(context):
        leftRightPair = "LR: " + context[pos-1] + " " + context[pos+1]

    # K-Windowing Algorithm
    start_index = pos - k
    end_index = pos + k + 1
    window_features = context[start_index:end_index]

    # Go through all the features we have sorted 
    currentSense = ""
    for key in sorted_ranking_list:
        featureAndSenseID = key.split(" <E>|</E> ")
        feature = featureAndSenseID[0]
        senseID = featureAndSenseID[1]
        
        # If we find a matching feature, we can break out and make sense prediction
        if left_word == feature:
          currentSense = senseID
          break

        if right_word == feature:
          currentSense = senseID
          break

        if two_left_word == feature:
          currentSense = senseID
          break

        if two_right_word == feature:
          currentSense = senseID
          break

        if leftRightPair == feature:
          currentSense = senseID
          break

        for windowFeature in window_features:
          if not re.search( r'\<head', windowFeature ):
              windowFeature = "W: " + windowFeature
              if windowFeature == feature:
                currentSense = senseID
                break
                
    if currentSense == "":
      # assign majority default if we don't find any matching features  
      currentSense = major_freq

    # Output our predication
    print("<answer instance=\"" + list_instanceId[i][0] +"\" senseid=\""+ currentSense + "\"/>")
