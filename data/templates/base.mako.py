# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1289136242.4242289
_template_filename=u'/home/alendit/workspace/exepylons/ExePylons/exepylons/templates/base.mako'
_template_uri=u'/base.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u"<!DOCTYPE html>\n<html>\n    <head>\n        <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\n        <title>EXE Main: ")
        # SOURCE LINE 5
        __M_writer(escape(self.title()))
        __M_writer(u'</title>\n        ')
        # SOURCE LINE 6
        __M_writer(escape(h.javascript_link('/scripts/jquery.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 7
        __M_writer(escape(self.head_tags()))
        __M_writer(u'\n    </head>\n    <body>\n        <h1>')
        # SOURCE LINE 10
        __M_writer(escape(self.title()))
        __M_writer(u'</h1>\n\n<!-- ***BEGIN page content -->\n')
        # SOURCE LINE 13
        __M_writer(escape(self.body()))
        __M_writer(u'\n<!-- ***END page content -->\n\n    </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


