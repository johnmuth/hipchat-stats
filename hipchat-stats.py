#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
    HipChatStats
    ~~~~~~

    A web app for stats about HipChat chats.

"""

import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import datetime
import unicodedata
import pprint
import sys
import operator
from hipchat import get_rooms, get_room, get_messages, get_message_objs
from phraseology import get_phrases, normalize_message, nltk_init

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config.update(dict( DEBUG=True))

@app.route('/')
def show_rooms():
    return render_template('rooms.html', rooms=sorted(get_rooms(), key=lambda room: room['name']))

@app.route('/room/<int:room_id>')
def show_room(room_id):
    room = get_room(room_id)
    stats = room.statistics.self()
    pprint.pprint(stats.last_active)
    return render_template('room.html', room=room, messages_sent=stats.messages_sent, last_active=stats.last_active.encode('utf-8'))

@app.route('/room/<int:room_id>/significant-phrases')
def show_significant_phrases(room_id):
    room = get_room(room_id)
    messages = get_messages(room_id)
    phrases = get_phrases(messages, 2, 4)
    return render_template('significant-phrases.html', room=room, phrases=sorted(phrases.items(), key=operator.itemgetter(1), reverse=True))

@app.route('/room/<int:room_id>/messages')
def show_room_messages(room_id):
    room = get_room(room_id)
    messages = get_message_objs(room_id)
    query = request.args.get('q')
    filtered_messages = [ message for message in messages if query in normalize_message(message) ]
    return render_template('messages.html', room=room, messages=filtered_messages, phrase=query)


if __name__ == "__main__":
    nltk_init()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')))


