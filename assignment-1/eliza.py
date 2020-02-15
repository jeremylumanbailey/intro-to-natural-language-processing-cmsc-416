# Name: Jeremy Bailey Date: 1/30/20


# 1) The problem we are trying to solve is that we want to create a program that can imitate a therapist to help
# people talk about their problems in a rogerian manner.

# 2) From command prompt run: python3 eliza.property
# output: [eliza] HI, I'M A PSYCHOTHERAPIST. WHAT IS YOUR NAME?
# input (use keyboard to type): my name is Jeremy
# output: [eliza] HI JEREMY. HOW CAN I HELP YOU TODAY?
# input: i am feeling good
# output: JEREMY, WHY DO YOU THINK THAT YOU ARE FEELING GOOD?
# input: i am not sure
# output: JEREMY, WHY DO YOU THINK THAT YOU ARE NOT SURE?
# input: goodbye
# output: it was nice talking with you.

# 3) My eliza uses a main() method that takes in input and passes that input to find_name functiong
# in order to find the name of the user. After the name has been found, main goes into a loop, checking
# the input for keywords. If the input is "goodbye" the program will exit. Otherwise, it will pass it to different
# functions, and if those functions find keywords then they will return a response to the user. If
# they do not find a keyword, then they will return None and main() will try a different function
# until it finds one that works, falling back to a defualt function if no other function is found.
# if one of the functions returns something other than None, main will use that function to reply
# to the user and it will continue the loop.




import re
import random
global last_said


# Used to swap between pronouns
pronouns = {
    "AM": "ARE",
    "WAS": "WERE",
    "I": "YOU",
    "I'D": "YOU WOULD",
    "I'VE": "YOU HAVE",
    "I'LL": "YOU WILL",
    "MY": "YOUR",
    "ARE": "AM",
    "YOU'VE": "I HAVE",
    "YOU'LL": "I WILL",
    "YOUR": "MY",
    "YOURS": "MINE",
    "YOU": "ME",
    "ME": "YOU"
}


remove_contraction = {
    "I'M": "I AM",
    "WASN'T": "WAS NOT",
    "I": "YOU",
    "I'D": "I WOULD",
    "I'VE": "I HAVE",
    "I'LL": "I WILL",
    "ARE": "AM",
    "YOU'VE": "YOU HAVE",
    "ISN'T": "IS IT NOT"
}


# This will be fired if the user asks a questions indicated by a "?" in the users input
def handle_their_questions(user_input, name):
    if re.search(r'\?', user_input):
        x = random.randint(1, 2)
        if x == 1:
            return "YOU RAISE A GOOD QUESTION THERE. BUT LET'S GET BACK TO TALKING ABOUT YOU."
        elif x == 2:
            return "IF YOU TRIED ASKING THAT QUESTION TO YOURSELF, HOW WOULD YOU ANSWER?"
    return None


# This regex checks if they are making a hard statement "yes I am afraid" looking for words such as yes, no or agree
def confirm(user_input, name):
    x = random.randint(1, 3)
    if re.search(r"\s(YES|AGREE|OK|OKAY|NO|DISAGREE)\s", user_input):
        if x == 1:
            return "WOULD YOU BE WILLING TO RECONSIDER?"
        if x == 2:
            return "WHAT MAKES YOU SO CERTAIN?"
        if x == 3:
            return "ARE YOU SURE ABOUT THAT " + name + "?"
        return None


# This function finds their name by first checking if it is at least 2 characters long and then
# parses through their introduction to check for contractions such as "I'm". It also used the group() regex
# to detect their name right after IS or AM this would catch things such as "I am John" and "My name is Jeremy"
def find_name(user_input):
    if len(user_input) < 2:
        print("PLEASE GIVE ME YOUR ACTUAL NAME.")
        return None
    response = user_input
    for each_word in user_input.split():
        if remove_contraction.get(each_word):
            predicate = True
            pattern = re.compile(r'\s?{}\s'.format(each_word))
            response = pattern.sub(" " + r'{}'.format(remove_contraction.get(each_word)) + " ", response)

    m = re.search(r'IS', response)
    if m and re.search(r'(?<=\bIS\s)(\w+)', response):
        found = re.search(r'(?<=\bIS\s)(\w+)', response)
        name = found.group(1)
        return name
    m = re.search(r'AM', response)
    if m and re.search(r'(?<=\bAM\s)(\w+)', response):
        found = re.search(r'(?<=\bAM\s)(\w+)', response)
        name = found.group(1)
        return name
    return user_input


# This checks if they are using a "!" which implies that they are angry or yelling and tries to calm them down.
def calm_them_down(user_input, name):
    x = '"' + user_input + '"'
    if re.search(r'\!', user_input):
        return name + ", I KNOW THIS IS DIFFICULT, BUT YELLING " + x + " ISN'T GOING TO SOLVE ANYTHING."
    return None


# This searches for desires such as keywords like crave, desire or wish.
def desire(user_input, users_name):
    predicate = False
    if re.search(r'\s(CRAV)', user_input):
        return "WHY DON'T YOU TELL ME MORE ABOUT YOUR CRAVINGS."
    if re.search(r'\s(DESIR|WISH)', user_input):
        tmp = re.search(r'\s(DESIR|WISH)', user_input)
        return "HMMM, WHERE DO YOU THINK THESE {} STEM FROM?".format(tmp.group(1) + "ES")
    return None


# Creates a question from what they say. The for loop converts all of the pronouns and then rearranges
# their statement into a question.
# I attempted to use regex .sub() method to construct the response, but it would cause input such as "i hate you" to
# become "Me hate you" so I switched to a string builder. This is what the code I attempted before looked like:
# pattern = re.compile(r'\s?{}\s'.format(each_word))
# response = pattern.sub("" + r'{} '.format(pronouns.get(each_word)) + "", response)
# print(response)
def transform_into_question(user_input, users_name):
    predicate = False
    response = user_input
    string_builder = ""
    for each_word in user_input.split():
        if pronouns.get(each_word):
            predicate = True
            string_builder = string_builder + " " + pronouns.get(each_word)
        else:
            string_builder = string_builder + " " + each_word
    if predicate:
        x = random.randint(1, 1)
        if x == 1:
            return "{}, WHY DO YOU THINK THAT{}?".format(users_name, string_builder)
    return None


# Default response if nothing else catches what they say
def generic_responses(user_name):
    x = random.randint(1, 9)
    if x == 1:
        return "I'M SORRY, I DON'T QUITE UNDERSTAND."
    if x == 2:
        return "COULD YOU REPHRASE THAT? I'M NOT SURE I UNDERSTAND."
    if x == 3:
        return "I THINK IT'S TIME WE MOVED ON TO SOMETHING ELSE. WHAT ELSE IS ON YOUR MIND?"
    if x == 4:
        return "YOU CAN'T CONTROL YOUR FEELINGS, ONLY OBSERVE THEM."
    if x == 5:
        return "TELL ME MORE..."
    if x == 6:
        return "COME, COME, ELUCIDATE YOUR THOUGHTS."
    if x == 7:
        return "GO ON..."
    if x == 8:
        return "CAN YOU ELABORATE ON THAT?"
    if x == 9:
        return "HOW DOES THAT MAKE YOU FEEL?"


# Regex searches if user is apologizing and responds.
def apologies(user_input, name):
    x = random.randint(1, 2)
    if re.search(r'SORRY', user_input):
        if x == 1:
            return "THERE IS NO NEED TO APOLOGIZE."
        elif x == 2:
            return "IT'S OKAY."


# This catches other miscellaneous words and responds accordingly
def other_words_to_catch(user_input):
    if re.search(r'(.*?)\b(BECAUSE|CAUSE)\b(.*?)', user_input):
        return "THAT IS A FAIR REASON. WHAT ELSE?"
    if re.search(r'(.*?)\b(SAD|DEPRESS|MAD|HAPPY|ANGRY)(ED)?\b(.*?)', user_input):
        tmp = re.search(r'(.*?)\b(SAD|DEPRESSED|MAD|HAPPY|ANGRY)(ED)?\b(.*?)', user_input)
        return "WHY DO YOU FEEL {}?".format(tmp.group(2))
    return None


# Decides what function to call to deal with user's input
def handle_input(user_input, users_name):
    # Handles if user enters gibberish (just a single letter)
    if len(users_name) < 2:
        return "I CAN'T HELP YOU IF YOU WON'T SAY MORE."
    elif other_words_to_catch(user_input):
        return other_words_to_catch(user_input)
    elif confirm(user_input, users_name):
        return confirm(user_input, users_name)
    elif apologies(user_input, users_name):
        return apologies(user_input, users_name)
    elif desire(user_input, users_name):
        return desire(user_input, users_name)
    elif transform_into_question(user_input, users_name):
        return transform_into_question(user_input, users_name)

    return generic_responses(users_name)


# This will return a response if the user types in the same thing multiple times in a row
def repeating(name):
    x = random.randint(1, 3)
    if x == 1:
        return "YOU ALREADY SAID THAT."
    elif x == 2:
        return "DO YOU EXPECT A DIFFERENT ANSWER BY REPEATING YOURSELF?"
    elif x == 3:
        return "WHY DID YOU REPEAT YOURSELF?"
    elif x == 4:
        return "ARE YOU OKAY " + name + "? YOU KEEP REPEATING YOURSELF."


# main function that loops through and chooses a function to use to respond depending on what the user gives
def main():
    last_said = ""
    print("[eliza] HI, I'M A PSYCHOTHERAPIST. WHAT IS YOUR NAME?")
    while True:
        introduction = input().upper()
        if find_name(introduction):
            name = find_name(introduction)
            print("[eliza] HI {}. HOW CAN I HELP YOU TODAY?".format(name))
            break
    first_loop = True
    while True:
        user_input = input().upper()
        if user_input == "GOODBYE":
            print("IT WAS NICE TALKING WITH YOU.")
            break
        if user_input == last_said:
            print(repeating(name))
            continue
        elif handle_their_questions(user_input, name):
            print(handle_their_questions(user_input, name))
        elif calm_them_down(user_input, name):
            print(calm_them_down(user_input, name))
        else:
            user_input = user_input.rstrip(",.'")
            print(handle_input(user_input, name))
        last_said = user_input


if __name__ == "__main__":
    main()
