# http://svn.jejik.com/viewvc.cgi/jukebox/jukebox/trunk/audioplayer.py?view=markup
# https://core.fluendo.com/carid/svn/trunk/schroedinger/misc/pydvdrip

import gst
class VorbisencodeBin(gst.Bin):
        """
        An output bin that does:
        queue --> vorbisenc --> oggmux
        maybe add capsfilter??
        """

        def __init__(self):
            gst.Bin.__init__(self)

            self.queue = gst.element_factory_make('queue')
            self.vorbisenc = gst.element_factory_make('vorbisenc')
            self.oggmux = gst.element_factory_make('oggmux')

            self.add(self.queue, self.vorbisenc, self.oggmux)
            gst.element_link_many(self.queue, self.vorbisenc, self.oggmux)

            self.add_pad(gst.GhostPad('sink', self.queue.get_pad("sink")))
            self.add_pad(gst.GhostPad('src', self.oggmux.get_pad("src")))