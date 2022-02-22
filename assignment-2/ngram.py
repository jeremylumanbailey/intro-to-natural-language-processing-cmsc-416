'''
1) Describe the problem: Create a program that will produce any number of randomly generated sentences based on any number of text documents
(such as books) using probability. For example: if we told the program to generate a sentence based on 3 books about cats,
there would be a high probability that it could produce the sentence "i have a pet cat" or if we gave it 3 books about
dogs, there would be a high probability that it could produce the sentence "i have a pet dog" instead (note that this
does not guarantee these sentences, just that there would be a high probability it would produce them). It would use
something called "n"-grams ("n" is a number more than or equal to 1 that would be decided on starting the program)
to calculate these probabilties. So if n = 3, we would call it a trigram, and calculate the probabilties based on that.

2) Give actual examples: Ensure you have python3 installed on your system.
On linux you would run it by typing something like this into
the terminal: "python3 ngram.py 3 5 crime.txt war.txt anna.txt" python3 being the tool, ngram.py being the program,
3 being n (making it a trigram), 5 being the number of sentences you want the program to output, and "crime.txt war.txt
anna.txt" being the text files the program will be extracting text from. This would result in an output along the
lines of:

1: and now moscow memories--and he again obeyed the command of an old familiar acquaintance we are distressing him that it was disagreeable and unnatural state.
2: was just what he was silent.
3: at the windows.
4: you must find out whether anyone had come upon some expense on our helplessness dounia observed irritably.
5: she is going to begin.


3) Describe algorithm: The first step is to take in arguments for input from the user. Second step is to create the
grams based on the user's input. In the create ngram function the input is sanitized, tokenized, zipped and then joined
to be returned as list. If the n is one then the function to generate based on a unigram is called. And the probability
is calculated using the overall frequency of each word. If the n is greater than one, then a frequency of histories is
stored using the denominator and numerator functions that product dictionary of dictionaries. The generate sentences
is then called with both dictionary of dictionaries passed in that pass that to another function that will create the
actually sentences m number of times.

Jeremy Bailey V00880079

'''

import sys
import re
import random


'''
This function creates the actual ngram by returning an iterable zip object that can be
assigned to a list.
'''
def create_ngram(string_input, n):

    # Cleaning input
    string_input = string_input.lower()
    string_input = re.sub(r"['\"“”‘’„”«»,]", ' ', string_input)
    string_input = re.sub(r"\n", " ", string_input)

    start_tag = ""
    for i in range(n - 1):
        start_tag = start_tag + " <START> "

    string_input = start_tag + string_input
    start_tag = " <END> " + start_tag

    string_input = string_input.replace(".", start_tag)
    string_input = string_input.replace("...", start_tag)
    string_input = string_input.replace("....", start_tag)
    string_input = string_input.replace("!", start_tag)
    string_input = string_input.replace("?", start_tag)


    string_input = re.sub(r"  ", ' ', string_input)

    # Create tokens
    tokenized = [token for token in string_input.split(" ") if token != ""]
    raw_tokens = [tokenized[i:] for i in range(0, n)]

    ngrams = zip(*raw_tokens)
    # Have to use zip function to make it an n-gram. Otherwise would have to hardcode "n" in raw_tokens
    return [" ".join(ngram) for ngram in ngrams]


# Simple function used to cast a list to a string
def listToString(s):
    str1 = " "
    return str1.join(s)

# Function used to created the frequency tables used in the numerator for the probability
def numerator(grams, n):
    my_dict = {}

    for i in range(0, len(grams)):
        w = str(grams[i].split()[n - 1])
        h = listToString(grams[i].split()[:(n - 1)])
        if h in my_dict:  # If history exists and history has this key
            if w in my_dict[h]:
                my_dict[h][w] += 1
            else:
                my_dict[h][w] = {}
                my_dict[h][w] = 1
        else:
            my_dict[h] = {}  # dict[h] =  { w : 1} # If history doesn't exist, init history, add key, set to one
            my_dict[h][w] = {}
            my_dict[h][w] = 1
    return my_dict

# Function used to created the frequency tables used in the denominator for the probability
def denominator(grams, n):
    my_dict = {}

    for i in range(0, len(grams)):
        w = str(grams[i].split()[n - 1])
        h = listToString(grams[i].split()[:(n - 1)])
        if h in my_dict:  # If history exists and history has this key
            my_dict[h] += 1
        else:
            my_dict[h] = {}  # dict[h] =  { w : 1} # If history doesn't exist, init history, add key, set to one
            my_dict[h] = 1
    return my_dict

# Function used to create the actual sentences. It calculates the probability on the fly and picks a words randomly.
# It uses an array to pop off the values and then appends those values
# onto the sentence until it ends an <END> tag denoting to finish the sentence.
def generate_sentence(numerator_freq, freq_denominator, n):
    sentence = ""
    history = ""
    ngram_array = []

    for n in range(0, (n - 1)):
        ngram_array.append("<START>")

    while "<END>" not in ngram_array:
        history = " ".join(ngram_array)
        word_list = numerator_freq[history]
        denom = freq_denominator[history]
        sum = 0
        ran_num = random.uniform(0, 1)
        for word in word_list:
            probabilitiy = word_list[word] / denom
            sum = sum + probabilitiy
            if ran_num < sum:
                sentence = sentence + ngram_array.pop(0) + " "
                ngram_array.append(word)

                if "<END>" in ngram_array:
                    sentence += " ".join(ngram_array)
                break

    sentence = sentence.replace("<START>", " ")
    sentence = sentence.replace(" <END>", ".")

    return sentence.lstrip()

# Function that is used to call the generate sentence function to create the disired number of sentences
def create_m_sentences(number_of_sentences, numerator_freq, freq_denominator, n):
    for x in range(0, number_of_sentences):
        sentence = generate_sentence(numerator_freq, freq_denominator, n)
        print(str(x+1) + ": " + sentence)

# Function that is used to generate sentences specifically for unigrams
def create_unigram_sentence(sum_of_all_words, frequency_of_each_word):
    sentence = ""
    history = ""
    ngram_array = [" "]
    denom = sum_of_all_words

    while "<END>" not in ngram_array:
        history = " ".join(ngram_array)

        my_sum = 0
        ran_num = random.uniform(0, 1)
        for word in frequency_of_each_word:
            probabilitiy = frequency_of_each_word[word] / denom
            my_sum = my_sum + probabilitiy
            if ran_num < my_sum:
                sentence = sentence + ngram_array.pop(0) + " "
                ngram_array.append(word)

                if "<END>" in ngram_array:
                    sentence += " ".join(ngram_array)
                break
    sentence = sentence.replace(" <END>", ".")

    return sentence.lstrip()


def main():

    print()

    # This is for arguments
    n = int(sys.argv[1])
    m = int(sys.argv[2])

    full_text = ""
    for text_file in sys.argv[3:]:
        with open(text_file, "r", encoding="utf-8") as file:
            data = file.read()
            full_text += data

    if n == 1:

        grams = create_ngram(full_text, n)
        frequency_of_each_word = {}
        for each in grams:
            if each in frequency_of_each_word:
                frequency_of_each_word[each] += 1
                continue
            frequency_of_each_word[each] = 1

        sum_of_all_words = sum(frequency_of_each_word.values()) - frequency_of_each_word["<END>"]

        for m in range(0, m):
            sentence = create_unigram_sentence(sum_of_all_words, frequency_of_each_word)
            print(str(m+1) + ": " + sentence)

    elif n > 1:
        grams = create_ngram(full_text, n)

        numerator_freq = numerator(grams, n)

        freq_denominator = denominator(grams, n)

        create_m_sentences(m, numerator_freq, freq_denominator, n)


if __name__ == "__main__":
    main()
    print()
    print("Jeremy Bailey V00880079")
