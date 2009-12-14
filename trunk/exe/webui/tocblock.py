# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
# Copyright 2004-2008 eXe Project, http://eXeLearning.org
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
LatexBlock processes LatexIdevice to HTML
"""

import re, os
import logging
from exe.webui.block   import Block
from exe.webui         import common
from exe.webui.element import TextAreaElement
from exe.engine.idevice   import Idevice

log = logging.getLogger(__name__)


# ===========================================================================
class TOCBlock(Block):
    """
    WikipediaBlock can render and process WikipediaIdevices as XHTML
    """
    def __init__(self, parent, idevice):
        """
        Initialize
        """
        Block.__init__(self, parent, idevice)

        # to compensate for the strange unpickling timing when objects are 
        # loaded from an elp, ensure that proper idevices are set:
        if idevice.article.idevice is None: 
            idevice.article.idevice = idevice
        self.articleElement = TextAreaElement(idevice.article)
        self.articleElement.height = 300
        if not hasattr(self.idevice,'undo'): 
            self.idevice.undo = True
        self.idevice.generateTOC()


    def process(self, request):
        """
        Process the request arguments from the web server to see if any
        apply to this block
        """
        log.debug("process " + repr(request.args))

        is_cancel = common.requestHasCancel(request)
        
        # If they hit "the tick" instead of "load"
        Block.process(self, request)
        if (u"action" not in request.args \
        or request.args[u"action"][0] != u"delete"):
            # If the text has been changed
            self.articleElement.process(request)
        if ("action" in request.args and request.args["action"][0] == "done" or not self.idevice.edit):
            if hasattr(self.idevice, 'undo'):
                del self.idevice.undo



           
    def renderEdit(self, style):
        """
        Returns an XHTML string with the form elements for editing this block
        """

        html = self.articleElement.renderEdit()
        html += self.renderEditButtons(undo=self.idevice.undo)
        html += u"</div>\n"
        return html


    def renderPreview(self, style):
        """
        Returns an XHTML string for previewing this block
        """
        log.debug("renderPreview")
        html  = u"<div class=\"iDevice "
        html += u"emphasis"+unicode(self.idevice.emphasis)+"\" "
        html += u"ondblclick=\"submitLink('edit',"+self.id+", 0);\">\n"
        if self.idevice.emphasis != Idevice.NoEmphasis:
            if self.idevice.icon:
                html += u'<img alt="idevice icon" class="iDevice_icon" '
                html += u" src=\"/style/"+style
                html += "/icon_"+self.idevice.icon+".gif\"/>\n"
            html += u"<span class=\"iDeviceTitle\">"
            html += self.idevice.title
            html += u"</span>\n"
            html += u"<div class=\"iDevice_inner\">\n"
        html += self.articleElement.renderPreview()
        html += u"<br/>\n"
        html += self.renderViewButtons()
        if self.idevice.emphasis != Idevice.NoEmphasis:
            html += u"</div></div>\n"
        else:
            html += u"</div>\n"
        return html
    

    def renderView(self, style):
        """
        Returns an XHTML string for viewing this block
        """        
        log.debug("renderView")
        content = self.articleElement.renderView()
        content = re.sub(r'src="resources/', 'src="', content)
        html  = u"<div class=\"iDevice "
        html += u"emphasis"+unicode(self.idevice.emphasis)+"\">\n"

        if self.idevice.emphasis != Idevice.NoEmphasis:
            if self.idevice.icon:
                html += u'<img alt="iDevice icon" class="iDevice_icon" '
                html += u" src=\"icon_"+self.idevice.icon+".gif\"/>\n"
            html += u"<span class=\"iDeviceTitle\">"
            html += self.idevice.title
            html += u"</span>\n"
            html += u"<div class=\"iDevice_inner\">\n"
        html += content
        html += u"<br/>\n"
        if self.idevice.emphasis != Idevice.NoEmphasis:
            html += u"</div></div>\n"
        else:
            html += u"</div>\n"
        return html
    

from exe.engine.tocidevice import TOCIdevice
from exe.webui.blockfactory      import g_blockFactory
g_blockFactory.registerBlockType(TOCBlock, TOCIdevice)    

# ===========================================================================
