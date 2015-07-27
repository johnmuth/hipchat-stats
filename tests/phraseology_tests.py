import phraseology
import codecs
import numpy.testing

def test_get_phrases():
    messages = [ { 'id':"123",'message': "Hello, my name is John Doe."}, { 'id':"456" ,'message': "The rain in Spain falls mainly on the plain."}, { 'id': "789",'message' : "My name is Bob." }]
    gotPhrases = phraseology.get_phrases(messages, 2, 3)
    assert gotPhrases == [{'phrase':'my name is', 'count':2, 'message_ids': ["123", "789"]}]

def test_get_phrases_with_url():
    messages = [{ 'id':"123",'message' : "Looks like http://goo.com/abc is fucked"}, {'id':"234",'message' : "http://goo.com/def is fucked" }]
    gotPhrases = phraseology.get_phrases(messages, 2, 3)
    assert gotPhrases == [{'count': 2, 'phrase': 'http://goo.com is fucked', 'message_ids': ['234', '123']}]

def test_get_words():
    with codecs.open('tweets.txt','r',encoding='utf8') as f:
        tweets = f.readlines()
    tweet = tweets[0]
    words = phraseology.get_words(tweet)
    assert words[0].encode('utf-8') == "rt"
    assert words[1].encode('utf-8') == "@kirkkus"

def test_remove_redundant_phrases():
    originalPhrases = {('http://goo.com', 'is', 'fucked'): 2, ('http://goo.com', 'is'): 2, ('is', 'fucked'): 2, ('a', 'completely', 'different', 'phrase'): 4}
    expectedResult = {('a', 'completely', 'different', 'phrase'): 4, ('http://goo.com', 'is', 'fucked'): 2}
    actualResult = phraseology.remove_redundant_subphrases(originalPhrases)
    assert actualResult == expectedResult

def test_logLikelihoodRatio():
    actual_log_likelihood_ratio = phraseology.log_likelihood_ratio(100, 25, 20, 100000)
    numpy.testing.assert_almost_equal(actual_log_likelihood_ratio, 7.5, 1)

def test_truncate_url():
    result1 = phraseology.truncate_if_url('http://abc.def/foo/bar')
    assert result1 == 'http://abc.def'

def test_dont_truncate_nonurl():
    result1 = phraseology.truncate_if_url('bicycle')
    assert result1 == 'bicycle'
