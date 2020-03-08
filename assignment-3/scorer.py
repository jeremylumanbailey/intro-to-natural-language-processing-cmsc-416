import sys
import re
import pandas as pd

def clean_brackets(dirty_string):
    clean_string = re.sub(r"[\[\]]", '', dirty_string)
    cleaner_string = re.sub(r'\|\S+', '', clean_string)
    #cleanest_string = re.sub(r'\/','', cleaner_string)
    return cleaner_string.replace("\/", "")


def main():

    model = ""
    with open(sys.argv[1], "r") as model_arg:
        data = model_arg.read()
        model += data

    answers = ""
    with open(sys.argv[2], "r") as key_arg:
        data = key_arg.read()
        answers += data

    model = clean_brackets(model).split()
    answers = clean_brackets(answers).split()

    key_list = []
    model_list = []

    for each in answers:

        holder = re.split('\/', each)

        tag = holder[1]

        key_list.append(each.split('/')[1])

    for every in model:

        holder = re.split('\/', every)

        tag = holder[1]

        model_list.append(every.split('/')[1])

    # y_true = ['rabbit', 'cat', 'rabbit', 'rabbit', 'cat', 'dog', 'dog', 'rabbit', 'rabbit', 'cat', 'dog', 'rabbit']
    # y_pred = ['cat', 'cat', 'rabbit', 'dog', 'cat', 'rabbit', 'dog', 'cat', 'rabbit', 'cat', 'rabbit', 'rabbit']

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
