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
Feedback block, renders simple feedback link
"""

import logging
from exe.webui.block            import Block
from exe.webui.elementfactory   import g_elementFactory
from exe.webui                  import common

log = logging.getLogger(__name__)


# ===========================================================================
class FeedbackBlock(Block):
    """
    GenericBlock can render and process GenericIdevices as XHTML
    """
    def __init__(self, parent, idevice):
        Block.__init__(self, parent, idevice)
        self.elements = []
        for field in self.idevice:
            self.elements.append(g_elementFactory.createElement(field))
        if not hasattr(self.idevice,'undo'): 
            self.idevice.undo = True


    def process(self, request):
        """
        Process the request arguments from the web server
        """
        is_cancel = common.requestHasCancel(request)

        Block.process(self, request)
        if (u"action" not in request.args or
            request.args[u"action"][0] != u"delete"):
            for element in self.elements:
                element.process(request)
        if "address" + self.id in request.args and not is_cancel:
            self.idevice.address = request.args["address" + self.id][0]
        if "subject" + self.id in request.args and not is_cancel:
            self.idevice.subject = request.args["subject" + self.id][0]
        if "comment" + self.id in request.args and not is_cancel:
            self.idevice.comment = request.args["comment" + self.id][0]
        if "title"+self.id in request.args:
            self.idevice.title = request.args["title"+self.id][0]
 


    def renderEdit(self, style):
        """
        Returns an XHTML string with the form element for editing this block
        """
        html  = u'<div><div class="block">\n'
        html += common.elementInstruc(self.idevice.instruc)
        html += common.textInput("title"+self.id, self.idevice.title)
        html += u"</div>\n"
        html += u"<div class=\"block\">"
        html += u"<div class=\"block\">"
        html += u"<strong>%s</strong>" % _("Email Address")
        html += common.elementInstruc(_("Enter the email address you want\
            feedback to be sent to"))
        html += u"</div>\n"
        if self.idevice.address == "":
            self.idevice.address = self.package.email
        html += common.textInput("address"+self.id, self.idevice.address)
        html += u"<div class=\"block\">\n"
        html += u"<strong>%s</strong>" % _("Subject")
        if self.idevice.subject == "":
            if self.package.title == "":
                self.idevice.subject = _("Feedback on ") + \
                  self.package.name + " - " + self.idevice.parentNode.title
            else:
                self.idevice.subject = \
                    _("Feedback on ") + self.package.title + " - " + \
                        self.idevice.parentNode.title
        html += common.elementInstruc(_("Enter default subject of feedback"))
        html += u"</div>\n"
        html += common.textInput("subject"+self.id, self.idevice.subject)
        html += u"<div class=\"block\">\n"
        html += u"<strong>%s</strong>" % _("Comment")
        html += u"<div>\n"
        html += common.textInput("comment"+self.id, self.idevice.subject)
        html += "</div>\n"
        for element in self.elements:
            html += element.renderEdit() + "<br/>"
        html += self.renderEditButtons()
        html += u"</div>\n"
        return html


    def renderViewContent(self):
#        html = "<div class=\"iDevice emphasis1\">\n"
#        html += "<span class=\"iDeviceTitle\">%s</span>" % self.idevice.title
        if self.package is None:
            self.package = self.idevice.parentNode.package
        html = "<div class=\"iDevice_inner\">\n"
        if self.idevice.comment != "":
            html += "<p>%s</p>\n" %\
                self.idevice.comment
        mailtostring = "<a href=\"mailto:" + self.idevice.address
        if self.idevice.subject != "":
            mailtostring += "?subject:%s" % self.idevice.subject
        mailtostring += '" rel="external">%s</a>' % (_("Feedback to ") \
            + self.package.author)
        html += "<div class=\"block\">%s</div>\n" % mailtostring
        html += "</div>\n"
#        html += "</div>\n"
        return html

from exe.engine.feedbackidevice import FeedbackIdevice
from exe.webui.blockfactory    import g_blockFactory
g_blockFactory.registerBlockType(FeedbackBlock, FeedbackIdevice)

# ===========================================================================
