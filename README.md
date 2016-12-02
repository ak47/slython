# slython
hacking the slack api with python - because

## SLACK API TOKEN
You need a testing/development token: https://api.slack.com/docs/oauth-test-tokens

## Usage
```
slacking.py -c <channel> -o <operation> [-n <count> -m <message>]
  commands:
    pw - parrot wave
    pwr - parrot wave reverse
    re - random emoji
    eb - emoji bomb
    cms - channel messages (opt arg: -n count - default 5)
    ls - list channels
    msg - send message (-m message)
```

## Development
I use pyenv installed via brew on Max OSX.
Currently developed on
```
» python --version
Python 3.5.1
```

