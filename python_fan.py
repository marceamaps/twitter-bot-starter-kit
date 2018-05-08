import tweepy
from authentication import api

class PythonFanListener(tweepy.StreamListener):
    def on_connect(self):
        print('Ready to rumble!!')
    def on_status(self, status):
        print ('just received a status:\n  ', status.text)

myStream = tweepy.Stream(auth = api.auth, listener=PythonFanListener())

myStream.filter(track=['python'])
