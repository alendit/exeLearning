# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
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
PDF device, uses pdflib to convert pdf to html
"""

import logging
import os
from exe.webui.block            import Block
from exe.webui.elementfactory   import g_elementFactory
from exe.webui                  import common
from exe.engine.idevice                 import Idevice
import re

log = logging.getLogger(__name__)


# ===========================================================================
class PdfBlock(Block):
    """
    PDF device, uses pdflib to convert pdf to html
    """
    def __init__(self, parent, idevice):
        Block.__init__(self, parent, idevice)
        self.elements = []


    def process(self, request):
        """
        Process the request arguments from the web server
        """
        is_cancel = common.requestHasCancel(request)

        Block.process(self, request)
        if "pages" + self.id in request.args and not is_cancel :
            self.idevice.pages = request.args["pages" + self.id][0]
        if "path" + self.id in request.args \
        and not is_cancel:
            pdfPath = request.args["path"+self.id][0]
            self.idevice.path = pdfPath
            try:
                self.idevice.uploadFile()
            except IOError, e:
                log.error("Unable to add file %s" % pdfPath)
        if "height" + self.id in request.args and not is_cancel:
            self.idevice.height = request.args["height" + self.id][0]
        if (u"action" not in request.args or
            request.args[u"action"][0] != u"delete"):
            for element in self.elements:
                element.process(request)

    def renderEdit(self, style):
        """
        Returns an XHTML string with the form element for editing this block
        """
        heightArr = [['small', '300'],
                    ['normal', '500'],
                    ['large', '700']]
        html  = u'<div><div class="block">\n'
        html += u"<strong>%s</strong>" % _("PDF import")
        html += common.elementInstruc(self.idevice.appletInstruc)
        html += u'</div>'
        html += u'<div class="block">\n'
        html += u"<strong>%s</strong>" % _("Path to PDF file")
        html += u'</div>\n'
        html += u'<div class="block">\n'
        html += common.textInput("path"+self.id, self.idevice.path, 50) 
        html += u'<input type="button" onclick="addPdf(\'%s\')"' % self.id
        html += u"value=\"%s\"/>\n" % _(u"Add file")
        html += u'</div>'
        html += u'<div class="block">\n'
        html += u"<strong>%s</strong>" % _("Pages to import")
        html += common.elementInstruc(self.idevice.pagesInstruc)
        html += u'</div>\n'
        html += u'<div class="block">\n'
        html += common.textInput("pages"+self.id, self.idevice.pages, 10)
        html += u"</div>\n"
        html += u"<div>\n"
        this_package = None
        if self.idevice is not None and self.idevice.parentNode is not None:
            this_package = self.idevice.parentNode.package
        html += common.formField('select', this_package, _('Frame Height:'),
                "height" + self.id, options = heightArr, 
                selection = self.idevice.height)
        html += u"</div>\n"
        for element in self.elements:
            html += element.renderEdit() + "<br/>"
        html += u"</div>\n"
        html += self.renderEditButtons()
        return html


    def renderPreview(self, style):
        """
        Returns an XHTML string for previewing this block during editing
        """
        html  = u"<div class=\"iDevice "
        html += u"emphasis"+unicode(self.idevice.emphasis)+"\" "
        html += u"ondblclick=\"submitLink('edit', "+self.id+", 0);\">\n"
        if self.idevice.emphasis != Idevice.NoEmphasis:
            if self.idevice.icon:
                html += u'<img alt="%s" class="iDevice_icon" ' % _('IDevice Icon')
                html += u" src=\"/style/"+style
                html += "/icon_"+self.idevice.icon+".gif\"/>\n"
            #html += u"<span class=\"iDeviceTitle\">"
            #html += self.idevice.title
            #html += u"</span>\n"
        html += self.renderViewContent("resources/")
        html += self.renderViewButtons()
        html += u"</div>\n"
        return html

    
    def renderView(self, style):
        """
        Returns an XHTML string for viewing this block, 
        i.e. when exported as a webpage or SCORM package
        """
        html  = u"<div class=\"iDevice "
        html += u"emphasis"+unicode(self.idevice.emphasis)+"\">\n"
        html += self.renderViewContent()
        html += u"</div>\n"
        return html



    def renderViewContent(self, resource=""):
        html = "<div class=\"iDevice_inner\">\n"
        if self.idevice.file == None:
            html += "<strong>%s : %s</strong>" \
                % (_("File not found"), self.idevice.path)
        else:
            html += u'<iframe height="%s"'  %\
                self.idevice.height
            html += ' width="100%"'
            html += u"src=\"%s\"></iframe>\n" \
                % (resource + self.idevice.file.storageName)
        html += u'</div>\n'
        return html

from exe.engine.pdfidevice import PdfIdevice
from exe.webui.blockfactory    import g_blockFactory
g_blockFactory.registerBlockType(PdfBlock, PdfIdevice)    

# ===========================================================================
