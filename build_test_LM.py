#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import nltk
import sys
import getopt
from nltk import ngrams
import math

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print('building language models...')
    # creating a dictionary to store all languages as keys mapping to a list of 4-grams storing their respective occurrences
    lm_dict = {"malaysian" : {}, "indonesian" : {}, "tamil" : {}}
    # opening the input file for reading and getting all the training sentences in lines
    file1 = open(in_file, "r", encoding = "utf8")
    lines = file1.readlines()
    # count_per_language will keep track of the total count of 4 grams for that language (includes smoothing)
    count_per_language = {"malaysian" : 0, "indonesian" : 0, "tamil" : 0}
    for line in lines:
        # getting the label(language) from the training set and the data - the sentence
        language, sentence = line.split(' ', 1)
        chrs = [c for c in sentence]
        # generating all the character 4 grams from the sentence by using the build in function in nltk
        n_grams = ngrams(chrs, 4)
        for ngram in n_grams:
            for lang in lm_dict:
                if ngram not in lm_dict[lang]:
                    # adding Laplace smoothing for all languages
                    lm_dict[lang][ngram] = 1
                    count_per_language[lang] += 1
            # need to increase the count for this 4gram in the labeled language
            lm_dict[language][ngram] += 1
            count_per_language[language] += 1

    return lm_dict, count_per_language


# helper function that calculates the max probability label given the new 4 grams and the training counts
def getLabel(n_grams, lm_dict, LanguageCount):

    # out_of_vocab and count will keep track of the number of unseen 4grams and total number of 4grams in the sentence respectively, and if the frequency of unseen 4grams is high
    # (probability limit given by threshold) we consider that sentence as other
    out_of_vocab = 0
    count = 0
    # THRESHOLD will give us the limit on the probability on when to consider this sentence as none of the 3 labeled languages
    THRESHOLD = 0.7
    for ngram in n_grams:
        count += 1
        # if a 4 gram doesnt appear in at least one of the languages,
        # it means it is not in any of them since we added smoothing ! so we can just check if it's not in (eg.) tamil
        if ngram not in lm_dict["tamil"]:
            # if this is an unseen ngram, we remove it and increase the out of vocab ngrams
            n_grams.remove(ngram)
            out_of_vocab += 1
    predicted_language = ""
    first = True

    for language in lm_dict:
        probability = 0
        for ngram in n_grams:
            if ngram in lm_dict[language]:
                # calculate the total log probability of the sentence in one language by adding up the log probabilities of individual 4grams,
                # we have a probability range from approximately [-2000, 0]
                probability += (math.log10(lm_dict[language][ngram] / float(LanguageCount[language])))
        # since the log probability is negative, use the first probability found to initialize the max_log_probability and predicted language
        if first:
            first = False
            max_log_probability = probability
            predicted_language = language
        # update the predicted language if the current language has a higher probability
        elif probability >= max_log_probability:
            max_log_probability = probability
            predicted_language = language
        # checking if we have a higher number of out of vocabulary words, and if so, the predicted language would be other
        if out_of_vocab / float(count) >= THRESHOLD:
            max_log_probability = out_of_vocab / float(count)
            predicted_language = "other"

    return predicted_language, max_log_probability

def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # opening the input test file for reading and the output file for writing
    test_file = open(in_file, "r", encoding="utf8")
    test_data = test_file.readlines();
    output_file = open(out_file, 'w')
    for line in test_data:
        chrs = [c for c in line]
        # generating character 4 grams from the test sentence
        n_grams = ngrams(chrs, 4)
        # using the helper method to calculate the log probability and the predicted language
        label, probability = getLabel(list(n_grams), LM[0], LM[1])
        # writing the result to the output file
        output_file.write(label + " " + line)

def usage():
    print("usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file")

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
