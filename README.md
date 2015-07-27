# hipchat-stats

A web app for stats about HipChat chats.

## Overview

hipchat-stats finds frequently occurring 'interesting' phrases in a HipChat chatroom history.

It does a bit of statistical analysis to identify interesting phrases, https://en.wikipedia.org/wiki/Likelihood-ratio_test

## Running

You must set environment variables HIPCHAT_API_KEY and REDIS_HOST

Run 

```
$ pip install -r requirements.txt
$ pip install -r conda_requirements.txt
$ export HIPCHAT_API_KEY=hipchat-api-key
$ export REDIS_HOST=redis-hostname
$ ./hipchat-stats-webapp.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

## TODO

  * Analyse more than most recent 1000 messages
  * when displaying messages that contained a phrase, also display one or two of the messages immediately before and after, for context
  * eliminate common but uninteresting phrases like 'I am'
    * phrases consisting only of stopwords, pronouns, ...?
  * identify trends
