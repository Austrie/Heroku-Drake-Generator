import pickle
import ast
import os.path
from os import path
import json

import resource
import sys

print resource.getrlimit(resource.RLIMIT_STACK)
print sys.getrecursionlimit()

max_rec = 0x100000

# # May segfault without this line. 0x100 is a guess at the size of each stack frame.
# resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
sys.setrecursionlimit(max_rec)


from hashtable import HashTable
from linkedlist import LinkedList
from random import randint

def load_words():
    if path.exists('words.pkl'):
        loaded_words = pickle.load(open('words.pkl', 'rb'))
    else:
        loaded_words = open("clean_words2.txt", "r").read().splitlines()
        pickle.dump(loaded_words, open('words.pkl', 'wb'))
    return loaded_words

words = load_words()

def getRandomWord(table = None, lastWord = None):
    if table is None:
        table = setupFirstOrder()

    lis = []
    if lastWord is None or lastWord == ".":
        lis = table.get("[")
    else:
        lis = table.get(lastWord)

    new_word = lastWord
    # We do this while-loop to prevent repeating words
    while new_word == lastWord:
        total = 0
        line = randint(0, lis[0] - 1)
        for word, amount in lis[1].items():
            total += amount
            if (total > line):
                if "]" in word:
                    new_word = "."
                    break
                new_word = word
                break
    return new_word

def load_table(order):
    if path.exists(order + '_order_table.txt'):
        return ast.literal_eval(open(order + '_order_table.pkl', 'r'))
    return None


def save_table(order, table):
    # We have to save as json since Pickle is reaching a recursion limit
    with open(order + '_order_table.txt', 'w') as file_handle:
        file_handle.write(str(dictionary))

def setupFirstOrder():
    table = load_table("first")
    if table is not None:
        return table
    table = HashTable(len(words) + 1)
    for i in range(0, len(words)):
        # Our initial implementation of Hashtable is so limited (no resize/load)
        # That I might as well use a LinkedList for the innerTable, Because
        # Our HashTable with an initial size of 1, is essentially a LinkedList
        # The only way to improve this is recreating the HashTable with size + 1
        # with each new word for a word

        # I could use the table.get surrounded by a try-except instead of contains
        begin = False
        end = False
        word = words[i]

        # If the word starts a sentence
        if "BEGINSENT" in word:
            begin = True
            word = word[(len("BEGINSENT")):]

        # If the word ends a sentence
        if "ENDSENT" in word:
            end = True
            word = word[:-(len("ENDSENT"))]

        # We have to remove any beginning or ending flags for the next word (word2)
        # in order to add the next word (word2) to the current word's innertable
        word2 = ""

        # We have to check that we're not at the end of the for-loop
        if (i + 1 != len(words)):
            word2 = words[i + 1]
            word2.replace("\n", "")
            # If the next word starts a sentence,
            if "BEGINSENT" in word2:
                word2 = word2[(len("BEGINSENT")):]

            # If the next word ends a sentence
            if "ENDSENT" in word2:
                word2 = word2[:-(len("ENDSENT"))]

        # I could also do a check to see if the word is an ending word, then
        # proceed to add only the ending token. However, I decided to add
        # both the next word and possibly the ending token because lyrics are
        # are really short.
        # If the table contains the word already
        if table.contains(word):
            lis = table.get(word)
            # Increment the total number of tokens that can come after this word
            lis[0] += 1
            # This variable represent the total number of times the word that comes
            # after this word in the for-loop appears
            tup = 0

            # if the the current word isn't the end of the for-loop, meaning
            # that it has a word coming after the current one
            # (The word at the end of the loop is automatically an ending word)
            if i + 1 != len(words):
                # Try to find the word, if the word isnt in there, then the
                # get method throws an error so catch it
                # We want to set the "tup" variable to how many times the word
                # has already appeared
                try:
                    tup = lis[1].get(word2)
                except:
                    tup = 0
                # Then we reset the next word but increment the number of times
                # the next word appears after the current word
                lis[1].set(word2, tup + 1)

        # If the word is new to the table
        else:
            lis = [None, None]
            lis[0] = 1
            lis[1] = HashTable(1)
            lis[1].set(word2, 1)
            table.set(word, lis)


        # Technically we could've used the same character for both beginning
        # and ending since they wont live in the same space (table vs innertable)

        # If the word is an end of a sentence (or if it's at the end of the
        # for-loop then it's automatically the end of the sentence)
        # then we need to account for how likely is it to end the sentence
        # It's stored inside the innertable
        if end:
            lis = table.get(word)
            lis[0] += 1
            tup = 0
            try:
                tup = lis[1].get("]")
            except:
                # Word hasn't ended a sentence before
                tup = 0
            lis[1].set("]", tup + 1)

        # If the word is an beginning of a sentence
        # then we need to account for how likely is it to start a sentence
        # We use '[' as the character to signify starting a new sentence
        # It's stored in a table of it's own (not an innertable)
        if begin:
            # Not the first sentence starter
            if table.contains("["):
                lis = table.get("[")
                lis[0] += 1
                tup = 0
                try:
                    tup = lis[1].get(word)
                except:
                    # Word hasn't started a sentence before
                    tup = 0
                lis[1].set(word, tup + 1)

            # This is the first sentence starter (Happens at beginning of for-loop)
            else:
                lis = [None, None]
                lis[0] = 1
                lis[1] = HashTable(1)
                lis[1].set(word, 1)
                table.set("[", lis)

    pickle.dump(table, open('first_order_table.pkl', 'wb'))
    return table

def setupSecondOrder():
    table = load_table("second")
    if table is not None:
        return table
    table = HashTable(len(words) + 1)
    for i in range(0, len(words) - 3):
        # Our initial implementation of Hashtable is so limited (no resize/load)
        # That I might as well use a LinkedList for the innerTable, Because
        # Our HashTable with an initial size of 1, is essentially a LinkedList
        # The only way to improve this is recreating the HashTable with size + 1
        # with each new word for a word

        # I could use the table.get surrounded by a try-except instead of contains
        begin = False
        end = False
        twoWord = ""
        word = words[i]

        # If the word starts a sentence
        if "BEGINSENT" in word:
            begin = True
            word = word[(len("BEGINSENT")):]

        # If the word ends a sentence
        if "ENDSENT" in word:
            word = word[:-(len("ENDSENT"))]

        # We have to remove any beginning or ending flags for the next word (word2)
        # in order to add the next word (word2) to the current word's innertable
        word2 = ""

        # We have to check that we're not at the end of the for-loop
        # if (i + 1 != len(words)):
        word2 = words[i + 1]
        # If the next word starts a sentence,
        if "BEGINSENT" in word2:
            word2 = word2[(len("BEGINSENT")):]

        # If the next word ends a sentence
        if "ENDSENT" in word2:
            word2 = word2[:-(len("ENDSENT"))]


        twoWord = word + " " + word2

        twoWord2 = ""
        word3 = words[i + 2]

        # If the word starts a sentence
        if "BEGINSENT" in word3:
            word3 = word3[(len("BEGINSENT")):]

        # If the word ends a sentence
        if "ENDSENT" in word3:
            word3 = word3[:-(len("ENDSENT"))]

        # We have to remove any beginning or ending flags for the next word (word2)
        # in order to add the next word (word2) to the current word's innertable
        word4 = ""

        # We have to check that we're not at the end of the for-loop
        # if (i + 1 != len(words)):
        word4 = words[i + 3]
        # If the next word starts a sentence,
        if "BEGINSENT" in word4:
            word4 = word4[(len("BEGINSENT")):]

        # If the next word ends a sentence
        if "ENDSENT" in word4:
            end = True
            word4 = word4[:-(len("ENDSENT"))]

        twoWord2 = word3 + " " + word4

        # I could also do a check to see if the word is an ending word, then
        # proceed to add only the ending token. However, I decided to add
        # both the next word and possibly the ending token because lyrics are
        # are really short.
        # If the table contains the word already
        if table.contains(twoWord):
            lis = table.get(twoWord)
            # Increment the total number of tokens that can come after this word
            lis[0] += 1
            # This variable represent the total number of times the word that comes
            # after this word in the for-loop appears
            tup = 0

            # if the the current word isn't the end of the for-loop, meaning
            # that it has a word coming after the current one
            # (The word at the end of the loop is automatically an ending word)
            # if i + 1 != len(words):
                # Try to find the word, if the word isnt in there, then the
                # get method throws an error so catch it
                # We want to set the "tup" variable to how many times the word
                # has already appeared
            try:
                tup = lis[1].get(twoWord2)
            except:
                tup = 0
            # Then we reset the next word but increment the number of times
            # the next word appears after the current word
            lis[1].set(twoWord2, tup + 1)

        # If the word is new to the table
        else:
            lis = [None, None]
            lis[0] = 1
            lis[1] = HashTable(1)
            lis[1].set(twoWord2, 1)
            table.set(twoWord, lis)


        # Technically we could've used the same character for both beginning
        # and ending since they wont live in the same space (table vs innertable)

        # If the word is an end of a sentence (or if it's at the end of the
        # for-loop then it's automatically the end of the sentence)
        # then we need to account for how likely is it to end the sentence
        # It's stored inside the innertable
        if end:
            try:
                lis = table.get(twoWord2)
            except:
                lis = [None, None]
                lis[0] = 0
                lis[1] = HashTable(1)
                table.set(twoWord2, lis)
            lis[0] += 1
            tup = 0
            try:
                tup = lis[1].get("]")
            except:
                # Word hasn't ended a sentence before
                tup = 0
            lis[1].set("]", tup + 1)

        # If the word is an beginning of a sentence
        # then we need to account for how likely is it to start a sentence
        # We use '[' as the character to signify starting a new sentence
        # It's stored in a table of it's own (not an innertable)
        if begin:
            # Not the first sentence starter
            if table.contains("["):
                lis = table.get("[")
                lis[0] += 1
                tup = 0
                try:
                    tup = lis[1].get(twoWord)
                except:
                    # Word hasn't started a sentence before
                    tup = 0
                lis[1].set(twoWord, tup + 1)

            # This is the first sentence starter (Happens at beginning of for-loop)
            else:
                lis = [None, None]
                lis[0] = 1
                lis[1] = HashTable(1)
                lis[1].set(twoWord, 1)
                table.set("[", lis)

    pickle.dump(table, open('second_order_table.pkl', 'wb'))
    return table

def generate(first_order = True, num_words=140, table=None):
    if table is None:
        table = setupFirstOrder()
    sentence = "Drake Generator says: "
    if first_order:
        lastWord = getRandomWord(table)
        sentence += lastWord
        for i in range(0, num_words):
            lastWord = getRandomWord(table, lastWord)
            if lastWord is not ".":
                sentence += " " + str(lastWord)
            else:
                sentence += str(lastWord)
    else:
        lastWord = getRandomWord(table)
        sentence += lastWord
        for i in range(0, num_words):
            lastWord = getRandomWord(table, lastWord)
            if lastWord is not ".":
                sentence += " " + str(lastWord)
            else:
                sentence += str(lastWord)
    return sentence

if __name__ == '__main__':
    print generate(1)
