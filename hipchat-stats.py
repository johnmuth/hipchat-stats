# -*- coding: utf-8 -*-
"""
    HipChatStats
    ~~~~~~

    A web app for stats about HipChat chats.

"""

from __future__ import division
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import hypchat
import datetime
import operator
import nltk
import numpy as np
from scipy.stats import binom
import string
import unicodedata
import pprint
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True
))

@app.route('/')
def show_rooms():
    rooms = get_hc().rooms()['items']
    return render_template('rooms.html', rooms=sorted(rooms, key=lambda room: room['name']))

@app.route('/room/<int:room_id>')
def show_room(room_id):
    room = get_hc().get_room(room_id)
    stats = room.statistics.self()
    pprint.pprint(stats.last_active)
    return render_template('room.html', room=room, messages_sent=stats.messages_sent, last_active=stats.last_active.encode('utf-8'))

@app.route('/room/<int:room_id>/significant-phrases')
def show_significant_phrases(room_id):
    room = get_hc().get_room(room_id)
    messages = get_messages(room_id)
    phrases = get_phrases(messages)
    return render_template('significant-phrases.html', room=room, phrases=sorted(phrases.items(), key=operator.itemgetter(1), reverse=True))

@app.route('/room/<int:room_id>/messages')
def show_room_messages(room_id):
    room = get_hc().get_room(room_id)
    messages = get_message_objs(room_id)
    query = request.args.get('q')
    filtered_messages = [ message for message in messages if query in normalize_message(message) ]
    return render_template('messages.html', room=room, messages=filtered_messages, phrase=query)

def get_hc():
    return hypchat.HypChat(os.getenv('HIPCHAT_API_KEY', 'HIPCHAT_API_KEY env var not set'))

def get_messages(room_id):
    messages = []
    for message_obj in get_message_objs(room_id):
        messages.append(message_obj['message'].encode('utf-8'))
    return messages

def get_message_objs(room_id):
    room = get_hc().get_room(room_id)
    return room.history(maxResults=1000).contents()


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

def get_phrases(messages):
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
  for i in range(2, 5):
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

if __name__ == "__main__":
    try:
        nltk.word_tokenize("hello world")
    except LookupError as e:
        nltk.download('punkt')
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')))


