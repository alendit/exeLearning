# ===========================================================================
# eXe
# Copyright 2004-2006, University of Auckland
# Copyright 2006-2007 eXe Project, New Zealand Tertiary Education Commission
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================

"""
Importing pdf page by page
"""

import logging
from twisted.web.resource      import Resource
from exe.webui                 import common
from exe.webui.renderable      import RenderableResource

log = logging.getLogger(__name__)


class ImportPDFPage(RenderableResource):
    """
    ImportPDFPage is resposible for importing pdfs page by page
    """
    name = 'importPDF'

    def __init__(self, parent):
        """
        Initialize
        """
        RenderableResource.__init__(self, parent)
        self.localeNames  = []



    def getChild(self, name, request):
        """
        Try and find the child for the name given
        """
        if name == "":
            return self
        else:
            return Resource.getChild(self, name, request)


    def render_GET(self, request):
        """Render the preferences"""
        log.debug("render_GET")
        
        # Rendering
        html  = common.docType()
        html += u"<html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
        html += u"<head>\n"
        html += u"<style type=\"text/css\">\n"
        html += u"@import url(/css/exe.css);\n"
        html += u'@import url(/style/base.css);\n'
        html += u"@import url(/style/standardwhite/content.css);</style>\n"
        html += u'''<script language="javascript" type="text/javascript">
            function doImportPDF(path, pages) {
                opener.nevow_clientToServerEvent('importPDF', this, '', path,
                    pages);
                window.close();
            }
        </script>'''
        html += "<script src=\"scripts/common.js\" language=\"JavaScript\">"
        html += "</script>\n"
        html += u"<title>"+_("Import PDF")+"</title>\n"
        html += u"<meta http-equiv=\"content-type\" content=\"text/html; "
        html += u" charset=UTF-8\"></meta>\n";
        html += u"</head>\n"
        html += u"<body>\n"
        html += u"<div id=\"main\"> \n"     
        html += u"<form method=\"post\" action=\"\" "
        html += u"id=\"contentForm\" >"  

        # package not needed for the preferences, only for rich-text fields:
        this_package = None
        html += common.formField("textInput", this_package, _("Path to PDF"),
            'path', instruction=_("Enter path to pdf you want to import"))
        html += u'<input type="button" onclick="addPdf(\'\')"'
        html += u"value=\"%s\"/>\n" % _(u"Add file")
        html += common.formField("textInput", this_package, _("Pages to import"),
            'pages', instruction = _("Comma-separated list of pages to import"))
        html += u"<div id=\"editorButtons\"> \n"     
        html += u"<br/>" 
        html += common.button("ok", _("OK"), enabled=True,
                _class="button",
                onClick='doImportPDF(document.forms.contentForm.path.value,' +
                    'document.forms.contentForm.pages.value)')
        html += common.button("cancel", _("Cancel"), enabled=True,
                _class="button", onClick="window.close()")
        html += u"</div>\n"
        html += u"</div>\n"
        html += u"<br/></form>\n"
        html += u"</body>\n"
        html += u"</html>\n"
        return html.encode('utf8')


    def render_POST(self, request):
        """
        function replaced by nevow_clientToServerEvent to avoid POST message
        """
        log.debug("render_POST " + repr(request.args))
        
        # invoked if enter is pressed in text field
        path = ""
        if "path" in request.args:
            path = request.args['path'][0]
        if "pages" in request.args:
            pages = request.args['pages'][0]
        html  = common.docType()
        html += u"<html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
        html += u"<head>\n"
        html += u'''<script language="javascript" type="text/javascript">
            function doImportPDF(path, pages) {
                opener.nevow_clientToServerEvent('importPDF', this, '', path);
                window.close();
            }
        </script>'''
        html += u"</head>"
        html += u"<body onload=\"doImportPDF(\'%s\', \'%s\')\";\n" % \
            (path, pages)
        html += u"</body>\n"
        html += u"</html>\n"
        return html.encode('utf8')
