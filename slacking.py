from slackclient import SlackClient
import random
import sys, getopt

print("Number of arguments: %s arguments" % len(sys.argv))
#print 'Argument List:', str(sys.argv)

#slack_token = os.environ["SLACK_API_TOKEN"]
def slack_token():
  return "xoxp-3127633817-29010123941-101221187830-9492d5368bd19281865733e3f18c4205"

def sc():
  return SlackClient(slack_token())

def channa():
  return channels()['general']

def channels():
  chans = {}
  response = sc().api_call(
    "channels.list",
    exclude_archived=1
  )

  for c in response['channels']:
    chans[c['name']] = c['id']
  return chans

def last_channel_msg(channel):
  lst_msg = sc().api_call(
    "channels.history",
    channel=channel,
    count = 1
  )
  return lst_msg['messages'][0]

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

#response = sc.api_call(
#  "chat.update",
#  ts='1478278703.000138',
#  channel="C033RJMQF",
#  text="i am slackbot all your message are belong to me :snake:"
#)

#response = sc.api_call(
#  "reactions.add",
#  channel=channels['ideas'],
#  name="cry",
#  timestamp="1478281469.000027"
#)

def parrot_wave(channel, msg):
  for i in range(1,8):
    sc().api_call(
      "reactions.add",
      channel=channel,
      name="parrot_wave_{0}".format(i),
      timestamp=msg['ts']
    )

def main(argv):
  channel = ''
  command = ''
  help_response = 'test.py -c <channel> -o <command>'
  try:
    opts, args = getopt.getopt(argv,"hc:o:",["channel=","command="])
  except getopt.GetoptError:
    print(help_response)
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print(help_response)
      sys.exit()
    elif opt in ("-c", "--channel"):
      channel = channels()[arg]
    elif opt in ("-o", "--command"):
      command = arg

  print("Channel is %s" % channel)
  print("Command is %s" % command)

  if command == "pw":
    parrot_wave(channel, last_channel_msg(channel))
  elif command == "re":
    slap_random_emoji(channel, last_channel_msg(channel))
  else:
    print("command: %s is unknown" % command)

print(__name__)

if __name__ == "__main__":
  main(sys.argv[1:])

