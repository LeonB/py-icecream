#!/usr/bin/env python

#          |--queue--vorbisenc--oggmux--|
#playbin --|                            |--inputselector--shout2send
#          |--queue--vorbisenc--oggmux--|

import gst
import gobject
songs = ['file:///home/leon/Music/18 - bibelebons thema - bibelebons.mp3',
    'file://20 - hallo vriendjes - Bassie en adriaan.mp3']

class Backend(object):
    def __init__(self):
        playbin = gst.element_factory_make("playbin2")
        fakesink = gst.element_factory_make("fakesink")

#        shout2send = gst.element_factory_make('shout2send')
#        shout2send.set_property('mount', 'stream.ogg')
#        shout2send.set_property('ip', 'basil')
#        shout2send.set_property('port', 9000)
#        shout2send.set_property('password', 'hackmePbq11Kz')
#        shout2send.set_property('streamname', 'test')
#        shout2send.set_property('description', 'tester')
#        shout2send.set_property('genre', 'random')
#
#        alsasink = gst.element_factory_make('alsasink')
#
#        sink = gst.element_factory_make('bin')
#
#        tee = gst.element_factory_make('tee')
#        q1 = gst.element_factory_make('queue')
#        q2 = gst.element_factory_make('queue')
#
#        g1 = gst.GhostPad("sink1", q1.get_pad('sink'))
#        g2 = gst.GhostPad("sink2", q2.get_pad('sink'))
#
#        ve1 = gst.element_factory_make('vorbisenc')
#        ve2 = gst.element_factory_make('vorbisenc')
#        om1 = gst.element_factory_make('oggmux')
#        om2 = gst.element_factory_make('oggmux')
#        a1 = gst.element_factory_make('adder')
#        a2 = gst.element_factory_make('adder')
#        ins = gst.element_factory_make('input-selector')


#        sink.add(tee, ve1, ve2, om1, om2, ins, alsasink)
#        sink.add(tee, q1, a1, ins, alsasink)

#        q1.get_pad('src').link(tee.get_pad('sink'))
#        ins.get_pad('src').link(q1.get_pad('sink'))
#        ins.get_pad('src').link(q1.get_pad('sink'))

#        g = gst.GhostPad("src", q1.get_pad('src'))
#        alsasink.add_pad(g)

#        sink = gst.parse_bin_from_description('tee ! queue ! input-selector ! alsasink', True)

        t = gst.element_factory_make('tee')
        q1 = gst.element_factory_make('queue')
        q2 = gst.element_factory_make('queue')
        i = gst.element_factory_make('input-selector')
        a = gst.element_factory_make('alsasink')

        sink = gst.element_factory_make('bin')
        sink = gst.Pipeline()
        sink.add(t, q1, q2, i, a)
        t.link(q1)
        t.link(q2)
        q1.link(i)
        q2.link(i)
        i.link(a)

        sink.add_pad(gst.GhostPad("sink", t.get_pad("sink")))
        
        playbin.set_property("video-sink", fakesink)
        playbin.set_property("audio-sink", sink)

        playbin.set_property('uri', songs[0])
        playbin.set_state(gst.STATE_PLAYING)
        self.i = i

#        for i in playbin.elements():
#        print playbin.get_by_name('playsink0')
#        for i in playbin.get_by_name('playsink0').elements():
#            print i
#        exit(2)

b = Backend()

## enter into a mainloop
import time
while 1:
    time.sleep(1)
    ap = b.i.get_property('active-pad')
    print ap
    for i in b.i.pads():
        print i
#    b.i.set_property('active-pad', b.i.get_pad('sink0'))
    b.i.remove_pad(b.i.get_pad('sink0'))
#    if ap == b.i.get_by_name('sink1'):
#        b.i.set_property('active-pad', b.i.get_by_name('sink0'))
#    elif ap == b.i.get_by_name('sink0'):
#        b.i.set_property('active-pad', b.i.get_by_name('sink1'))

loop = gobject.MainLoop()
loop.run()