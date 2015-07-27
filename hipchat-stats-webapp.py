#!/usr/bin/env python

"""
    HipChatStats
    ~~~~~~

    A web app for stats about HipChat chats.

"""

import os
import sys

from flask import Flask, request, render_template
import phraseology
import redisclient
import updater

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config.update(dict( DEBUG=True))

@app.route('/')
def show_rooms():
    return render_template('rooms.html', rooms=redisclient.get_rooms())

@app.route('/room/<int:room_id>')
def show_room(room_id):
    room = redisclient.get_room(room_id)
    if 'id' not in room:
        room = updater.room_update(room_id)
    return render_template('room.html', room=room)

@app.route('/room/<int:room_id>/significant-phrases')
def show_significant_phrases(room_id):
    room = redisclient.get_room(room_id)
    phrases = redisclient.get_phrases_for_room(room_id)
    if len(phrases)==0:
        phrases = updater.room_phrases_update(room_id)
    return render_template('significant-phrases.html', room=room, phrases=phrases)

@app.route('/room/<int:room_id>/messages')
def show_room_messages(room_id):
    room = redisclient.get_room(room_id)
    messages = redisclient.get_messages_for_room_phrase(room_id, request.args.get('q'))
    print 'message=',messages
    # query = request.args.get('q')
    # filtered_messages = [ message for message in messages if query in phraseology.normalize_message(message) ]
    return render_template('messages.html', room=room, messages=messages, phrase=request.args.get('q'))


if __name__ == "__main__":
    phraseology.nltk_init()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')))

