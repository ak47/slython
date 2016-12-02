# slython
hacking the slack api with python - because

## SLACK API TOKEN
You need a testing/development token: https://api.slack.com/docs/oauth-test-tokens

## Usage
```
» python slacking.py -h
slacking.py -c <channel> -o <operation> [-n <count> -m <message>]
  commands:
    pw - parrot wave
    pwr - parrot wave reverse
    re - random emoji
    eb - emoji bomb
    cms - channel messages (opt arg: -n count - default 5)
    ls - list channels
    msg - send message (-m message)
    cmd - pipe command stdout to slack channel

» export SLACK_API_TOKEN="xoxp-your-api-token-here"

» python slacking.py -o ls
gameofthrones
investing
slython

» python slacking.py -c slython -o cmd -m fortune
{'channel': 'C3A2C5LER', 'ts': '1480707833.000040', 'ok': True, 'message': {'ts': '1480707833.000040', 'bot_id': 'B39UZ6QJF', 'user': 'U0V0A3MTP', 'type': 'message', 'text': 'Lack of money is the root of all evil.\n\t\t-- George Bernard Shaw\n'}}
```

## Development
I use pyenv installed via brew on Max OSX.
Currently developed on
```
» python --version
Python 3.5.1
```

Slack Developer Kit for Python: https://slackapi.github.io/python-slackclient/
