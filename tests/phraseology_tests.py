from nose.tools import *
import phraseology

def test_llr():
    assert phraseology.llr(2, 2, 2, 19) == 1.8908357968738141

def test_get_phrases():
    messages = [ "Hello, my name is John Doe.", "The rain in Spain falls mainly on the plain.", "My name is Bob."]
    assert phraseology.get_phrases(messages, 2, 3) == {('my', 'name'): 2, ('name', 'is'): 2}

