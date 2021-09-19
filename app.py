from generate_poem import generate_poem
from uberduck import uberduck
from datetime import datetime
import uuid
import sound
import sys
import clip_music_video.vid_gen as vid_gen
import email_send
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, jsonify, request
from flask_restful import Resource, Api


print("starting up")
def music_video_generation(title):
    ID = uuid.uuid4().hex
    bg_music_path = ""

    topics = []
    topics = "the 4 elements, finding yourself, friendship".split(', ')
    # title = input("title: ")
    rapper_name = "nas"

    print('writing poem')
    poem = generate_poem(topics, title)

    print('rapping poem')
    uberduck(rapper_name, poem, filename="" + ID + '-duck.wav')

    # poem = "\nit's still summer, even if it feels like fall. i've got the fan on high.\n\n\tii.this room has no windows, so there's no way to know if it's day or night. i've turned off the radio, too; no use knowing what's going on outside this cage.\n\n\tiii.they took my clock away, but i can hear bells ringing across town; i can't tell if they're coming from churches or schools or factories; they're just bells; one long ring after another until their hands touch down on one of those ivy-covered walls and come to a stop. all the birds are asleep"

    # Generating timing sheet
    vocal_length = sound.get_length("./outputs/"+ ID +'-duck.wav')
    # vocal_length = sound.get_length('./outputs/a343e28d6ca149f69bf276e970468f8b-duck.wav')
    poem_ls = poem.strip().split()
    add = float(vocal_length)/float(len(poem_ls)/7)
    count = 0
    timer = 0.0
    default = sys.stdout

    with open('./outputs/' + ID +'-lyrics.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(datetime.fromtimestamp(int(timer)).strftime("%M:%S"), end=' ')
        for s in poem_ls:
            if count == 6:
                count = 0
                timer+=add
                print("\n" + datetime.fromtimestamp(int(timer)).strftime("%M:%S"), end=' ')
            else:
                print(s, end = " ")
                count += 1

    sys.stdout = default
    # sentiment analysis to set the background music
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(poem)
    dom_score = max(scores, key=scores.get)
    if dom_score == "pos":
        bg_music_path = "pos_bg_music.wav"
    elif dom_score == "neu":
        bg_music_path = "neu_bg_music.wav"
    else:
        bg_music_path = "neg_bg_music.wav"

    sound.add_background("./outputs/"+ ID +'-duck.wav',  bg_music_path, ID)
    vid_gen.generate_video(50, "./outputs/"+ ID + "-lyrics.txt", "./outputs/" + ID + "-final_music.wav", ID)

    return ID


# --------------------------------API CREATION--------------------------------------

# Creating the flask app and api
app = Flask(__name__)
api = Api(app)

@app.route('/submit', methods=['GET', 'POST'])
def parse_request():
    title = request.form.get('title')  # data is empty
    email = request.form.get('email')
    ID = music_video_generation(title)

    # WILL PROBABLY CHANGE
    email_send.send_email(email, "./frontend/public/FinalClips/"+ID+"-finaloutput.mp4")
    return "Request recieved!"

# driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0')