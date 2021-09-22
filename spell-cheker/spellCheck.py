import re
import string
from collections import Counter
import numpy as np

def read_corpus(filename):
  with open(filename, "r", encoding="utf8") as file:
    lines = file.readlines()
    words = []
    for line in lines:
      words += re.findall(r'\w+', line.lower())

  return words

# words = read_corpus("./big.txt")
words = read_corpus("./emakhuwa.txt")
print(f"There are {len(words)} total words in the corpus")

vocabs = set(words)
print(f"There are {len(vocabs)} unique words in the vocabulary")

for v in sorted(vocabs):
  f = open("demofile.txt", "a", encoding="utf8")
  f.write(v+'\n')
  f.close()

# word_counts = Counter(words)
# print(word_counts["yesu"])
#
# total_word_count = float(sum(word_counts.values()))
# word_probas = {word: word_counts[word] / total_word_count for word in word_counts.keys()}
# print(word_probas["yesu"])
#
# def split(word):
#   return [(word[:i], word[i:]) for i in range(len(word) + 1)]
#
# print(split("trash"))
#
# def delete(word):
#   return [l + r[1:] for l,r in split(word) if r]
#
# print(delete("trash"))
#
# def swap(word):
#   return [l + r[1] + r[0] + r[2:] for l, r in split(word) if len(r)>1]
#
# print(swap("trash"))
#
# def replace(word):
#   letters = string.ascii_lowercase
#   return [l + c + r[1:] for l, r in split(word) if r for c in letters]
#
# print(replace("trash"))
#
# def replace_for_vmw(word):
#   letters = ['a', 'aa', 'c', 'e', 'ee', 'f', 'h', 'i', 'ii', 'k', 'kh', 'l', 'm', 'n', 'ny', 'ng', 'o', 'oo', 'p', 'ph', 'r', 's', 't', 'th', 'tt', 'tth', 'u', 'uu', 'v', 'w', 'x', 'y']
#   return [l + c + r[1:] for l, r in split(word) if r for c in letters]
#
# print(replace_for_vmw("trash"))
#
# def insert(word):
#   letters = string.ascii_lowercase
#   return [l + c + r for l, r in split(word) for c in letters]
#
# print(insert("trash"))
#
# def insert_for_vmw(word):
#   letters = ['a', 'aa', 'c', 'e', 'ee', 'f', 'h', 'i', 'ii', 'k', 'kh', 'l', 'm', 'n', 'ny', 'ng', 'o', 'oo', 'p', 'ph',
#              'r', 's', 't', 'th', 'tt', 'tth', 'u', 'uu', 'v', 'w', 'x', 'y']
#   return [l + c + r for l, r in split(word) for c in letters]
#
# print(insert_for_vmw("trash"))
#
# def edit1(word):
#   return set(delete(word) + swap(word) + replace_for_vmw(word) + insert_for_vmw(word))