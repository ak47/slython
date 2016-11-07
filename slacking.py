from slackclient import SlackClient

#slack_token = os.environ["SLACK_API_TOKEN"]
slack_token = "xoxp-3127633817-29010123941-101221187830-9492d5368bd19281865733e3f18c4205"
sc = SlackClient(slack_token)

channels = {
  'random': 'C033RJMQF',
  'ideas': 'C055KNP3Q',
  'engineering': 'C042VKA0B'
}

#response = sc.api_call(
#  "chat.postMessage",
#  channel="@zacc",
#  text="Hello from Python! :tada:",
#  as_user="true"
#)

#response = sc.api_call(
#  "channels.list",
#  exclude_archived=1
#)

response = sc.api_call(
  "channels.history",
  channel=channels['engineering'],
  count = 1
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

for m in response['messages']:
  print(m['ts'])
  for i in range(1,8):
    #print("parot_{0}".format(i))
    response = sc.api_call(
      "reactions.add",
      channel=channels['engineering'],
      name="parrot_wave_{0}".format(i),
      timestamp=m['ts']
    )

#print(response)
