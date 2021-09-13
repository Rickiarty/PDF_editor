#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
 * 
 *  Coded by Rei-Chi Lin 
 * 
"""

from PdfEditor.PdfLib.pdf_wrapper import PdfFileReaderWrapper, PdfFileWriterWrapper, PdfFileWrapper

class PdfManipulator:
    _r_pdf_list = None # PDF reader wrapper objects
    _w_pdf_list = None # PDF writer wrapper objects
    
    def __init__(self):
        self._r_pdf_list = []
        self._w_pdf_list = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    def close(self):
        for pdf_obj in self._r_pdf_list:
            if pdf_obj != None:
                pdf_obj.close()

    @property
    def r_pdf_list(self):
        return self._r_pdf_list
    @property
    def w_pdf_list(self):
        return self._w_pdf_list

    def r_append_to_list_at_last(self, pdf_wrapper_obj):
        self._r_pdf_list.append(pdf_wrapper_obj)
    def w_append_to_list_at_last(self, pdf_wrapper_obj):
        self._w_pdf_list.append(pdf_wrapper_obj)

    def split_one_to_multiple(self, loc, page_num): # SPLIT
        try:
            writer = None
            num_pages = self._r_pdf_list[loc].pdf_reader_obj.getNumPages()
            last_num = 0 # page 1
            non_repeated = set(page_num) # to remove duplicate element(s) from original list by using a set
            page_num = [elem for elem in non_repeated] # 'list comprehension' in Python
            page_num = sorted(page_num) # to sort the list without duplicate elements

            for pn in page_num:
                if pn < num_pages:
                    writer = PdfFileWriterWrapper("p" + str(last_num+1) + "-p" + str(pn) + '.pdf')
                    for i in range(last_num, pn):
                        page = self._r_pdf_list[loc].pdf_reader_obj.getPage(i)
                        writer.pdf_writer_obj.addPage(page)
                    self._w_pdf_list.append(writer)
                    last_num = pn
            
            if last_num < num_pages:
                writer = PdfFileWriterWrapper("p" + str(last_num+1) + '-p' + str(num_pages) + ".pdf")
                for i in range(last_num, num_pages):
                    page = self._r_pdf_list[loc].pdf_reader_obj.getPage(i)
                    writer.pdf_writer_obj.addPage(page)
                self._w_pdf_list.append(writer)
            
            return None
        except Exception as ex:
            return ex

    def merge_multiple_to_one(self): # MERGE
        try:
            self._w_pdf_list.append(PdfFileWriterWrapper('Merged.pdf'))
            for pdf_obj in self._r_pdf_list:
                num_pages = pdf_obj.pdf_reader_obj.getNumPages()
                for i in range(num_pages):
                    page = pdf_obj.pdf_reader_obj.getPage(i)
                    self._w_pdf_list[0].pdf_writer_obj.addPage(page)
            return None
        except Exception as ex:
            return ex

    def r_clear_list(self):
        for pdf_obj in self._r_pdf_list:
            if pdf_obj != None:
                pdf_obj.close()
        self._r_pdf_list = []
    def w_clear_list(self):
        self._w_pdf_list = []
    
    def r_delete_pdf_at(self, loc):
        pdf_obj = self._r_pdf_list.pop(loc)
        if pdf_obj != None:
            pdf_obj.close()
    def w_delete_pdf_at(self, loc):
        pdf_obj = self._w_pdf_list.pop(loc)

    def read_pdf_from(self, file_path): # import/read PDF
        try:
            f_path = file_path.replace("\\", "/")
            f_name = f_path.split('/')[-1]
            pdf_obj = PdfFileReaderWrapper(f_name, file_path)
            self.r_append_to_list_at_last(pdf_obj)
            return None
        except Exception as ex:
            return ex

    def write_pdf_to(self, loc, file_path): # export/write PDF
        pdf_writer = self._w_pdf_list[loc].pdf_writer_obj
        try:
            with open(file_path, 'wb') as file:
                pdf_writer.write(file)
            return None
        except Exception as ex:
            return ex

    def r_sort_asc(self):
        self._r_pdf_list.sort(key=PdfFileWrapper.comparator, reverse=False)
    def w_sort_asc(self):
        self._w_pdf_list.sort(key=PdfFileWrapper.comparator, reverse=False)

    def r_sort_desc(self):
        self._r_pdf_list.sort(key=PdfFileWrapper.comparator, reverse=True)
    def w_sort_desc(self):
        self._w_pdf_list.sort(key=PdfFileWrapper.comparator, reverse=True)

    def r_swap(self, loc1, loc2):
        temp = self.r_pdf_list[loc1]
        self.r_pdf_list[loc1] = self.r_pdf_list[loc2]
        self.r_pdf_list[loc2] = temp
    def w_swap(self, loc1, loc2):
        temp = self.w_pdf_list[loc1]
        self.w_pdf_list[loc1] = self.w_pdf_list[loc2]
        self.w_pdf_list[loc2] = temp
