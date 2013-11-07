#! /usr/bin/env python
from __future__ import division
import string
from collections import defaultdict, Counter
from random import random, choice
import syllables
import sys


def clean_input(data):
    output = ''
    data = data.lower()
    for char in data:
        if char in string.lowercase:
            output += char
        else:
            output += ' '
    return output


def create_mapping_table(data):
    words = data.split()
    markov_mapping = defaultdict(lambda: Counter())

    for n in range(len(words) - 1):
        word, after = words[n], words[n + 1]
        markov_mapping[word][after] += 1

    return markov_mapping


def calculate_probabilities(table):
    probabily_mapping = {}
    for word, mapping in table.iteritems():
        occurances = dict(mapping.most_common())
        total_words = sum(occurances.values())
        for k, v in occurances.items():
            occurances[k] = v / total_words
        probabily_mapping[word] = occurances
    return probabily_mapping


def select_followon_word(mapping, word):
    followons = mapping[word]
    val = random()
    for follower, prob in followons.iteritems():
        val -= prob
        if val <= 0:
            return follower
    return follower


def count_syllables(word):
    #d = cmudict.dict()
    #return [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]
    return syllables.count(word)


def count_syllables_in_line(line):
    syllable_count = 0
    for word in line:
        syllable_count += count_syllables(word)
    return syllable_count


def generate_line(mapping, target_syllables=5):
    words = [choice(mapping.keys())]
    while count_syllables_in_line(' '.join(words)) != target_syllables:
        if count_syllables_in_line(' '.join(words)) > target_syllables:
            return None
        else:
            words.append(select_followon_word(mapping, words[-1]))
    return ' '.join(words)


def make_haiku(mapping):
    art = []
    for line in range(3):
        if line == 1:
            target_syllables = 7
        else:
            target_syllables = 5
        current_line = None
        while current_line is None:
            current_line = generate_line(mapping, target_syllables)
        art.append(current_line)
    return '\n'.join(art)


def make_art(input_corpus):
    clean_input_corpus = clean_input(input_corpus)
    mapping_table = calculate_probabilities(create_mapping_table(clean_input_corpus))
    print(make_haiku(mapping_table))

if __name__ == '__main__':
    args = sys.argv[1:]
    corpus = ""
    for f in args:
        with open(f) as fh:
            corpus += fh.read()
    make_art(corpus)
