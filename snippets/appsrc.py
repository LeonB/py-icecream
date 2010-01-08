import gobject
gobject.threads_init() 
import gst

#http://whispercast.org/trac/browser/trunk/whispermedialib/third-party/gstreamer/gst-plugins-bad/examples/app/appsrc-seekable.c?rev=2

class Progress(object):
    @classmethod
    def set_progress(cls, progress):
        cls.progress = progress

    @classmethod
    def get_progress(cls):
        return cls.progress

    @classmethod
    def file(cls):
        if not hasattr(cls, 'f'):
            cls.f = open('/home/leon/Music/02 Paranoid Android.mp3')
        return cls.f


def on_message(bus, message):
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

def on_about_to_finish(playbin):
    pass

def feed_data(playbin, buffer_size):
    print 'feeding data'
    f = Progress.file()

#    buffer = gst.Buffer('1'*4096)
    buffer = gst.Buffer(f.read(4096))

    playbin.emit('push-buffer', buffer)
    Progress.set_progress(Progress.get_progress() + buffer_size)

def seek_data(playbin, position):
    Progress.set_progress(position)
    return True

def deep_notify_source(bin, orig, params):
#    print bin.get_element(params.name)
    appsrc = orig.get_by_name(params.name)
    appsrc.set_property('stream-type', 1)

    appsrc.connect('need-data', feed_data)
    appsrc.connect('seek-data', seek_data)

playbin = gst.element_factory_make("playbin2")
fakesink = gst.element_factory_make("fakesink")
playbin.set_property("video-sink", fakesink)

playbin.set_property('uri', 'appsrc://')
#playbin.set_property('uri', 'file:///home/leon/Music/02 Paranoid Android.mp3')

bus = playbin.get_bus()
bus.add_signal_watch()
bus.connect("message", on_message)
playbin.connect('about-to-finish', on_about_to_finish)
playbin.connect('deep-notify::source', deep_notify_source)

playbin.set_state(gst.STATE_PLAYING)

# enter into a mainloop
loop = gobject.MainLoop()
loop.run()