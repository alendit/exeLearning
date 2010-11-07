# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1289152437.41154
_template_filename='/home/alendit/workspace/exepylons/ExePylons/exepylons/templates/main/main.mako'
_template_uri='/main/main.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['head_tags', 'title']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u"\n<div id='packages'>\n    <h2> Package List </h2>\n")
        # SOURCE LINE 6
        for package in c.packages:
            # SOURCE LINE 7
            __M_writer(u"    <p><a href='/package/index/")
            __M_writer(escape(package.id))
            __M_writer(u"'>")
            __M_writer(escape(package.title))
            __M_writer(u' - ')
            __M_writer(escape(package.id))
            __M_writer(u'</a><p>\n')
            pass
        # SOURCE LINE 9
        __M_writer(u'</div>\n<p>And Zoidberg...</p>\n\n<input id="createNew" type="submit" action="#" value="Create New"/>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(escape(h.javascript_link('/scripts/common.js')))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'Main Page')
        return ''
    finally:
        context.caller_stack._pop_frame()


