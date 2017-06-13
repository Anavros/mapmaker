
import rocket
from uuid import uuid4
import os
import pickle


n = 0
sequence_directory = None
root = "/home/john/media/pictures/"


def screenshot(path=None):
    if path is None:
        path = root + "{}.png".format(uuid4())
    print("Saving screenshot to {}...".format(path))
    rocket.screenshot(path)


def screenshot_sequence():
    global sequence_directory, n
    if sequence_directory is None:
        sequence_directory = root + "{}/".format(uuid4())
        os.mkdir(sequence_directory)
    path = sequence_directory + "{}.png".format(n)
    screenshot(path)
    n += 1


def save_app(app):
    print("Saving world to 'world.pickle'...")
    pickle.dump(app, open('world.pickle', 'wb'))


def load_app(path):
    return pickle.load(open(path, 'rb'))
