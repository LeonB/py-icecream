import string
import gobject
gobject.threads_init()
import gst

#@TODO: look into the posibilities of gst_controller:

class Backend(object):

    def __init__(self, stream):
        self.stream = stream

    def construct_pipeline(self):
        playbin = self.playbin = gst.element_factory_make('playbin2')
        fakesink = gst.element_factory_make('fakesink')

        sink_description = string.Template('vorbisenc ! oggmux ! \
            shout2send mount=${mount} ip=${ip} port=${port} \
            password=${password}')

        sink_description = sink_description.substitute(
            mount = self.stream.server.mount,
            ip = self.stream.server.host,
            port = self.stream.server.port,
            password = self.stream.server.password,
        )

        sink = gst.parse_bin_from_description(sink_description, True)

        playbin.set_property('video-sink', fakesink)
        playbin.set_property('audio-sink', sink)

        playbin.set_property('uri', self.uri)

        bus = playbin.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        playbin.connect('about-to-finish', self.on_about_to_finish)

    def play(self):
        self.construct_pipeline()
        self.playbin.set_state(gst.STATE_PLAYING)
    
    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.playbin.set_state(gst.STATE_NULL)
            #self.loop.quit()
            print 'stopped gstreamer'
        elif t == gst.MESSAGE_ERROR:
            print message
            print 'error!'
            #self.loop.quit()
        elif t == gst.MESSAGE_STATE_CHANGED:
            pass
        else:
            pass

    def on_about_to_finish(self, playbin):
        self.uri = self.stream.source.get()
        self.playbin.set_property('uri', self.uri)
