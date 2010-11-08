'''
Created on Nov 7, 2010

@author: alendit
'''
from pylons import session

__all__ = ['_assert_in']

def _assert_in(arguments, response):
    '''Takes a list and a response object and returns True,
if every element is in response'''
    if not hasattr(arguments, '__iter__'):
        raise TypeError("Arguments should be iterable") 
    for arg in arguments:
        if arg not in response:
            raise AssertionError("%s is not in response" % arg)
