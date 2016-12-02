from slackclient import SlackClient
import random
import os
import subprocess
import sys, getopt
import re

# print("Number of arguments: %s arguments" % len(sys.argv))
# print('Argument List:', str(sys.argv))

def slack_token():
  return os.environ["SLACK_API_TOKEN"]

def sc():
  return SlackClient(slack_token())

def channels():
  chans = {}
  response = sc().api_call(
    "channels.list",
    exclude_archived=1
  )

  for c in response['channels']:
    chans[c['name']] = c['id']
  return chans

def channel_messages(channel, count=None):
  if count is None:
    count = 5

  messages = sc().api_call(
    "channels.history",
    channel=channel,
    count=count
  )
  return messages

def last_channel_msg(channel):
  lst_msg = sc().api_call(
    "channels.history",
    channel=channel,
    count = 1
  )
  return lst_msg['messages'][0]

def fetch_user(user_id):
  user_info = sc().api_call(
    "users.info",
    user=user_id
  )
  return user_info

def emoji_list():
  response = sc().api_call("emoji.list")

  emoji = {}
  for e in response['emoji']:
    emoji[e] = response['emoji'][e]

  return emoji

def random_emoji():
  return random.sample(list(emoji_list()), 1)[0]

def slap_random_emoji(channel, msg):
  return sc().api_call(
    'reactions.add',
    channel=channel,
    name=random_emoji(),
    timestamp=msg['ts']
  )

def send_message(channel, message):
  return sc().api_call(
    "chat.postMessage",
    text=message,
    channel=channel,
    as_user='true'
  )

def parrot_wave(channel, msg, dir):
  rng = range(1,8) if dir == 'norm' else range(8,1)

  for i in rng:
    sc().api_call(
      "reactions.add",
      channel=channel,
      name="parrot_wave_{0}".format(i),
      timestamp=msg['ts']
    )

def emoji_bomb(channel, msg):
  for i in range(0,20):
    sc().api_call(
     "reactions.add",
     channel=channel,
     name=random_emoji(),
     timestamp=msg['ts']
    )

def main(argv):
  channel = ''
  command = ''
  count = -1
  stream = None
  help_response = """slacking.py -c <channel> -o <operation> [-n <count> -m <message>]
  commands:
    pw - parrot wave
    pwr - parrot wave reverse
    re - random emoji
    eb - emoji bomb
    cms - channel messages (opt arg: -n count - default 5)
    ls - list channels
    msg - send message (-m message)
    cmd - pipe command stdout to slack channel
  """
  try:
    opts, args = getopt.getopt(argv,"hc:o:n:m:",["channel=","operation=","count=","message="])
  except getopt.GetoptError:
    print(help_response)
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print(help_response)
      sys.exit()
    elif opt in ("-c", "--channel"):
      m = re.search('(^@)', arg)
      channel =  channels()[arg] if m is None else arg
    elif opt in ("-o", "--operation"):
      command = arg
    elif opt in ("-n", "--count"):
      count = arg
    elif opt == "-":
      #stream = sys.stdin
      for line in sys.stdin:
        stream += len(line)

    elif opt in ("-m", "--message"):
      stream = arg

  #print("Channel is %s" % channel)
  #print("Command is %s \n" % command)

  if command == "pw":
    parrot_wave(channel, last_channel_msg(channel), 'norm')
  elif command == "pwr":
    parrot_wave(channel, last_channel_msg(channel), 'rev')
  elif command == "re":
    slap_random_emoji(channel, last_channel_msg(channel))
  elif command == "eb":
    emoji_bomb(channel, last_channel_msg(channel))
  elif command == "cms":
    num_msg = count if count > 0 else None
    for msg in reversed(channel_messages(channel, num_msg)['messages']):
      if 'user' in msg:
        print("username: %s" % fetch_user(msg['user'])['user']['name'])
      print("message: %s" % msg['text'])
  elif command == "ls":
    chans = channels()
    for name in chans:
      print(name)
  elif command == "msg":
    print(stream)
    print(send_message(channel, stream))
  elif command == "cmd":
    stdout = subprocess.check_output(stream.split(), stderr=subprocess.STDOUT, universal_newlines=True)
    print(send_message(channel, stdout))
  else:
    print("command: %s is unknown" % command)

if __name__ == "__main__":
  main(sys.argv[1:])

