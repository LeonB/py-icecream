#What should this do?
# create a playbin element
# replace filesrc by appsrc/fdsrc
#
# Remove element:http://gtk2-perl.sourceforge.net/doc/pod/GStreamer/Bin.html
# Plugins:http://gstreamer.freedesktop.org/documentation/plugins.html
# appsrc:http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-appsrc.html
# fdsrc:http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-plugins/html/gstreamer-plugins-fdsrc.html 
# appsrc example:http://webcvs.freedesktop.org/gstreamer/gst-plugins-bad/examples/app/appsrc_ex.c?view=markup
# example:http://www.nabble.com/appsrc,-random-crash-td25039676.html 

import gst
import gobject

playbin = gst.element_factory_make("playbin2")
fakesink = gst.element_factory_make("fakesink")
playbin.set_property("video-sink", fakesink)

#gst-inspect-0.10 shout2send
#sink_string = 'audioresample ! audioconvert ! vorbisenc ! oggmux ! shout2send mount = test.ogg ip=192.168.1.150 port=8000 password=hackmePbq11Kz'
#sink = gst.parse_bin_from_description(sink_string, True)
#shout2send = sink.get_by_name('shout2send1')
#shout2send.set_property('streamname', 'tester')

#@TODO: use decodebin2!

#remove filesrc element
playsink = playbin.get_by_name('playsink0')
for i in playbin.elements():
    print i
exit(2)

print filesrc
exit(2)

#playbin.set_property("audio-sink", sink)

#filepath = '/home/leon/Documents/My Documents/Text Documents/prive/25 jarig huwelijk/Creedence Clearwater Revival - All Time Greatest Hits (CD 1) - 02 - Bad Moon Rising.ogg'
#filepath = '/home/leon/Downloads/HITZONE 46 NLT release/DISC 1/17 - DE JEUGD VAN TEGENWOORDIG - HOLLEREER.mp3'
#playbin.set_property('uri', 'file://' + filepath)
#playbin.set_state(gst.STATE_PLAYING)
 
# enter into a mainloop
loop = gobject.MainLoop()
loop.run()

class Tester(object):
    def lalaala(self):
        pass

class Tester2(object):
    def toests(self):
        pass

t = Tester()
t.lalaala()
t2 = Tester2()