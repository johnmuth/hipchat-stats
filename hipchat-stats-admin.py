#! /usr/bin/env python
import argparse
import sys
import json
import updater
import redisclient
import hipchat
import phraseology

class HipchatStatsAdmin(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Manages Hipchat Stats',
                                         usage='''hipchat-stats-admin <command> [<args>]

Commands are:

   room_list_update     Write list of chatrooms into redis, from hipchat api
   room_list_get        Get list of chatrooms from redis

   room_phrases_update  Write phrases into redis, from hipchat api
   room_phrases_get     Get phrases (from redis)

   room_dates_list      List dates for which room has phrases (from redis)

   message_get          Get message from redis
   messages_get         Get messages for a chatroom, from hipchat

''')
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command', args.command
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def room_list_update(self):
        updater.room_list_update()

    def room_list_get(self):
        print json.dumps(redisclient.get_rooms())

    def room_phrases_update(self):
        parser = argparse.ArgumentParser(description='Update phrases for room')
        parser.add_argument('--room_id', required=True, help='Id of room.')
        args = parser.parse_args(sys.argv[2:])
        updater.room_phrases_update(args.room_id)

    def room_phrases_get(self):
        parser = argparse.ArgumentParser(description='Update phrases for room')
        parser.add_argument('--room_id', required=True, help='Id of room.')
        parser.add_argument('--date', required=False, help='Get phrases for a specific date.')
        args = parser.parse_args(sys.argv[2:])
        phrases = redisclient.get_phrases_for_room(args.room_id) if args.date is None else redisclient.get_phrases_for_room_date(args.room_id, args.date)
        print json.dumps( phrases )

    def room_dates_list(self):
        parser = argparse.ArgumentParser(description='List dates for which room has phrases')
        parser.add_argument('--room_id', required=True, help='Id of room.')
        args = parser.parse_args(sys.argv[2:])
        print json.dumps( redisclient.get_dates_for_room(args.room_id))

    def message_get(self):
        parser = argparse.ArgumentParser(description='Get message from redis')
        parser.add_argument('--message_id', required=True, help='Id of message.')
        args = parser.parse_args(sys.argv[2:])
        message = redisclient.get_message(args.message_id)
        print json.dumps( message )

    def messages_get(self):
        parser = argparse.ArgumentParser(description='Get messages from a chatroom in hipchat')
        parser.add_argument('--room_id', required=True, help='Id of room.')
        args = parser.parse_args(sys.argv[2:])
        messages = hipchat.get_messages(args.room_id)
        print json.dumps( messages )

    def messages_get_phrases(self):
        parser = argparse.ArgumentParser(description='Get phrases from a messages json file')
        parser.add_argument('--file', required=True, help='file containing messages json')
        args = parser.parse_args(sys.argv[2:])
        with open(args.file) as data_file:
            messages = json.load(data_file)

        phrases = phraseology.get_phrases(messages)

        print json.dumps( phrases )


if __name__ == '__main__':
    HipchatStatsAdmin()
