'''

Name: Jeremy Bailey     Date: March 8th 2020

1)  Part Of Speech tagging is a way in linguistics of marking up a word in a text as corresponding to a
particular part of speech.

'''

import sys
import re


def clean_brackets(dirty_string):
    clean_string = re.sub(r"[\[\]]", '', dirty_string)
    return clean_string


def findWordTagFreq(word_tag_list):
    my_dict = {}
    for every_pair in word_tag_list:
        word = every_pair.split("/")[0]
        tag = every_pair.split("/")[1]

        if word in my_dict:
            if tag in my_dict[word]:
                my_dict[word][tag] += 1
            else:
                my_dict[word][tag] = {}
                my_dict[word][tag] = 1
        else:
            my_dict[word] = {}
            my_dict[word][tag] = {}
            my_dict[word][tag] = 1

    return my_dict


def main():

    #
    train_text = ""
    with open(sys.argv[1], "r") as train_arg:
        data = train_arg.read()
        train_text += data

    test_text = ""
    with open(sys.argv[2], "r") as test_arg:
        data = test_arg.read()
        test_text += data

    train_text_list = clean_brackets(train_text).split()


    word_tag = {}
    tag_his = {}
    prev_tag = ''

    for every_pair in train_text_list:
        word = every_pair.split("/")[0]
        tag = every_pair.split("/")[1]


        if word in word_tag:
            if tag in word_tag[word]:
                word_tag[word][tag] += 1
            else:
                word_tag[word][tag] = {}
                word_tag[word][tag] = 1
        else:
            word_tag[word] = {}
            word_tag[word][tag] = {}
            word_tag[word][tag] = 1

        #
        if prev_tag in tag_his:
            if tag in tag_his[prev_tag]:
                tag_his[prev_tag][tag] += 1
            else:
                tag_his[prev_tag] = {}
                tag_his[prev_tag][tag] = 1
        elif prev_tag != '':
            tag_his[prev_tag] = {}
            tag_his[prev_tag][tag] = {}
            tag_his[prev_tag][tag] = 1
        #
        prev_tag = tag
    # end of for loop

    # Start parsing test data

    test_list = clean_brackets(test_text).split()
    final_list = []
    prev_tag = None



    for every_word in test_list:
        if every_word not in word_tag:
            final_list.append(every_word + "/" + "NN")
            continue

        tmp_prob = 0
        current_prob = 0

        # First word without prev_tag edge case
        if prev_tag is None:
            for tag, tag_value in word_tag[every_word].items():
                tmp_prob = word_tag[every_word][tag] / sum(word_tag[every_word].values())

                if tmp_prob > current_prob:
                    current_prob = tmp_prob
                    tag_to_append = tag

            final_list.append(every_word + "/" + tag_to_append)
            prev_tag = tag_to_append
            continue


        for tag, tag_value in word_tag[every_word].items():
            tmp_prob = (word_tag[every_word][tag] / sum(word_tag[every_word].values())) \
                       * (tag_his[prev_tag][tag] / sum(tag_his[prev_tag].values()))
            if tmp_prob > current_prob:
                current_prob = tmp_prob
                tag_to_append = tag

            final_list.append(every_word + "/" + tag_to_append)
            prev_tag = tag_to_append





        #this will be done at the end of every loop
        # final_list.append(every_word + "/" + tag_to_append)
        # prev_tag = tag_to_append

if __name__ == "__main__":
    main()


