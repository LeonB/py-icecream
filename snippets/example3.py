import gst
import gobject

def on_message(bus, message):
    t = message.type
    if t == gst.MESSAGE_EOS:
        print message
    elif t == gst.MESSAGE_ERROR:
        err, debug = message.parse_error()
        print "Error: %s" % err, debug 

#pipeline = gst.Pipeline('py-ice')
#source = gst.element_factory_make("filesrc")
#convert = gst.element_factory_make("audioconvert")
#vorbisenc = gst.element_factory_make('vorbisenc')
#oggmux = gst.element_factory_make('oggmux')

playbin = gst.element_factory_make("playbin2")
fakesink = gst.element_factory_make("fakesink")

shout2send = gst.element_factory_make('shout2send')
shout2send.set_property('mount', 'stream.ogg')
shout2send.set_property('port', 8000)
shout2send.set_property('password', 'hackmePbq11Kz')
shout2send.set_property('ip', 'basil')
shout2send.set_property('streamname', 'test')
shout2send.set_property('description', 'tester')
shout2send.set_property('genre', 'random')

#pipeline.add(source, convert, vorbisenc, oggmux)
#gst.element_link_many(source, convert, vorbisenc, oggmux)

#bus = pipeline.get_bus()
#bus.add_signal_watch()
#bus.connect("message", on_message)

playbin.set_property("video-sink", fakesink)
playbin.set_property("audio-sink", shout2send)

bus = playbin.get_bus()
bus.add_signal_watch()
bus.connect("message", on_message)
#self.playbin.connect('about-to-finish', self.on_about_to_finish)

#filepath = '/home/leon/Music/albums/P/Pink Floyd/A Collection of Great Dance Songs/06 Another Brick in the Wall, Part 2.flac'
filepath = '/home/leon/Documents/My Documents/Text Documents/prive/25 jarig huwelijk/Creedence Clearwater Revival - All Time Greatest Hits (CD 1) - 02 - Bad Moon Rising.ogg'
#filepath = '/home/leon/Workspaces/pmpd/samples/gapless/wav/17. Beethoven.wav'
#source.set_property("location", filepath)

#pipeline.set_state(gst.STATE_PLAYING)
playbin.set_property('uri', 'file://' + filepath)
playbin.set_state(gst.STATE_PLAYING)
 
# enter into a mainloop
loop = gobject.MainLoop()
loop.run()

