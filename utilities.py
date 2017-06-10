

import rocket
from uuid import uuid4

def screenshot():
    path = "/home/john/media/pictures/{}.png".format(uuid4())
    print("Saving screenshot to {}...".format(path))
    rocket.screenshot(path)
