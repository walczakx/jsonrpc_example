import os
import sys

try:
    this = __file__
except NameError:
    this = sys.argv[0]

root_dir = os.path.abspath(os.path.dirname(this))
sys.path.insert(0, os.path.join(root_dir, '3rdparty'))
os.environ["PATH"] += ":" + root_dir + '/3rdparty'


BROWSER_WIDTH=1680
BROWSER_HEIGHT=1050
