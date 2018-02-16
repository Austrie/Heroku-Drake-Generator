from hashtable import HashTable
from linkedlist import LinkedList
from random import randint

words = open("clean_words2.txt", "r").read().splitlines()

def getRandomWord(table = None, lastWord = None):
    if table is None:
        table = setup()

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

def setup():
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
            lis[0] += 1;
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

    return table

def setupSecondOrder():
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
            lis[0] += 1;
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

    return table

if __name__ == '__main__':
    table1 = setupSecondOrder()
    lastWord = getRandomWord(table1)
    sentence = "First Order: " + lastWord
    for i in range(0, 140):
        lastWord = getRandomWord(table1, lastWord)
        if lastWord is not ".":
            sentence += " " + str(lastWord)
        else:
            sentence += str(lastWord)
    print sentence

    table2 = setupSecondOrder()
    lastWord = getRandomWord(table2)
    sentence = "Second Order: " + lastWord
    for i in range(0, 140):
        lastWord = getRandomWord(table2, lastWord)
        if lastWord is not ".":
            sentence += " " + str(lastWord)
        else:
            sentence += str(lastWord)
    print sentence
