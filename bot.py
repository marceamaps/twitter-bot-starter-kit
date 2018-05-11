import datetime
import arpeggio
from authentication import api
from turtle_lang import run_turtle_program

def check_for_mentions():

    last_response = api.user_timeline(count=1) #returns a list of recent statuses
    most_recent_status_id = last_response[0].id #figure out the status_id of our most recent response

    my_latest_mentions = api.mentions_timeline(since_id=most_recent_status_id) #Recognize a tweet that tags @twitter draw box 

    for mention in my_latest_mentions:
        mentioned_status_id =  mention.id
        mentioned_text = mention.text[14:]
        user_name = mention.user.screen_name
        reply_with_image(mentioned_status_id, mentioned_text, user_name)


def reply_with_image(status_id, program_text, user_name):

    tagged_user_name = '@'+user_name  
    error_status = tagged_user_name + " Sorry, I could't read that. Try again!"

    try:
        image_file = run_turtle_program(program_text)
        reply_tweet = api.update_with_media(status = tagged_user_name, in_reply_to_status_id=status_id, filename=image_file)

    except arpeggio.NoMatch:
        reply_tweet = api.update_status(status = error_status, in_reply_to_status_id=status_id)

    return reply_tweet

# message = "The turtle movement is {}".format(
#     datetime.datetime.now().strftime('%-I:%m %p'))
# print('posting this clever message to twitter:')
# print(message)

# api.update_with_media(image_file, program)
check_for_mentions()

# from pprint import pprint

# mentions = check_for_mentions()
# for ment in mentions:
#     pprint(ment._json)