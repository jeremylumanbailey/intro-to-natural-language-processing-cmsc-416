'''

Name: Jeremy Bailey     Date: March 8th 2020

1)  In natural language processing, we use a tool called Part Of Speech (POS) to reduce words to their root forms. POS tagging is a way in linguistics of marking up a word in a text as corresponding to a
particular part of speech. So for example, if we had the word apple, we would tag it with the tag NN for noun, singular or mass.

'''

import sys
import re


# Cleans that brackets from the data, as well as other sanitizing
def clean_brackets(dirty_string):
    clean_string = re.sub(r"[\[\]]", '', dirty_string)
    cleaner_string = re.sub(r'|\S+', '', clean_string)
    return cleaner_string.replace("\/", "")


# Main function where I run most of the code
def main():

    # Load the training text from pos-train.txt
    train_text = ""
    with open(sys.argv[1], "r") as train_arg:
        data = train_arg.read()
        train_text += data

    # Load the testing text from pos-te
    test_text = ""
    with open(sys.argv[2], "r") as test_arg:
        data = test_arg.read()
        test_text += data

    # Cleaning training text and load into array
    train_text_list = clean_brackets(train_text).split()
    # Setup variables to iterate
    word_tag = {}
    tag_his = {}
    prev_tag = None

    # Interate through every word/tag pair
    for every_pair in train_text_list:

        # Split the word/tag pairs
        tmp_arr = re.split('\/', every_pair)
        word = tmp_arr[0]
        tag = tmp_arr[1]

        # Fill dictionary with word/tag frequencies
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

        # Fill dictionary with prev_tag/tag frequencies
        # will not run for the very first word since the tag will have no history
        if prev_tag in tag_his:
            if tag in tag_his[prev_tag]:
                tag_his[prev_tag][tag] += 1
            else:
                tag_his[prev_tag] = {}
                tag_his[prev_tag][tag] = 1
        elif prev_tag:
            tag_his[prev_tag] = {}
            tag_his[prev_tag][tag] = {}
            tag_his[prev_tag][tag] = 1

        # we now have a tag history, and can start using it to fill our prev_tag/tag dictionary
        prev_tag = tag
    # end of for loop


    # Start parsing test data
    test_list = clean_brackets(test_text).split()
    final_list = []
    prev_tag = None

    for every_word in test_list:

        # If we find a word that we have never seen before, set it's tag to NN by default
        if every_word not in word_tag:
            final_list.append(every_word + "/" + "NN")
            prev_tag = "NN"
            continue

        tmp_prob = 0
        current_prob = 0

        # First word without prev_tag edge case
        if prev_tag is None:
            for tag, tag_freq in word_tag[every_word].items():

                # Find tag that maximizes P(tag_i|word_i)
                tmp_prob = word_tag[every_word][tag] / sum(word_tag[every_word].values())
                if tmp_prob > current_prob:
                    current_prob = tmp_prob
                    tag_to_append = tag

            # Assign tag to word
            final_list.append(every_word + "/" + tag_to_append)
            prev_tag = tag_to_append
            continue

        # Regular way we would find tag to assign to word
        for tag, tag_freq in word_tag[every_word].items():

            # Edge case if we had not seen the prev_tag before in our training data
            if tag not in tag_his[prev_tag]:
                continue

            # Find tag to assign that maximizes P(tag|word)*P(tag|previous tag)
            tmp_prob = (word_tag[every_word][tag] / sum(word_tag[every_word].values())) * (tag_his[prev_tag][tag] / sum(tag_his[prev_tag].values()))
            if tmp_prob > current_prob:
                current_prob = tmp_prob
                tag_to_append = tag
        # Finally assign tag to word
        final_list.append(every_word + "/" + tag_to_append)
        prev_tag = tag_to_append

    # Write results to pos-test-with-tags.txt file
    with open("pos-test-with-tags.txt", "w") as filehandle:
        for item in final_list:
            filehandle.write('%s\n' % item)


if __name__ == "__main__":
    main()
