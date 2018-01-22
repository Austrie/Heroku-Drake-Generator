import sys
import random
words = sys.argv

og_sentence = "one fish two fish red fish blue fish"

""" List of lists """
def list_of_lists(sentence = og_sentence):
    # sentence = " ".join(words)''
    # fish one fish ...
    arr_sentence = sentence.split()
    histogram = []

    for word in arr_sentence:
        # [["one", 1], ["fish", 4], ...]
        # i = 0
        found = False
        for i in range(0, len(histogram) - 1):
            if histogram[i][0] == word:
                histogram[i][1] += 1
                found = True
                break
        if found == False:
            histogram.append([word, 1])
    return histogram

''' List of tuples '''
def list_of_tuples(sentence = og_sentence):
    # sentence = " ".join(words)''
    # fish one fish ...
    arr_sentence = sentence.split()
    histogram = []

    for word in arr_sentence:
        # [("one", 1), ("fish", 4), ...]
        # i = 0
        found = False
        for i in range(0, len(histogram) - 1):
            if histogram[i][0] == word:
                histogram[i] = (word, histogram[i][1] + 1)
                found = True
                break
        if found == False:
            histogram.append((word, 1))
    return histogram

''' Dictionary '''
def dictionary(sentence = og_sentence):
    # {"one": 1, "fish": 4}
    arr_sentence = sentence.split()
    histogram = {}
    for word in arr_sentence:
        if word in histogram:
            histogram[word] += 1
        else:
            histogram[word] = 1

    return histogram


''' Inverted tuple '''
def inverted_tuple(sentence = og_sentence):
    # The desired outcome: [(1, ['one', 'two', 'red', 'blue']), (4, ['fish'])]
    arr_sentence = sentence.split()
    histogram = []

    # We use each word/item in sentence array to update the histogram
    for word in arr_sentence:
        # Number of words is set to 1 initially because at minimum it should
        # appear in the tuple for the words that appear once. This variable will
        # be updated if the word is found in a different tuple
        number_of_times = 1

        # For when the histogram is just created
        if len(histogram) == 0:
            histogram.append((number_of_times, [word]))

        # For when there is only one tuple in the histogram
        elif len(histogram) == 1:

            # If the word is already in the histogram
            if word in histogram[0][1]:
                number_of_times = histogram[0][0] + 1
                updated_old_list = histogram[0][1]
                updated_old_list.remove(word)

                # If this is true, then that means only one type of word is in
                # the histogram, which is the one we're adding again
                if len(updated_old_list) == 0:
                    histogram[0] = ((number_of_times, [word]))

                # If this is true, then we must add a new tuple
                # since there are other words in the existing tuple and we dont
                # want to delete them
                else:
                    histogram[0] = (histogram[0][0], updated_old_list)
                    histogram.append((number_of_times, [word]))

            # If this is true then the word is new, and we simple add it to
            # the correct tuple
            else:
                # If this is true then the tuple in the histogram is for single
                # appearance words
                if histogram[0][0] == 1:
                    updated_old_list = histogram[0][1]
                    updated_old_list.append(word)
                    histogram[0] = (number_of_times, updated_old_list)

                # If this is true then the tuple that's already there isn't for
                # new words
                else:
                    histogram.append((number_of_times, [word]))

        else:
            # Attempt to remove the word from the old list and get the number of
            # times it appears
            for i in range(0, len(histogram)):

                # If this is true then that means the word is not new
                # so get how many times it appears and put it to the appropriate
                # tuple
                if word in histogram[i][1]:
                    number_of_times = histogram[i][0] + 1
                    updated_old_list = histogram[i][1]
                    updated_old_list.remove(word)

                    # If this is true then that mean the tuple only had that
                    # word and since we're moving the word, then we should just
                    # remove the tuple
                    if len(updated_old_list) == 0:
                        histogram.remove(histogram[i])

                    # If this is true then that means the tuple had other words
                    # so we should not remove the whole tuple, but instead
                    # update the tuple with a list of words that does not contain
                    # the removed words
                    else:
                        histogram[i] = (histogram[i][0], updated_old_list)
                    break

            # This represents if the word was added to the appropriate tuple
            done = False
            # Add the word to the appropriate tuple based on the number of times
            # it appears
            for i in range(0, len(histogram) - 1):
                if number_of_times == histogram[i][0]:
                    updated_old_list = histogram[i][1]
                    updated_old_list.append(word)
                    histogram[i] = (number_of_times, updated_old_list)
                    done = True
                    break

            # If no appropriate tuple was found then we must create it and add it
            if done == False:
                histogram.append((number_of_times, [word]))

    return histogram

def random_word_histogram_with_word_frequency_factor(num_of_words = 1, sentence = og_sentence):
    str_random_sentence = ""
    if type(sentence) == list:
        while num_of_words > 0:
            index = random.randint(0, len(sentence) - 1)
            str_random_sentence += sentence[index] + " "
            num_of_words -= 1
        return str_random_sentence
    elif type(sentence) == str:
        sentence2 = sentence.split(" ")
        while num_of_words > 0:
            index = random.randint(0, len(sentence2) - 1)
            str_random_sentence += sentence2[index] + " "
            num_of_words -= 1
    return str_random_sentence
    # if (len(histogram_input) == 0):
    #     return
    # elif (len(histogram_input) == 1):
    #     return
    # else:
    #     for i in range(0, len(histogram_input)):
    #
    #     index = random.randint(0, len(histogram_input) - 1)
    #     if type(histogram_input) == list:
    #         list_keys = histogram_input.keys()
    #         print histogram_input[list_keys[index]]
    #
    #     elif type(histogram_input) == list:
    #         print "false"
    #         print "bye"

# def frequency(histogram_input = histogram.dictionary(str_sentence)):
#     list_keys = histogram_input.keys()


if __name__ == "__main__":
    print list_of_lists()
    print list_of_tuples()
    print dictionary()
    print inverted_tuple()
