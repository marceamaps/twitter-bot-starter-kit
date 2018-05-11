import datetime
import arpeggio
from authentication import api
from turtle_lang import run_turtle_program

def check_for_mentions():

    last_response = api.user_timeline(count=1) #returns a list of recent statuses
    most_recent_status_id = last_response[0].id #figure out the status_id of our most recent response

    my_latest_mentions = api.mentions_timeline(since_id=most_recent_status_id) #Recognize a tweet that tags @twitter draw box 
    my_latest_mention = my_latest_mentions[0]

    mentioned_status_id =  my_latest_mention.id
    mentioned_text = my_latest_mention.text[14:]
    user_name = my_latest_mention.user.screen_name

    return mentioned_text, mentioned_status_id, user_name


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
program_text, status_id, user_name = check_for_mentions()
print(reply_with_image(status_id, program_text, user_name))

# from pprint import pprint

# mentions = check_for_mentions()
# for ment in mentions:
#     pprint(ment._json)