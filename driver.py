from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os
import subprocess

import config

from xvfbwrapper import Xvfb


class Driver(object):
    def __init__(self, target):
        self._target = target

    def __getattr__(self, item):
        return getattr(self._target, item)

    def __get__(self):
        return self.driver.driver

    def quit(self):
        return self._target.quit()

class XvfbWrapper(Driver):

    def __init__(self, driver_class, *args, **kwargs):
        self._xvfb = Xvfb(width=1680, height=1050)
        self._xvfb.start()
        super(XvfbWrapper, self).__init__(driver_class(*args, **kwargs))

    def quit(self):
        ret = super(XvfbWrapper, self).quit()
        self._xvfb.stop()
        return ret

class Firefox(Driver):
    def __init__(self):
        target = webdriver.Firefox()
        target.set_window_size(config.BROWSER_WIDTH, config.BROWSER_HEIGHT)
        super(Firefox, self).__init__(target)

def get_driver_class(name):
    if name == 'firefox':
        return Firefox
    else:
        raise Exception("invalid driver: %s" % name)

def create_driver(name, use_xvfb, *args, **kwargs):
    if use_xvfb == True:
        return XvfbWrapper(get_driver_class(name), *args, **kwargs)
    else:
        return get_driver_class(name)(*args, **kwargs)