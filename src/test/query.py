import gobject
gobject.threads_init()
import pygst
pygst.require("0.10")
import gst
import time
import sys

def on_message(self, bus, message):
    pass

def on_about_to_finish(playbin):
    playbin.set_property('uri', 'file:///home/leon/Workspaces/py-icecream/samples/gapless/ogg/07. Beethoven.ogg')

playbin = gst.element_factory_make('playbin2')
fakesink = gst.element_factory_make('fakesink')

playbin.set_property('video-sink', fakesink)

playbin.set_property('uri', 'file:///home/leon/Workspaces/py-icecream/samples/gapless/ogg/06. Beethoven.ogg')

bus = playbin.get_bus()
bus.add_signal_watch()
bus.connect("message", on_message)
playbin.connect('about-to-finish', on_about_to_finish)

for i in playbin.elements():
    print i
exit(2)

playbin.set_state(gst.STATE_PLAYING)

while 1:
    try:
        print playbin.query_position(gst.FORMAT_TIME)[0] / 1000000000
    except:
        print sys.exc_info()
    time.sleep(1)