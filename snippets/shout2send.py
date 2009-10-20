#!/usr/bin/python
import gconf
import gst
import gtk
import gtk.glade
import rb

_GCONF_KEY = '/apps/rhythmbox/plugins/shout2send/%s'
_GST_BIN = ('audioresample ! audioconvert ! vorbisenc ! oggmux ! shout2send '
            'mount=%(mount)s port=%(port)d password=%(password)s ip=%(ip)s')


class shout2send(rb.Plugin):

  def __init__(self):
    rb.Plugin.__init__(self)
    self.read_gconf()
    print 'Ready to stream.'

  def read_gconf(self):
    self.client = gconf.client_get_default()
    self.mount = self.client.get_string(_GCONF_KEY % 'mount') or '/stream.ogg'
    self.ip = self.client.get_string(_GCONF_KEY % 'ip') or '127.0.0.1'
    self.port = self.client.get_int(_GCONF_KEY % 'port') or 8000
    self.password = self.client.get_string(_GCONF_KEY % 'password') or 'hackme'

  def build_sink(self):
    config = {
        'mount': self.mount,
        'ip': self.ip,
        'port': self.port,
        'password': self.password
        }
    print 'Sink config:\n%s' % config
    self.sink = gst.parse_bin_from_description(_GST_BIN % config, True)
    print 'Built sink.'

  def add_sink(self):
    self.build_sink()
    self.shell.get_player().props.player.add_tee(self.sink)

  def remove_sink(self):
    self.shell.get_player().props.player.remove_tee(self.sink)

  def activate(self, shell):
    self.shell = shell
    self.add_sink()
    print 'Added tee.'

  def deactivate(self, shell):
    self.shell = shell
    self.remove_sink()
    print 'Removed tee.'

  def create_configure_dialog(self, dialog=None):
    if dialog is None:
      self.glade_file = self.find_file('shout2send.glade')
      self.glade_xml = gtk.glade.XML(self.glade_file)
      self.mount_entry = self.glade_xml.get_widget('entry1')
      self.ip_entry = self.glade_xml.get_widget('entry2')
      self.port_entry = self.glade_xml.get_widget('entry3')
      self.password_entry = self.glade_xml.get_widget('entry4')
      dialog = self.glade_xml.get_widget('preference')
      dialog.connect('response', self.dialog_response)
    self.mount_entry.set_text(self.mount)
    self.ip_entry.set_text(self.ip)
    self.port_entry.set_text(str(self.port))
    self.password_entry.set_text(self.password)
    dialog.present()
    return dialog

  def dialog_response(self, dialog, response):
    if response == gtk.RESPONSE_OK:
      self.client.set_string(_GCONF_KEY % 'mount', self.mount_entry.get_text())
      self.client.set_string(_GCONF_KEY % 'ip', self.ip_entry.get_text())
      self.client.set_int(_GCONF_KEY % 'port', int(self.port_entry.get_text()))
      self.client.set_string(_GCONF_KEY % 'password',
                             self.password_entry.get_text())
      self.read_gconf()
      self.remove_sink()
      self.add_sink()
      dialog.hide()
      print 'Saved changes.'
    elif response in (gtk.RESPONSE_CANCEL, gtk.RESPONSE_DELETE_EVENT):
      dialog.hide()
      print 'Canceled.'
    else:
      print 'Unknown response.'
