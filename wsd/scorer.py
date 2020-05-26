'''

Info: Jeremy Bailey April 2020

Accuracy is: 84.13%

Most frequent sense baseline: 0.68%

Confusion matrix:

True       phone  product

Predicted               
          
phone         69       17
product        3       37

1) From wsd.py we have assigned a predicted senseID on a test data set. Using this scorer.py program we will now measure 
    how accurate the model from wsd.py was by using the key answers of that test data. We will give the prediction accuracy of the program
    and provide a confusion matrix. The confusion matrix will allow us to see the false positive vs false negative ratio. 

2)  The scorer.py will run as follows:

        python3 scorer.py my-line-answers.txt line-key.txt

    Just as the first one, scorer.py will run using python (hence the python3 parameter). The program will be called
    scorer.py and will give an accuracy of the produced answer from the previous wsd.py. It will do this by taking in the 
    line-key.txt file and comparing it to the the output file my-line-answers.txt to see which were predicted as correct. 

3) By taking both the key and predicted text files, we can iterate them both of them simultaneously and see if they match. 
    if they do match we can increment the number of correct predictions and append the results to two lists that will be 
    used to create the confusion matrix using the "pandas" python library     

 '''
 
import re
import pandas as pd
from sys import argv

#Grab file paths
guesses = str(argv[1])
key = str(argv[2])

correct = 0
incorrect = 0
model_list = []
key_list = []
true = []
pred = []

# Append our model predications to list
with open(argv[1], "r") as file1:
    for x in file1:
        model_list.append(x)

# Append the answer keys to list
with open(argv[2], "r") as file1:
    for x in file1:
        key_list.append(x)

# Iterate through the lists
for i in range(0, len(key_list)):
    try:
        # Compare is senses are the same
        if model_list[i] == key_list[i]:
            # If they are we increase num of correct
            correct += 1
            # And append the sense to our true and pred list
            # using a regex search
            if re.search(r'phone', key_list[i]):
                true.append('phone')
                pred.append('phone')
            else:
                true.append('product')
                pred.append('product')
        # If the actual and predicted are not the same
        else:
            # Find the sense
            if re.search(r'phone', key_list[i]):
                true.append('phone')
                #And set the predicted oposite of the actual
                pred.append('product')
            else:
                true.append('product')
                pred.append('phone')
            # And increase number of incorrect
            incorrect += 1
    except:
        print("length of lists not same size. ERROR!")

# Output accuracy
total = correct + incorrect
acc = (correct / total) * 100
print("Accuacy is: " + str(acc) + " percent")

# Build pandas series from lists
x_true = pd.Series(true, name='True')
y_pred = pd.Series(pred, name='Predicted')

# Generate the confusion matrix from two Series
df_confusion = pd.crosstab(y_pred, x_true)

# Print confusion matrix
print("\n%s" % df_confusion)
