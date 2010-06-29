# ===========================================================================
# eXe
# Copyright 2004-2005, University of Auckland
# Copyright 2004-2007 eXe Project, New Zealand Tertiary Education Commission
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
This class exports marked freetext-idevices to a DOM presentation
"""

import logging
from cgi                      import escape
from urllib                   import quote
from exe.webui.blockfactory   import g_blockFactory
from exe.engine.error         import Error
from exe.engine.path          import Path
from exe.export.pages         import Page, uniquifyNames
from exe.webui                import common
from exe.export.pages         import Page
from exe.engine               import freetextidevice

log = logging.getLogger("__name__")


class HandoutExport(object):
    """
    This class transform a exe-package to a DOMPresenatation
    """


    def __init__(self, config, styleDir, filename):
        """ 'stylesDir' is the directory where we can copy the stylesheets from
        'outputDir' is the directory that will be [over]written
        with the website
        """
        self.config       = config
        self.imagesDir    = config.webDir/"images"
        self.scriptsDir   = config.webDir/"scripts"
        self.templatesDir = config.webDir/"templates"
        self.stylesDir    = Path(styleDir)
        self.filename     = Path(filename)
        self.pages        = []


    def export(self, package):
        """
        exports package to a dom presentation
        """

        outputDir = self.filename
        if not outputDir.exists():
            outputDir.mkdir()
        self.pages = [ HandoutPage("Index", 1, package.root) ]
        self.generatePages(package.root, 1)
        log.debug(map(lambda x : getattr(x, "name"), self.pages))

        html = u'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"             "http://www.w3.org/TR/html4/strict.dtd">
        <html dir="ltr" lang="en">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>%s</title>
        <style type="text/css" media="screen">
        @import url(base.css);
        @import url(content.css);
        </style>
        <script type="text/javascript">
            function print_page() {
                window.print();
                window.close();
            }
        </script>

        </head>
        <body onload=print_page()>
        <div id="boundary">
        <h1 align="center">%s</h1>
        ''' % (package.name, package.name)
        for page in self.pages:
            slidehtml = page.render()
            if slidehtml != "":
                html += u'<div class="page">'
                html += u'<p id="nodeTitle">%s</p>' % escape(page.node.titleLong)
                html += slidehtml
                html += u'</div>'

	log.debug(type(html))
        html = html.encode("utf8")
	log.debug(type(html))

        log.debug(html)
        output = open(outputDir / "index.html", "w")
        output.write(html)
        output.close()

        self.copyFiles(package, outputDir)


    def copyFiles(self, package, outputDir):
        """
        Copy all the files used by the website.
        """

        print outputDir
        
        # Copy the style sheet files to the output dir
        styleFiles  = [self.stylesDir/'..'/'base.css']
        styleFiles += [self.stylesDir/'..'/'ds_styles.css']
        styleFiles += [self.stylesDir/'..'/'popup_bg.gif']
        styleFiles += self.stylesDir.files("*.css")
        styleFiles += self.stylesDir.files("*.jpg")
        styleFiles += self.stylesDir.files("*.gif")
        styleFiles += self.stylesDir.files("*.png")
        styleFiles += self.stylesDir.files("*.js")
        styleFiles += self.stylesDir.files("*.html")
        self.stylesDir.copylist(styleFiles, outputDir)

        # copy the package's resource files
        package.resourceDir.copyfiles(outputDir)


 

    def generatePages(self, node, depth):
        """
        recursively generates pages
        """

        for child in node.children:
            title = child.titleShort
            if not title:
                title = "__"
            self.pages.append(HandoutPage(title, depth, child))
            self.generatePages(child, depth + 1)
        
        

class HandoutPage(Page):
    """
    converts a page to a presentation page
    """

    def render(self):
        html = u""
        for idevice in self.node.idevices:
            if hasattr(idevice, "exportType") and \
                idevice.exportType == freetextidevice.HANDOUT:
                log.debug("Exportable found: %s" % idevice.id)
                
                html += u"<div class=\"%s\" id=\"id%s\">\n" % \
                    (escape(idevice.klass), escape(idevice.id))
                block = g_blockFactory.createBlock(None, idevice)
                style = self.node.package.style
                html += block.renderView(style)
                html += u"</div>\n"
                
        return html
