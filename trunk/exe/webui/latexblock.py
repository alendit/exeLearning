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
class LatexBlock(Block):
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



    def process(self, request):
        """
        Process the request arguments from the web server to see if any
        apply to this block
        """
        log.debug("process " + repr(request.args))

        is_cancel = common.requestHasCancel(request)
        
        if 'emphasis'+self.id in request.args \
        and not is_cancel:
            self.idevice.emphasis = int(request.args['emphasis'+self.id][0])
            # disable Undo once an emphasis has changed: 
            self.idevice.undo = False
            
        if 'title'+self.id in request.args \
        and not is_cancel:
            self.idevice.title = request.args['title'+self.id][0]
        if 'kpse' + self.id in request.args and not is_cancel:
            path = \
                request.args['kpse' + self.id][0]
            if not os.path.isdir(path):
                path = os.path.dirname(path)
            self.idevice.latexpath = path
            self.idevice.set_env()
            
        if 'loadSource'+self.id in request.args:
            # If they've hit "load" instead of "the tick"
            self.idevice.source = request.args['path' + self.id][0]
            self.idevice.loadSource()
            # disable Undo once an article has been loaded: 
            self.idevice.undo = False
        else:
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
        log.debug("renderEdit")
        

        html  = u"<div class=\"iDevice\"><br/>\n"
        print self.idevice.message
        if self.idevice.message != "":
            html += common.editModeHeading(self.idevice.message)
            html += common.elementInstruc(self.idevice.kpseInstruc_)
            html += common.textInput("kpse" + self.id, self.idevice.latexpath)
            html += u'<input type="button" onclick="addKpsepath(\'%s\')"' % self.id
            html += u"value=\"%s\"/>\n" % _(u"Search")
            html += u"<br/><br/>\n"
 

        html += common.textInput("title" + self.id, self.idevice.title) + "<br/><br/>"

        this_package = None
        if self.idevice is not None and self.idevice.parentNode is not None:
            this_package = self.idevice.parentNode.package
        
        html += common.textInput("path" + self.id, self.idevice.source)
        html += u'<input type="button" onclick="addTeX(\'%s\')"' % self.id
        html += u"value=\"%s\"/>\n" % _(u"Add file")
        html += common.submitButton(u"loadSource"+self.id, _(u"Load"))
        
        html += u"<br/>\n"
        html += self.articleElement.renderEdit()
        emphasisValues = [(_(u"No emphasis"),     Idevice.NoEmphasis),
                          (_(u"Some emphasis"),   Idevice.SomeEmphasis)]

        html += common.formField('select', this_package, _('Emphasis'),
                                 'emphasis', self.id, 
                                 '', # TODO: Instructions
                                 emphasisValues,
                                 self.idevice.emphasis)

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
    

from exe.engine.latexidevice import LatexIdevice
from exe.webui.blockfactory      import g_blockFactory
g_blockFactory.registerBlockType(LatexBlock, LatexIdevice)    

# ===========================================================================
