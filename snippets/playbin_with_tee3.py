import gst
import gobject
import vorbisencode_bin

songs = [
    'file:///home/leon/Workspaces/py-icecream/samples/gapless/ogg/10. Beethoven.ogg',
    'file:///home/leon/Workspaces/py-icecream/samples/gapless/ogg/11. Beethoven.ogg',
    '',
]

class Backend(object):
    def __init__(self):
        self.playbin = playbin = gst.element_factory_make("playbin2")
        fakesink = gst.element_factory_make("fakesink")

        self.sink = sink = gst.element_factory_make('pipeline')
        audioconvert = gst.element_factory_make('audioconvert')
        self.tee = tee = gst.element_factory_make('tee')

        self.vb0 = vb0 = vorbisencode_bin.VorbisencodeBin()
        self.vb1 = vb1 = vorbisencode_bin.VorbisencodeBin()

        self.inputselector = inputselector = gst.element_factory_make('input-selector')
        shout2send = gst.parse_bin_from_description('shout2send mount=test.ogg \
        ip=basil port=9000 password=hackmePbq11Kz streamname=test', True)

        sink.add(audioconvert, tee, vb0, inputselector, shout2send)
        gst.element_link_many(audioconvert, tee, vb0, inputselector, shout2send)

        sink.add(vb1)
        gst.element_link_many(tee, vb1, inputselector)

        self.tee.get_pad('src0').set_active(True)
        self.tee.get_pad('src1').set_active(False)

        self.inputselector.set_property('active-pad', self.inputselector.get_pad('sink0'))

        sink.add_pad(gst.GhostPad('sink', audioconvert.get_pad("sink")))

        bus = playbin.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        playbin.connect('about-to-finish', self.on_about_to_finish)

        playbin.set_property("video-sink", fakesink)
        playbin.set_property("audio-sink", sink)

        playbin.set_property('uri', songs[1])
        playbin.set_state(gst.STATE_PLAYING)

    def on_message(self, bus, message):
        t = message.type

        if t == gst.MESSAGE_EOS:
            print 'stopped gstreamer'
        elif t == gst.MESSAGE_ERROR:
            print message
            print 'error!'
        elif t == gst.MESSAGE_STATE_CHANGED:
            pass
        else:
            pass

    def on_about_to_finish(self, playbin):
        print 'about to finish'

        self.tee.get_pad('src0').set_blocked_async(True, self.set_blocked)

        if self.playbin.get_property('uri') == songs[0]:
            self.playbin.set_property('uri', songs[1])
        else:
            self.playbin.set_property('uri', songs[0])

    def set_blocked(self, pad, block):
        print 'Setting blocked'

        self.tee.get_pad('src0').set_active(False)
        self.tee.get_pad('src1').set_active(True)

        self.sink.unlink(self.vb0)
        self.sink.set_state(gst.STATE_NULL)
        self.sink.remove(self.vb0)

        self.tee.remove_pad(self.tee.get_pad('src0'))
        self.inputselector.remove_pad(self.inputselector.get_pad('sink0'))
        self.inputselector.set_property('active-pad', self.inputselector.get_pad('sink1'))

        self.tee.get_pad('src0').set_blocked(False)

b = Backend()

## enter into a mainloop
loop = gobject.MainLoop()
loop.run()