import requests
import os
import time
import wget
import json

UBERDUCK_KEY = os.environ["UBERDUCK_KEY"]
UBERDUCK_SECRET = os.environ["UBERDUCK_SECRET"]

speaker = 'jayz'
poem = "This is just a test."

def uberduck(speaker, poem, filename):
    r = requests.post("https://api.uberduck.ai/speak",
            auth=(UBERDUCK_KEY, UBERDUCK_SECRET),
            data=json.dumps({"speech": poem, "voice": speaker, "pace": 0.7})
            )
    print(r)
    print(r.json())

    response_uuid = r.json()['uuid']

    while True:
        print('sleeping')
        time.sleep(5)
        poll = requests.get("https://api.uberduck.ai/speak-status",
                auth=(UBERDUCK_KEY, UBERDUCK_SECRET),
                params=r.json(),
                )
        download_link = poll.json()['path']
        print(download_link)
        if download_link:
            break

    output_dir = "outputs"
    wget.download(download_link, out=output_dir)
    os.rename(output_dir + '/audio.wav', output_dir + '/' + filename)
    print(filename)

if __name__ == '__main__':
    poem = """A different universe, a hundred trillion stars
Are burning, shining, planets whirling round them
But none shines brighter than the sun.
        I'm just a speck of dust on an orb circling that star,
A tiny spark in the vastness of space
But if you look close enough you'll see me.

        I'm wandering the stars tonight."""
    # d = {"speech": poem, "voice": speaker}
    # print(repr(json.dumps(d)))
    uberduck(speaker, poem)