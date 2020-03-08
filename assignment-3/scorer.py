import sys
import re
import pandas as pd


# Cleans that brackets from the data, as well as other sanitizing
def clean_brackets(dirty_string):
    clean_string = re.sub(r"[\[\]]", '', dirty_string)
    cleaner_string = re.sub(r'\|\S+', '', clean_string)
    return cleaner_string.replace("\/", "")


# Main function where I run most of the code
def main():

    # Load the tagged words from pos-test-with-tags.txt
    model = ""
    with open(sys.argv[1], "r") as model_arg:
        data = model_arg.read()
        model += data

    # Load the gold standard from pos-test-key.txt
    answers = ""
    with open(sys.argv[2], "r") as key_arg:
        data = key_arg.read()
        answers += data

    # Clean up data from answer and model
    model = clean_brackets(model).split()
    answers = clean_brackets(answers).split()
    key_list = []
    model_list = []

    # Fill key_list with tags
    for each in answers:
        tmp_arr = re.split('\/', each)
        tag = tmp_arr[1]
        key_list.append(tag)

    # Fill model_list with tags
    for every in model:
        tmp_arr = re.split('\/', every)
        tag = tmp_arr[1]
        model_list.append(tag)

    # # Print Statistics about general accuracy
    # print("Correct: " + str(correct))
    # print("Total: " + str(len(pred_tags)))
    # print("Accuracy: " + str(round((correct/x)*100, 4)) + "%") # 4 decimal places

    # # Create Pandas Series given dictionary entries
    # x_true = pd.Series(y_true, name='True')
    # y_pred = pd.Series(y_pred, name='Predicted')

    # Create Pandas Series given dictionary entries
    x_true = pd.Series(key_list, name='True')
    y_pred = pd.Series(model_list, name='Predicted')

    # Generate the confusion matrix from two Series
    df_confusion = pd.crosstab(y_pred, x_true)

    # Required flag to not truncate output for STDOUT
    pd.set_option('display.expand_frame_repr', False)


    # Print the confusion matrix to STDOUT
    print("\n%s" % df_confusion)

    with open("out.txt", "w") as file:
            file.write('%s\n' % df_confusion)


if __name__ == "__main__":
    main()
