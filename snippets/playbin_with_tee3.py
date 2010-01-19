import gst
import gobject
import vorbisencode_bin
songs = ['file:///home/leon/Music/18 - bibelebons thema - bibelebons.mp3',
    'file://20 - hallo vriendjes - Bassie en adriaan.mp3']

class Backend(object):
    def __init__(self):
        playbin = gst.element_factory_make("playbin2")
        fakesink = gst.element_factory_make("fakesink")

        sink = gst.element_factory_make('pipeline')
        audioconvert = gst.element_factory_make('audioconvert')
        tee = gst.element_factory_make('tee')
        vb = vorbisencode_bin.VorbisencodeBin()
        inputselector = gst.element_factory_make('input-selector')
        shout2send = gst.parse_bin_from_description('shout2send mount=test.ogg \
        ip=basil port=9000 password=hackmePbq11Kz streamname=test', True)

        sink.add(audioconvert, tee, vb, inputselector, shout2send)
        gst.element_link_many(audioconvert, tee, vb, inputselector, shout2send)
        sink.add_pad(gst.GhostPad('sink', audioconvert.get_pad("sink")))

        #sink gaat erin
        #src komt eruit
        #dus tee heeft 2 sources
        #dus inputselector heeft twee sinks
        vb2 = vorbisencode_bin.VorbisencodeBin()
        sink.add(vb2)
        tee.link(vb2)
        vb2.link(inputselector)

        playbin.set_property("video-sink", fakesink)
        playbin.set_property("audio-sink", sink)

        for i in tee.pads():
            print i
        for i in inputselector.pads():
            print i

        playbin.set_property('uri', songs[0])
        playbin.set_state(gst.STATE_PLAYING)

b = Backend()

## enter into a mainloop
loop = gobject.MainLoop()
loop.run()