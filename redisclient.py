import redis
import os
import json

def get_phrases_for_room(room_id):
    return json.loads(rc().get(room_phrase_key(room_id)) or "[]")

def set_phrases_for_room(room_id, phrases):
    rc().set(room_phrase_key(room_id), json.dumps(phrases))

def get_dates_for_room(room_id):
    return json.loads(rc().get(dates_key(room_id)))

def set_dates_for_room(room_id, dates):
    rc().set(dates_key(room_id), json.dumps(dates))

def get_phrases_for_room_date(room_id, date):
    return json.loads(rc().get(room_date_phrase_key(room_id, date)))

def set_phrases_for_room_date(room_id, date, phrases):
    rc().set(room_date_phrase_key(room_id, date), json.dumps(phrases))

def get_messageids_for_room_phrase(room_id, phrase):
    return json.loads(rc().get(messages_key(room_id, phrase)))

def set_messageids_for_room_phrase(room_id, phrase, messages):
    rc().set(messages_key(room_id, phrase), json.dumps(messages))

rooms_key = 'rooms'

def set_rooms(rooms):
    rc().set(rooms_key,json.dumps(rooms))

def get_rooms():
    return json.loads(rc().get(rooms_key))

def set_room(room):
    rc().set(room_key(room['id']),json.dumps(room))

def get_room(room_id):
    return json.loads(rc().get(room_key(room_id)) or "{}")

def set_message(message):
    message['date'] = message['date'].isoformat()
    rc().set(message_key(message['id']),json.dumps(message))

def get_message(message_id):
    return json.loads(rc().get(message_key(message_id)))

def rc():
    if os.getenv('REDIS_HOST') is None:
        raise Exception("REDIS_HOST env var must be set")
    return redis.StrictRedis(host=os.getenv('REDIS_HOST'))

def dates_key(room_id):
    return 'dates:'+ str(room_id)

def messages_key(room_id,phrase):
    return 'messages:'+ str(room_id) + ':' + phrase

def room_phrase_key(room_id):
    return 'phrases:'+ str(room_id)

def room_date_phrase_key(room_id, date):
    return 'phrases:'+ str(room_id) + ':' + str(date)

def room_key(room_id):
    return 'room:' + str(room_id)

def message_key(message_id):
    return 'message:' + str(message_id)

