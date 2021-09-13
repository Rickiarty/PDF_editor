#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
 * 
 *  Coded by Rei-Chi Lin 
 * 
"""

class Window:

    @property
    def version(self):
        return '1.0.0'
    
    @staticmethod
    def sanitize_data(original_str):
        valid_chars = '0123456789,'
        sanitized_str = ''
        for ch in original_str:
            if ch in valid_chars:
                sanitized_str += ch
        return sanitized_str

    @property
    def author(self):
        return 'Rei-chi Lin'
