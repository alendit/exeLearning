# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
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
StyleMenu is responsible for creating the XHTML for the styles menu
"""

import logging
from exe.webui.renderable import Renderable
from nevow import stan
log = logging.getLogger(__name__)


# ===========================================================================
class StyleMenu(Renderable):
    """
    StyleMenu is responsible for creating the XHTML for the styles menu
    """
    name = 'stylePane'

    def process(self, request):
        """ 
        Get current package
        """
        log.debug("process")
        
        if ("action" in request.args and 
            request.args["action"][0] == "ChangeStyle"):
            log.debug("changing style to "+request.args["object"][0])
            self.package.style = request.args["object"][0]
            
            
    def render(self, ctx, data):
        """
        Returns an XUL string for viewing this pane
        """
        log.debug("render")
        # Render the start tags
        html  = u"<!-- Styles Pane Start -->\n"
        html += u'<ul id="stylesMenu"'

        # Render each style individually
        for style in self.config.styles:
            name = style[style.find("/") + 1:].capitalize()
            html += u'  <li id="style%s">\n' % name
            html += u'      <a href="javascript:submitLink(\'ChangeStyle\''+\
                    ',\'' + style + '\', 1);">%s</a>\n' % name
            html += u'  </li>\n'

        # Render the end tags
        html += u'  <li id="Add Style">\n'
        html += u'   <a href="javascript:addStyle()">%s</a>\n' % _("Add Style")
        html += u'  </li>\n'
        html += u'</ul>'
        html += u"<!-- Styles Pane End -->\n"
        return stan.xml(html)
        
    
# ===========================================================================
