import gst
import gobject

#http://www.jejik.com/articles/2007/01/streaming_audio_over_tcp_with_python-gstreamer/

def OnDynamicPad(dbin, pad, islast):
    print "OnDynamicPad Called!"
    #pad.link(self.convert.get_pad("sink"))


playbin = gst.element_factory_make("playbin2")
fakesink = gst.element_factory_make("fakesink")

shout2send = gst.element_factory_make('shout2send')
shout2send.set_property('mount', 'stream.ogg')
shout2send.set_property('ip', '192.168.1.150')
shout2send.set_property('port', 8000)
shout2send.set_property('password', 'hackmePbq11Kz')
#shout2send.set_property('streamname', 'test')
#shout2send.set_property('description', 'tester')
#shout2send.set_property('genre', 'random')

#gst-inspect-0.10 shout2send
sink_string = 'audioresample ! audioconvert ! vorbisenc ! oggmux ! shout2send mount = test.ogg ip=192.168.1.150 port=8000 password=hackmePbq11Kz'
sink = gst.parse_bin_from_description(sink_string, True)
shout2send = sink.get_by_name('shout2send1')
shout2send.set_property('streamname', 'tester')

for i in sink.elements():
    print i
exit(2)

playbin.set_property("video-sink", fakesink)
playbin.set_property("audio-sink", sink)

filepath = '/home/leon/Documents/My Documents/Text Documents/prive/25 jarig huwelijk/Creedence Clearwater Revival - All Time Greatest Hits (CD 1) - 02 - Bad Moon Rising.ogg'
filepath = '/home/leon/Downloads/HITZONE 46 NLT release/DISC 1/17 - DE JEUGD VAN TEGENWOORDIG - HOLLEREER.mp3'
playbin.set_property('uri', 'file://' + filepath)
playbin.set_state(gst.STATE_PLAYING)
 
# enter into a mainloop
loop = gobject.MainLoop()
loop.run()

