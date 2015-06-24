# hipchat-stats

A web app for stats about HipChat chats.

## Overview

hipchat-stats shows you the most frequently occurring phrases in a HipChat chatroom history.

It does a bit of statistical analysis to discard frequently occurring but insignificant phrases, e.g., "I am". https://en.wikipedia.org/wiki/Likelihood-ratio_test

## Running

You must set environment variable HIPCHAT_API_KEY

Run 

```
$ python setup.py
$ export HIPCHAT_API_KEY=xxx-my-hipchat-api-key
$ python hipchat-stats.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```
