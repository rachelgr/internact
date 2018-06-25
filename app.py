#!/usr/bin/env python
# encoding: utf-8

import os
from slackclient import SlackClient
from bottle import run, post


SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)

slack_client = SlackClient(SLACK_TOKEN)


# [[a,b,c],[d,e,f],[g,h,i]]
#NEXT STEP: For each array in arrays make a channel and add the people into it, send a welcome message, and then leave the channel

@post('/food')
def food():
    return 'I can recommend some places nearby'

def list_groups():
    groups_call = slack_client.api_call("groups.list")
    if groups_call['ok']:
        return groups_call['groups']
    return None

def list_users():
    users_call = slack_client.api_call("users.list")
    if users_call['ok']:
        return users_call['members']
    return None

def create_channel(num):
  name = "internact" + str(num)
  channel = slack_client.api_call(
    "groups.create",
    name=name
  )
  return channel

def add_to_channel(channel_id, user_id):
  slack_client.api_call(
    "groups.invite",
    channel=channel_id,
    user=user_id
  )

def name_id_map(alist):
  adict = {}
  if alist:
        for a in alist:
          adict[a['name']] = a['id']
  return adict

def make_meetings(user_array):
  num = 12
  user_dict = name_id_map(list_users())
  for group in user_array:
    channel = create_channel(num)
    print(channel)
    channel_id = channel["group"]["id"]
    num += 1
    for member in group:
      add_to_channel(channel_id,user_dict[member])
    send_message(channel_id, "https://gph.is/1UTspRa")
    send_message(channel_id,"Welcome to the chat!")





# def channel_info(channel_id):
#     channel_info = slack_client.api_call("channels.info", channel=channel_id)
#     if channel_info:
#         return channel_info['channel']
#     return None

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='internact-bot',
        icon_emoji=':robot_face:'
    )

if __name__ == '__main__':

    run(host='0.0.0.0', port=5000)

    groups_dict = name_id_map(list_groups())
    users_dict = name_id_map(list_users())

    send_message(groups_dict["privatechannel3"], "https://gph.is/1UTspRa")
    send_message(groups_dict["privatechannel3"],"Welcome to the chat!")

    # make_meetings([["gg1219","rachelgr"]])

    # create_channel(1)
    # add_to_channel(groups_dict['privatechannel2'],users_dict['gg1219'])


