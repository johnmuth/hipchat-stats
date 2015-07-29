import os
import hypchat

def get_rooms():
    rooms = []
    for room in sorted(hc().rooms()['items'], key=lambda room: room['name'].lower()):
        rooms.append({'id':room['id'], 'name':room['name']})
    return rooms

def get_room(room_id):
    room = hc().get_room(room_id)
    stats = room.statistics.self()
    return { 'id' : room_id, 'name' : room.name, 'messages_sent' : stats.messages_sent, 'last_active' : stats.last_active }

def get_messages(room_id, maxResults=1000):
    messages = []
    for item in hc().get_room(room_id).history(maxResults=maxResults).contents():
        messages.append({'id':item['id'], 'message':item['message'], 'date':item['date'].isoformat(), 'from': item['from']})
    return messages

def get_message_objs(room_id, maxResults=1000):
    return hc().get_room(room_id).history(maxResults=maxResults).contents()

def get_history(room_id, date):
    messages = []
    for item in hc().get_room(room_id).history(date='recent', maxResults=1000).contents():
        messages.append({'id':item['id'], 'message':item['message'], 'date':item['date'], 'from': item['from']})
    return messages

def hc():
    if os.getenv('HIPCHAT_API_KEY') is None:
        raise Exception("HIPCHAT_API_KEY env var must be set")
    return hypchat.HypChat(os.getenv('HIPCHAT_API_KEY'))

