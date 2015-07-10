# hipchat-stats

A web app for stats about HipChat chats.

## Overview

hipchat-stats shows you the most frequently occurring phrases in a HipChat chatroom history.

It does a bit of statistical analysis to discard frequently occurring but insignificant phrases, e.g., "I am". https://en.wikipedia.org/wiki/Likelihood-ratio_test

## Install dependencies

```
$ pip install -r requirements.txt
```

## Run it

You must set environment variable HIPCHAT_API_KEY

```
$ export HIPCHAT_API_KEY=xxx-my-hipchat-api-key
$ ./hipchat-stats.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

## Tests

```
$ pip install -r test_requirements.txt
$ nosetests
```


## TODO

  * Do better at eliminating common but uninteresting phrases like 'I am'.
  * Fetch and analyse more than most recent 1000 messages.
  * When showing messages that contained a phrase, show more context, maybe one message before and after.
  * Analyse trends: phrase usage over time.

