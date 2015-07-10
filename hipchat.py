import os
import hypchat

def get_rooms():
    return hc().rooms()['items']

def get_room(room_id):
    return hc().get_room(room_id)

def get_messages(room_id):
    messages = []
    for message_obj in get_message_objs(room_id):
        messages.append(message_obj['message'].encode('utf-8'))
    return messages

def get_message_objs(room_id):
    return get_room(room_id).history(maxResults=1000).contents()
    
def hc(): 
    if os.getenv('HIPCHAT_API_KEY') is None:
        raise Exception("HIPCHAT_API_KEY env var must be set")
    return hypchat.HypChat(os.getenv('HIPCHAT_API_KEY'))

