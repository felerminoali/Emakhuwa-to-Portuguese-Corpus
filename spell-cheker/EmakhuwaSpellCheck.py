import re
import string
from collections import Counter
import numpy as np


class SpellChecker(object):

    def __init__(self, corpus_file_path):
        with open(corpus_file_path, "r", encoding="utf8") as file:
            lines = file.readlines()
            words = []
            for line in lines:
                words += re.findall(r'\w+', line.lower())

        self.vocabs = set(words)
        self.word_counts = Counter(words)
        total_words = float(sum(self.word_counts.values()))
        self.word_probas = {word: self.word_counts[word] / total_words for word in self.vocabs}
        self.word_freq = {word: self.word_counts[word] for word in self.vocabs}
        self.intended_possible_words = {}

    def possible_words(self, word):
        candidates = self._level_one_edits(word) or self._level_two_edits(word) or [word]
        return [w for w in candidates if w in self.vocabs]

    def dict_freq(self):
        return self.word_freq

    def abs_prob(self, typo):
        """Function that takes a typo in the form of a string and a corpus in the form of a list
        and returns a dictionary of probabilities for all possible correction candidates"""
        count = {}
        freq_ = self.dict_freq()
        for poss_word in self.possible_words(typo):
            if poss_word in freq_.keys():
                count[poss_word] = (freq_[poss_word], '{0:.10f}'.format(
                    (freq_[poss_word]) / (float(sum(self.word_counts.values())))))  # format up to 10 decimal places
            prob = {k: v for k, v in sorted(count.items(), key=lambda x: x[1], reverse=True)}
        return prob

    def _level_one_edits(self, word):
        letters = ['a', 'aa', 'c', 'e', 'ee', 'f', 'h', 'i', 'ii', 'k', 'kh', 'l', 'm', 'n', 'ny', 'ng', 'o', 'oo', 'p',
                   'ph', 'r', 's', 't', 'th', 'tt', 'tth', 'u', 'uu', 'v', 'w', 'x', 'y']
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [l + r[1:] for l, r in splits if r]
        swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r) > 1]
        replaces = [l + c + r[1:] for l, r in splits if r for c in letters]
        inserts = [l + c + r for l, r in splits for c in letters]

        return set(deletes + swaps + replaces + inserts)

    def _level_two_edits(self, word):
        return set(e2 for e1 in self._level_one_edits(word) for e2 in self._level_one_edits(e1))

    def _level_three_edits(self, word):
        return set(e3 for e2 in self._level_two_edits(word) for e3 in self._level_one_edits(e2))

    def check(self, word):
        candidates = self._level_one_edits(word) or self._level_two_edits(word) or [word]
        valid_candidates = [w for w in candidates if w in self.vocabs]
        return sorted([(c, self.word_probas[c]) for c in valid_candidates], key=lambda tup: tup[1], reverse=True)


# Python3 program to demonstrate auto-complete
# feature using Trie data structure.
# Note: This is a basic implementation of Trie
# and not the most optimized one.
class TrieNode():
    def __init__(self):
        # Initialising one node for trie
        self.children = {}
        self.last = False


class Trie():
    def __init__(self):

        # Initialising the trie structure.
        self.root = TrieNode()
        self.word_list = []

    def formTrie(self, keys):

        # Forms a trie structure with the given set of strings
        # if it does not exists already else it merges the key
        # into it by extending the structure as required
        for key in keys:
            self.insert(key)  # inserting one key to the trie.

    def insert(self, key):

        # Inserts a key into trie if it does not exist already.
        # And if the key is a prefix of the trie node, just
        # marks it as leaf node.
        node = self.root

        for a in list(key):
            if not node.children.get(a):
                node.children[a] = TrieNode()

            node = node.children[a]

        node.last = True

    def search(self, key):

        # Searches the given key in trie for a full match
        # and returns True on success else returns False.
        node = self.root
        found = True

        for a in list(key):
            if not node.children.get(a):
                found = False
                break

            node = node.children[a]

        return node and node.last and found

    def suggestionsRec(self, node, word):

        # Method to recursively traverse the trie
        # and return a whole word.
        if node.last:
            self.word_list.append(word)

        for a, n in node.children.items():
            self.suggestionsRec(n, word + a)

    def printAutoSuggestions(self, key, checker):

        # Returns all the words in the trie whose common
        # prefix is the given key thus listing out all
        # the suggestions for autocomplete.
        node = self.root
        not_found = False
        temp_word = ''

        for a in list(key):
            if not node.children.get(a):
                not_found = True
                break

            temp_word += a
            node = node.children[a]

        if not_found:
            return 0
        elif node.last and not node.children:
            return -1

        self.suggestionsRec(node, temp_word)

        # # add infixes too
        # for s in checker.vocabs:
        #     if s.find(key) != -1:
        #         self.word_list.append(s)

        candidates = sorted([(c, checker.word_probas[c]) for c in self.word_list], key=lambda tup: tup[1], reverse=True)
        print(candidates)
        # for s in self.word_list:
        #     print(s)
        #     print(checker.word_probas[s])

        return 1


# noisy channel part


if __name__ == '__main__':
    checker = SpellChecker("./emakhuwa.txt")

    # word = "opajer"
    while True:
        print('Insira uma palavra')
        word = input()
        spelling_suggestions = checker.check(word)

        if len(spelling_suggestions) == 0:
            print("Did you mean?")

            vocabs_array = np.array(list(checker.vocabs))
            # Driver Code
            keys = vocabs_array

            # creating trie object
            t = Trie()

            # creating the trie structure with the
            # given set of strings.
            t.formTrie(keys)

            # autocompleting the given key using
            # our trie structure.
            comp = t.printAutoSuggestions(word, checker)

            if comp == -1:
                print("No other strings found with this prefix\n")
            elif comp == 0:
                print("No string found with this prefix\n")
        else:
            print(spelling_suggestions)
            # print(checker.possible_words(word))
            # print(len(checker.word_freq))
            # print(checker.abs_prob(word))
