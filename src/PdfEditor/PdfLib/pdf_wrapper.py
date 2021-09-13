#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
 * 
 *  Coded by Rei-Chi Lin 
 * 
"""

from PyPDF4 import PdfFileWriter, PdfFileReader
from io import BytesIO

class PdfFileWrapper:
    _obj_name = ""
    _file_path = ""

    @property
    def obj_name(self):
        return self._obj_name
    @property
    def file_path(self):
        return self._file_path
    
    @staticmethod
    def comparator(pdf_wrapper_obj):
        return pdf_wrapper_obj.obj_name

class PdfFileReaderWrapper(PdfFileWrapper):
    _pdf_file = None
    _pdf_file_r = None

    def __init__(self, obj_name, file_path):
        self._obj_name = obj_name
        self._file_path = file_path
        self._pdf_file = open(file_path, 'rb')
        self._pdf_file_r = PdfFileReader(self._pdf_file)
    
    def close(self):
        if self._pdf_file != None:
            self._pdf_file.close()
    
    @property
    def pdf_reader_obj(self):
        return self._pdf_file_r

class PdfFileWriterWrapper(PdfFileWrapper):
    _pdf_file_w = None

    def __init__(self, obj_name):
        self._obj_name = obj_name
        self._pdf_file_w = PdfFileWriterExtended()

    @property
    def pdf_writer_obj(self):
        return self._pdf_file_w

class PdfFileWriterExtended(PdfFileWriter):
    '''
    'tsragland' commented on 18 Mar

    Here's a workaround that worked for at least one use case. Maybe it will work for yours.
    The problem seems to be that PdfFileWriter looks for a 'stream' attribute on the PdfFileWriter instance when performing some cleanup steps (_sweepIndirectReferences), and an error occurs because the PdfFileWriter class (as of 1.27.0) has no such attribute. However, that 'stream' attribute isn't referenced again in _sweepIndirectReferences.
    A potentially viable workaround (until a fix for this issue is released) would be to create a wrapper class which extends PdfFileWriter with a 'stream' attribute, with its value set to an instance of BytesIO.
    Use at your own risk. This is simply a workaround, which works in one case, but may or may not work for your case.
    
    original post: https://github.com/claird/PyPDF4/issues/24
    '''
    def __init__(self):
        super().__init__()
        self.stream = BytesIO()
