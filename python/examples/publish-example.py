
import sys
sys.path.append('../')
from Pubnub import Pubnub

## Initiate Class
pubnub = Pubnub( publish_key='demo', subscribe_key='demo', cipher_key='enigma', ssl_on=False )

## Publish Example
info = pubnub.publish({
    'channel' : 'abcd',
    'message' : {
        'some_text' : 'Hello my World'
    }
})
print(info)

info = pubnub.publish({
    'channel' : 'abcd',
    'message' : ['some_text','Hello my World']
})
print(info)

info = pubnub.publish({
    'channel' : 'abcd',
    'message' : "hi ,this is a string"
})
print(info)

info = pubnub.publish({
    'channel' : 'abcd',
    'message' : 1
})
print(info)

info = pubnub.publish({
    'channel' : 'abcd',
    'message' : 2.1
})
print(info)

