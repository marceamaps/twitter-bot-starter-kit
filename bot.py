import datetime
from authentication import api
from turtle_lang import run_turtle_program

def reply_with_image(status_id, program)
    """
    When called with a status_id, and a program:

    try to run the program.
    if it errors:
        say, "Sorry, I couldn't understand that..."
    if it succeeds:
        reply with the image.

        #image_file section and api.update_with_media will also be a part of this function
    """

program = '''
forward 10
maybe 0.6
  color red
end maybe
right 90
forward 100
'''

image_file = run_turtle_program(program)

message = "The turtle movement is {}".format(
    datetime.datetime.now().strftime('%-I:%m %p'))
print('posting this clever message to twitter:')
print(message)

api.update_with_media(image_file, program)

print('success!')
