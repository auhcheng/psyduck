from generate_poem import generate_poem
from uberduck import uberduck

topics = []
topics = "the 4 elements, finding yourself, friendship".split(', ')
title = input("title: ")
rapper = "nas"

print('writing poem')
poem = generate_poem(topics, title)

print('rapping poem')
uberduck(rapper, poem)