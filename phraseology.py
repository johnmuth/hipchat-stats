from __future__ import division
import operator
import nltk
import numpy as np
import string
from scipy.stats import binom

def normalize_message(message):
    words = get_words(message['message'].encode('utf-8'))
    words = filter(lambda x: is_valid(x), words)
    return ' '.join(words)

def is_valid(word):
  if word.startswith("#"):
    return False # no hashtag
  else:
    vword = word.translate(string.maketrans("", ""), string.punctuation)
    return len(vword) == len(word)

def llr(c1, c2, c12, n):
  p0 = c2 / n
  p10 = c12 / n
  p11 = (c2 - c12) / n
  probs = np.matrix([
    [binom(c1, p0).logpmf(c12), binom(n - c1, p0).logpmf(c2 - c12)],
    [binom(c1, p10).logpmf(c12), binom(n - c1, p11).logpmf(c2 - c12)]])
  return np.sum(probs[1, :]) - np.sum(probs[0, :])

def is_likely_ngram(ngram, phrases):
  if len(ngram) == 2:
    return True
  prevGram = ngram[:-1]
  return phrases.has_key(prevGram)

def get_words(message):
    return nltk.word_tokenize(message.strip().lower())

def get_phrases(messages, min_phrase_size, max_phrase_size):
  lines = []
  unigramFD = nltk.FreqDist()
  for message in messages:
    words = get_words(message)
    words = filter(lambda x: is_valid(x), words)
    for word in words:
        unigramFD[word] += 1
    lines.append(words)
  phrases = nltk.defaultdict(float)
  prevGramFD = None
  allPhrasesAndCounts = {}
  for i in range(min_phrase_size, max_phrase_size):
    ngramFD = nltk.FreqDist()
    for words in lines:
      nextGrams = nltk.ngrams(words, i)
      nextGrams = filter(lambda x: is_likely_ngram(x, phrases), nextGrams)
      for nextGram in nextGrams:
        ngramFD[nextGram] += 1
    for k, v in ngramFD.iteritems():
      if v > 1:
        c1 = unigramFD[k[0]] if prevGramFD == None else prevGramFD[k[:-1]]
        c2 = unigramFD[k[1]] if prevGramFD == None else unigramFD[k[len(k) - 1]]
        c12 = ngramFD[k]
        n = unigramFD.N() if prevGramFD == None else prevGramFD.N()
        kllr = llr(c1, c2, c12, n)
        phrases[k] = kllr

    # only consider ngrams where LLR > 0, ie P(H1) > P(H0)
    likelyPhrases = nltk.defaultdict(float)
    likelyPhrases.update([(k, v) for (k, v)
      in phrases.iteritems() if len(k) == i and v > 0])

    sortedPhrases = sorted(likelyPhrases.items(),
      key=operator.itemgetter(1), reverse=True)
    for k, v in sortedPhrases:
      allPhrasesAndCounts[k] = ngramFD[k]
    prevGramFD = ngramFD

  return allPhrasesAndCounts

def nltk_init():
    try:
        nltk.word_tokenize("hello world")
    except LookupError as e:
        nltk.download('punkt')
