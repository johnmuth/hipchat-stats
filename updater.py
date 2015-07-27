#!/usr/bin/env python

import datetime
import hipchat
import phraseology
import redisclient

def room_list_update():
    redisclient.set_rooms(hipchat.get_rooms())

def room_phrases_update(room_id):
    all_messages = []
    messages_per_day = {}

    room_update(room_id)

    for message in hipchat.get_history(room_id, datetime.datetime.utcnow()):
        redisclient.set_message(message)
        all_messages.append(message)
        message_date = message['date'][0:10]
        if message_date not in messages_per_day:
            messages_per_day[message_date]=[]
        messages_per_day[message_date].append(message)

    phrases = phraseology.get_phrases(all_messages, 2, 4)
    if len(phrases) > 0:
        for phrase in phrases:
            redisclient.set_messageids_for_room_phrase(room_id, phrase['phrase'], phrase['message_ids'])
        redisclient.set_phrases_for_room(room_id, phrases)

    for date in messages_per_day.keys():
        phrases = phraseology.get_phrases(messages_per_day[date], 2, 4)
        if len(phrases) > 0:
            redisclient.set_phrases_for_room_date(room_id, date, phrases)

    date_strings = map(lambda date: str(date), sorted(messages_per_day.keys()))
    redisclient.set_dates_for_room(room_id, date_strings)
    return phrases

def room_update(room_id):
    room = hipchat.get_room(room_id)
    redisclient.set_room(room)
    return room
