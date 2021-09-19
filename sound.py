from pydub import AudioSegment
from random import random

# inputs are all paths
def combine_audio(rap_track, background, id):
    rap_track_seg = AudioSegment.from_wav(rap_track)
    # background_seg = AudioSegment.from_wav(background)
    background_seg = background - 4
    output = rap_track_seg.overlay(background_seg)
    output.export("./outputs/" + id + "-final_music.wav", format="wav")

def extract_background(rap_track, long_background, id):
    rap_track_seg = AudioSegment.from_wav(rap_track)
    long_background_seg = AudioSegment.from_wav(long_background)
    rap_track_duration = rap_track_seg.duration_seconds
    long_background_duration = long_background_seg.duration_seconds
    rand = random()*(long_background_duration-rap_track_duration)*1000
    short_background = long_background_seg[rand:rand + rap_track_duration*1000]
    short_background.export(id + "-bg_music.wav", format="wav")
    return short_background

def add_background(rap_track, background, id):
    short_background = extract_background(rap_track, background,id)
    combine_audio(rap_track, short_background, id)


def get_length(audio):
    return AudioSegment.from_wav(audio).duration_seconds
# combine_audio("./music_generation/shortRap.wav","./outputs/audio (1).wav")
