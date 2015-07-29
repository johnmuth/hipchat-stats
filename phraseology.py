from __future__ import division
import re
from urlparse import urlparse
from itertools import islice
import nltk
import numpy as np
from scipy.stats import binom
from nltk.tokenize import WhitespaceTokenizer

def get_phrases(messages, min_phrase_size, max_phrase_size, min_llr=0):
  wordlists = {}
  unigram_freq_dist = nltk.FreqDist()
  for message in messages:
    wordlist = get_words(message['message'])
    for word in wordlist:
        unigram_freq_dist[word] += 1
    wordlists[message['id']] = wordlist
  phrases = nltk.defaultdict(float)
  previous_freq_dist = None
  all_phrases_and_counts = {}
  ngrams_messageids = {}
  for i in range(2, max_phrase_size + 1):
    ngram_freq_dist = nltk.FreqDist()
    for id, wordlist in wordlists.items():
      next_ngrams = nltk.ngrams(wordlist, i)
      next_ngrams = filter(lambda x: is_likely_ngram(x, phrases), next_ngrams)
      for ngram in next_ngrams:
        ngram_freq_dist[ngram] += 1
        if ngram not in ngrams_messageids:
          ngrams_messageids[ngram]={}
        ngrams_messageids[ngram][id]=1
    for k, v in ngram_freq_dist.iteritems():
      if v > 1:
        occurrences_word1 = unigram_freq_dist[k[0]] if previous_freq_dist == None else previous_freq_dist[k[:-1]]
        occurrences_word2 = unigram_freq_dist[k[1]] if previous_freq_dist == None else unigram_freq_dist[k[len(k) - 1]]
        occurrences_word1_word2 = ngram_freq_dist[k]
        total_occurrences = unigram_freq_dist.N() if previous_freq_dist == None else previous_freq_dist.N()
        klog_likelihood_ratio = log_likelihood_ratio(occurrences_word1, occurrences_word2, occurrences_word1_word2, total_occurrences)
        # print 'k=',k
        # print 'occurrences_word1=',occurrences_word1
        # print 'occurrences_word2=',occurrences_word2
        # print 'occurrences_word1_word2=',occurrences_word1_word2
        # print 'total_occurrences=',total_occurrences
        # print 'klog_likelihood_ratio=',klog_likelihood_ratio
        phrases[k] = klog_likelihood_ratio

    # restrict to log_likelihood_ratio > 0, i.e., the words occur together more often than they would by chance
    likely_phrases = nltk.defaultdict(float)
    likely_phrases.update([(k, v) for (k, v)
      in phrases.iteritems() if len(k) == i and v > min_llr])

    for k, v in likely_phrases.items():
      if i >= min_phrase_size:
        all_phrases_and_counts[k] = ngram_freq_dist[k]
    previous_freq_dist = ngram_freq_dist
  final_phrases = []
  for phrase, count in sorted(remove_redundant_subphrases(all_phrases_and_counts).items(), key=lambda phrase_count: int(phrase_count[1]), reverse=True):
    final_phrases.append({'phrase':" ".join(phrase), 'count':count, 'message_ids': ngrams_messageids[phrase].keys(), 'llr':phrases[phrase]})
  return final_phrases

def is_likely_ngram(ngram, phrases):
  if len(ngram) == 2:
    return True
  return phrases.has_key(ngram[:-1])

def get_words(message):
  words = WhitespaceTokenizer().tokenize(message.strip().lower())
  # truncate urls
  words = map(lambda word:truncate_if_url(word), words)
  # remove trailing punctuation
  return map(lambda word:re.sub(r'\W+$', '', word), words)

def remove_redundant_subphrases(phrases):
  deduped_phrases = {}
  seen_phrases = {}
  # sort by phrase length, longest first
  for phrase, count in sorted(phrases.items(), key=lambda phrase: len(phrase[0]), reverse=True):
    if phrase not in seen_phrases:
      deduped_phrases[phrase] = count
    for i in range(len(phrase) - 1, 0, -1):
      for subphrase in window(phrase, i):
        seen_phrases[subphrase] = 1
        if subphrase in phrases:
          subphrase_count = phrases[subphrase]
          if subphrase_count != count:
            deduped_phrases[subphrase] = subphrase_count
  return deduped_phrases


def window(seq, n=2):
  "Returns a sliding window (of width n) over data from the iterable"
  "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
  it = iter(seq)
  result = tuple(islice(it, n))
  if len(result) == n:
    yield result
  for elem in it:
    result = result[1:] + (elem,)
    yield result

def log_likelihood_ratio(occurrences_word1, occurrences_word2, occurrences_word1_word2, occurrences_all):
  p2 = occurrences_word2 / occurrences_all
  p12 = occurrences_word1_word2 / occurrences_all
  p2not12 = (occurrences_word2 - occurrences_word1_word2) / occurrences_all
  logpmf00 = binom(occurrences_word1, p2).logpmf(occurrences_word1_word2)
  logpmf01 = binom(occurrences_all - occurrences_word1, p2).logpmf(occurrences_word2 - occurrences_word1_word2)
  logpmf10 = binom(occurrences_word1, p12).logpmf(occurrences_word1_word2)
  logpmf11 = binom(occurrences_all - occurrences_word1, p2not12).logpmf(occurrences_word2 - occurrences_word1_word2)
  probs = np.matrix([
    [logpmf00, logpmf01],
    [logpmf10, logpmf11]])
  return np.sum(probs[1, :]) - np.sum(probs[0, :])

def nltk_init():
    try:
        nltk.word_tokenize("hello world")
    except LookupError as e:
        nltk.download('punkt')

def normalize_message(message):
  words = get_words(message['message'].encode('utf-8'))
  return ' '.join(words)

def truncate_if_url(input):
  result = urlparse(input)
  if result.scheme == '':
    return input
  else:
    return result.scheme + '://' + result.netloc

