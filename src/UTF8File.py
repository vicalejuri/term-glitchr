#!/usr/bin/env python

import codecs

class UTF8File(object):
    """ Save data as UTF-8 encoded file """
    path = ''
    file = None
    _old_data = ''

    def __init__(self,path):
        self.path = path
        self.file = file(path, 'r+')

        # Save OLD data (skipping the UTF8HEader, if it has)
        self._old_data = self.file.read()
        if self._old_data[0:3] == codecs.BOM_UTF8:
            print "HAS_BOM"
            self._old_data = self._old_data[3:]

        self.file.write( codecs.BOM_UTF8 )

    def write(self, data ):
        self.file.write( data.encode('utf-8') )

    def read(self):
        return self._old_data

    def close(self):
        self.file.close()


