from callback_method import *

class App(object):

    def __init__(self):
        self.boot()

    @callback_method
    def boot(self):
        self.setup_config()
        self.setup_logger()
        self.setup_callbacks()
        self.load_plugins()

    @callback_method
    def setup_config(self):
        self.config = Config()

    @callback_method
    def setup_logger(self):
        self.log = Logger(self.config.log)

    @callback_method
    def setup_callbacks(self):
        from player import Player
        
        callbacks.RegisterCallback(Player, 'stop',
            PermanentCallback(lambda p: self.log.debug('Stopping.....')))

    def load_plugins(self):
        callbacks.RunCallbackChain(Server, 'before_loading_plugins', self)

        for plugin in self.config.plugins:
            exec('from plugins import %s' % plugin)

    @callback_method
    def run(self):
        gobject.threads_init()
        self.loop = gobject.MainLoop()
        self.log.debug('running....')
        
        try:
            self.loop.run()
        except (KeyboardInterrupt, SystemExit):
            print 'shutting down...'
            raise
        except Exception:
            self.log.critical(Exception)
        finally:
            self.stop()

    @callback_method
    def stop(self):
        self.loop.quit()
