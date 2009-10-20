import gst
import gobject

#http://www.jejik.com/articles/2007/01/streaming_audio_over_tcp_with_python-gstreamer/

playbin = gst.element_factory_make("playbin2")
fakesink = gst.element_factory_make("fakesink")

audioresample = gst.element_factory_make('audioresample')
audioconvert = gst.element_factory_make('audioconvert')
vorbisenc = gst.element_factory_make('vorbisenc')
oggmux = gst.element_factory_make('oggmux')
shout2send = gst.element_factory_make('shout2send')

shout2send.set_property('mount', 'stream.ogg')
shout2send.set_property('ip', '192.168.1.150')
shout2send.set_property('port', 8000)
shout2send.set_property('password', 'hackmePbq11Kz')

'audioresample ! audioconvert ! vorbisenc ! oggmux ! shout2send'
sink = gst.element_factory_make('bin')
sink.add(audioresample, audioconvert, vorbisenc, oggmux, shout2send)
gst.element_link_many(audioresample, audioconvert, vorbisenc, oggmux, shout2send)

#Voodoo
sinkpad = audioresample.get_static_pad("sink")
sink.add_pad(gst.GhostPad('sink', sinkpad)i)

playbin.set_property("video-sink", fakesink)
playbin.set_property("audio-sink", sink)

filepath = '/home/leon/Documents/My Documents/Text Documents/prive/25 jarig huwelijk/Creedence Clearwater Revival - All Time Greatest Hits (CD 1) - 02 - Bad Moon Rising.ogg'
#filepath = '/home/leon/Downloads/HITZONE 46 NLT release/DISC 1/17 - DE JEUGD VAN TEGENWOORDIG - HOLLEREER.mp3'
playbin.set_property('uri', 'file://' + filepath)
playbin.set_state(gst.STATE_PLAYING)
 
# enter into a mainloop
loop = gobject.MainLoop()
loop.run()

#errors:
#Could not find a compatible pad to link to volume:src
#playsink gstplaysink.c:1052:gen_audio_chain:<playsink0> error: Failed to configure the audio sink.
