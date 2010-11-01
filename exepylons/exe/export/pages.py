# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
# Copyright 2004-2008 eXe Project, http://eXeLearning.org/
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
Export Pages functions
"""

import logging
from urllib                   import quote


log = logging.getLogger(__name__)


# ===========================================================================
class Page(object):
    """
    This is an abstraction for a page containing a node
    e.g. in a SCORM package or Website
    """
    def __init__(self, name, depth, node):
        """
        Initialize
        """
        self.name  = name
        self.depth = depth
        self.node  = node
        
    def renderLicense(self):
        """
        Returns an XHTML string rendering the license.
        """
        licenses = {"GNU Free Documentation License":
                     "http://www.gnu.org/copyleft/fdl.html", 
                     "Creative Commons Attribution 3.0 License":
                     "http://creativecommons.org/licenses/by/3.0/",
                     "Creative Commons Attribution Share Alike 3.0 License":
                     "http://creativecommons.org/licenses/by-sa/3.0/",
                     "Creative Commons Attribution No Derivatives 3.0 License":
                     "http://creativecommons.org/licenses/by-nd/3.0/",
                     "Creative Commons Attribution Non-commercial 3.0 License":
                     "http://creativecommons.org/licenses/by-nc/3.0/",
                     "Creative Commons Attribution Non-commercial Share Alike 3.0 License":
                     "http://creativecommons.org/licenses/by-nc-sa/3.0/",
                     "Creative Commons Attribution Non-commercial No Derivatives 3.0 License":
                     "http://creativecommons.org/licenses/by-nc-nd/3.0/",
                     "Creative Commons Attribution 2.5 License":
                     "http://creativecommons.org/licenses/by/2.5/",
                     "Creative Commons Attribution-ShareAlike 2.5 License":
                     "http://creativecommons.org/licenses/by-sa/2.5/",
                     "Creative Commons Attribution-NoDerivs 2.5 License":
                     "http://creativecommons.org/licenses/by-nd/2.5/",
                     "Creative Commons Attribution-NonCommercial 2.5 License":
                     "http://creativecommons.org/licenses/by-nc/2.5/",
                     "Creative Commons Attribution-NonCommercial-ShareAlike 2.5 License":
                     "http://creativecommons.org/licenses/by-nc-sa/2.5/",
                     "Creative Commons Attribution-NonCommercial-NoDerivs 2.5 License":
                     "http://creativecommons.org/licenses/by-nc-nd/2.5/",
                     "Developing Nations 2.0":
                     "http://creativecommons.org/licenses/devnations/2.0/"}
        html = ""
        
        license = self.node.package.license
        
        if license <> "None" and licenses.has_key(license):
            html += '<p align="center">'
            html += _("Licensed under the")
            html += ' <a rel="license" href="%s">%s</a></p>' % (licenses[license], license)
            
        return html
    
    def renderFooter(self):
        """
        Returns an XHTML string rendering the footer.
        """
        html = ""
        if self.node.package.footer != "":
            html += u'<p align="center">'
            html += self.node.package.footer + u"</p>"
        if self.node.package.footerImg: 
            print "Rendering footer image"
            html += u'<img src="%s">' %\
                self.node.package.footerImg.basename()
            
        return html



# ===========================================================================
def uniquifyNames(pages):
    """
    Make sure all the page names are unique
    """
    pageNumbers = {}

    # First identify the duplicate names
    for page in pages:
        if page.name in pageNumbers:
            pageNumbers[page.name] += 1
            page.name += str(pageNumbers[page.name])

        else:
            pageNumbers[page.name] = 0

