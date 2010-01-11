import string
import gobject
gobject.threads_init()
import gst
import re


#@TODO: look into the posibilities of gst_controller:
# * http://gstreamer.freedesktop.org/data/doc/gstreamer/head/manual/html/section-dparams-parameters.html
# * http://www.google.nl/search?hl=nl&client=firefox-a&rls=com.ubuntu%3Aen-US%3Aofficial&q=gstreamer+python++query+position&btnG=Zoeken&meta=&aq=f&oq=
# * http://pygstdocs.berlios.de/pygst-reference/index.html

class Backend(object):

    def __init__(self, stream):
        self.stream = stream
        self.playbin = None

    def construct_pipeline(self):
        //http://svn.jejik.com/viewvc.cgi/jukebox/jukebox/trunk/audioplayer.py?view=markup

        playbin = self.playbin = gst.element_factory_make('playbin2')
        fakesink = gst.element_factory_make('fakesink')

        sink_description = string.Template('vorbisenc ! oggmux ! \
            shout2send sync=0 mount=${mount} ip=${ip} port=${port} \
            password=${password} streamname="${name}" description="${description}"')
#        sink_description = string.Template('lame vbr=4 ! \
#            shout2send mount=${mount} ip=${ip} port=${port} \
#            password=${password} streamname="${name}" description="${description}"')
#        sink_description = string.Template('alsasink')

        sink_description = sink_description.substitute(
            mount = self.stream.server.mount,
            ip = self.stream.server.host,
            port = self.stream.server.port,
            password = self.stream.server.password,
            name = self.stream.name,
            description = self.stream.description
        )

        sink = gst.parse_bin_from_description(sink_description, True)

        playbin.set_property('video-sink', fakesink)
        playbin.set_property('audio-sink', sink)

        bus = playbin.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        playbin.connect('about-to-finish', self.on_about_to_finish)

    def play(self):
        if not self.playbin:
            self.construct_pipeline()

        self.playbin.set_property('uri', self.uri)
        self.playbin.set_state(gst.STATE_PLAYING)
        self.stream.hooks.source.call('start_play', self.playbin.get_property('uri'))
    
    def on_message(self, bus, message):
        t = message.type

        if t == gst.MESSAGE_EOS:
            self.playbin.set_state(gst.STATE_READY)

            #Callbacks
            self.stream.hooks.source.call('eof', self.playbin.get_property('uri'))
            self.stream.hooks.stream.call('eos')
            self.stream.stop()

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
        try:
            old_uri = self.uri
            new_uri = self.uri = self.stream.source.get()
        except Exception:
            new_uri = self.uri = 'file://%s' % self.stream.interval_sound

        sink_description = string.Template('vorbisenc ! oggmux ! \
            shout2send mount=${mount} ip=${ip} port=${port} \
            password=${password} streamname="${name}" description="${description}"')

        sink_description = sink_description.substitute(
            mount = self.stream.server.mount,
            ip = self.stream.server.host,
            port = self.stream.server.port,
            password = self.stream.server.password,
            name = self.stream.name,
            description = self.stream.description
        )

        sink = gst.parse_bin_from_description(sink_description, True)

        playbin.set_property('audio-sink', sink)
        self.playbin = playbin

        playbin.set_property('uri', new_uri)
        playbin.set_state(gst.STATE_PLAYING)
        self.stream.hooks.source.call('transition', old_uri, new_uri)
        self.stream.hooks.source.call('eof', old_uri)
        self.stream.hooks.source.call('start_play', new_uri)

    def query_duration(self):
        return self.playbin.query_duration(gst.FORMAT_TIME)[0] / 1000000000

    def query_position(self):
        try:
            for i in self.playbin.elements():
                name = i.get_name()
                if re.search('^playbin2inputselector[0-9]*$', name):
                    return i.query_position(gst.FORMAT_TIME)[0] / 1000000000
        except TypeError, e:
            pass

        return 0