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
ExternalUrlBlock can render and process ExternalUrlIdevices as XHTML
"""

import logging
from exe.webui.block            import Block
from exe.webui                  import common
from exe.webui.element          import TermElement

log = logging.getLogger(__name__)


# ===========================================================================
class GlossaryBlock(Block):
    """
    GlossaryBlock can render and process GlossaryIdevices as XHTML
    """
    def __init__(self, parent, idevice):
        Block.__init__(self, parent, idevice)
        self.idevice = idevice
        self.termElements = []
        if not hasattr(self.idevice,'undo'): 
            self.idevice.undo = True

        for term in idevice.terms:
            self.termElements.append(TermElement(term))


    def process(self, request):
        """
        Process the request arguments from the web server to see if any
        apply to this block
        """
        Block.process(self, request)

        is_cancel = common.requestHasCancel(request)

        if "title"+self.id in request.args:
            self.idevice.title = request.args["title"+self.id][0]
        if ("addTerm" + self.id) in request.args:
            self.idevice.addTerm()
            self.idevice.edit = True
            self.idevice.undo = False
        for element in self.termElements:
            element.process(request)
        if ("action" in request.args and request.args["action"][0] == "done"
            or not self.idevice.edit):
            # remove the undo flag in order to reenable it next time:
            if hasattr(self.idevice,'undo'): 
                del self.idevice.undo
 


    def renderEdit(self, style):
        """
        Returns an XHTML string with the form element for editing this block
        """
        html  = u'<div class="iDevice">\n'
        html += common.textInput("title"+self.id, self.idevice.title)
        html += "<br/><br/>\n"
        value = _("Add another Term")
        html += common.submitButton("addTerm" + self.id, value)
        for element in self.termElements:
            html += element.renderEdit()

        html += "<br/>"
        html += self.renderEditButtons()
        html += u"</div>\n"

        return html


    def renderPreview(self, style):
        """
        Returns an XHTML string for previewing this block
        """
        lettersDict = {}
        broken = []
        count = 0
        for element in self.termElements:
            count += 1
            log.debug(len(element.termElement.field.content))
            if len(element.termElement.field.content) == 0:
                broken.append(str(count))
                log.debug("THIS IS BROKEN " + str(count))
                continue
            leadLetter = element.termElement.field.content[0].upper()
            if leadLetter in lettersDict:
                lettersDict[leadLetter] += element.renderPreview()
            else:
                lettersDict[leadLetter] = element.renderPreview()
        sortedLetters = lettersDict.keys()
        sortedLetters.sort()

        html = u'<a id="glossary_start"></a>'
        if len(broken) > 0:
            log.debug(", ".join(broken)) 
            html += common.editModeHeading(_('Terms number %s are not entered)' % ", ".join(broken)))
        html += u"<div class=\"iDevice "
        html += u"emphasis"+unicode(self.idevice.emphasis)+"\" "
        html += u"ondblclick=\"submitLink('edit',"+self.id+", 0);\">\n"
        html += u'<img alt="" class="iDevice_icon" '
        html += u"src=\"/style/"+style+"/icon_"+self.idevice.icon
        html += ".gif\" />\n"
        html += u"<span class=\"iDeviceTitle\">"       
        html += self.idevice.title+"</span>\n"
        html += u'<div class="iDevice_inner">\n'

        for letter in sortedLetters:
            html += '<a href="#anchor%s">' % letter
            html += '<span style="font-size: 26px">%s</span></a>\n' % letter
        html += '<br/>\n'
        html += '<br/>\n'

        for letter in sortedLetters:
            html += '<a name="anchor%s">' % letter
            html += '<span style="font-size: 26px">%s</span></a>\n' % letter
            html += '<br/>\n'
            html += '<br/>\n'
            html += lettersDict[letter]
            html += '<br/>\n'
            html += '<a href="#glossary_start">%s</a>\n' % _('Top')
            html += '<br/>\n'
            html += '<br/>\n'
            html += '<br/>\n'

        html += u"</div>\n"
        html += self.renderViewButtons()
        html += u"</div>\n"

        return html


    def renderView(self, style):
        """
        Returns an XHTML string for viewing this block
        """
        lettersDict = {}
        broken = []
        count = 0
        for element in self.termElements:
            count += 1
            if len(element.termElement.field.content) == 0:
                broken.append(str(count))
                continue
            leadLetter = element.termElement.field.content[0].upper()
            if leadLetter in lettersDict:
                lettersDict[leadLetter] += element.renderPreview()
            else:
                lettersDict[leadLetter] = element.renderPreview()
        sortedLetters = lettersDict.keys()
        sortedLetters.sort()

        html = u'<a id="glossary_start"></a>'
        if broken:
            html += common.editModeHeading("Terms number %s are not entered)" % ", ".join(broken))
 
        html += u'<div class="iDevice '
        html += u'emphasis'+unicode(self.idevice.emphasis)+'">\n'
        html += u'<img alt="" class="iDevice_icon" '
        html += u'src="icon_'+self.idevice.icon+'.gif" />\n'
        html += u'<span class="iDeviceTitle">'
        html += self.idevice.title+'</span>\n'
        html += u'<div class="iDevice_inner">\n'

        for letter in sortedLetters:
            html += '<a href="#anchor%s">' % letter
            html += '<span style="font-size: 26px">%s</span></a>\n' % letter
        html += '<br/>\n'
        html += '<br/>\n'

        for letter in sortedLetters:
            html += '<a id="anchor%s">' % letter
            html += '<span style="font-size: 26px">%s</span></a>\n' % letter
            html += '<br/>\n'
            html += '<br/>\n'
            html += lettersDict[letter]
            html += '<br/>\n'
            html += '<a href="#glossary_start">%s</a>\n' % _('Top')
            html += '<br/>\n'
            html += '<br/>\n'
            html += '<br/>\n'

        html += "</div></div>\n"

        return html
 

from exe.engine.glossaryidevice import GlossaryIdevice
from exe.webui.blockfactory     import g_blockFactory
g_blockFactory.registerBlockType(GlossaryBlock, GlossaryIdevice)    

# ===========================================================================
