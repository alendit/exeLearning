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
SinglePageExport will export a package as a website of HTML pages
"""

from cgi                      import escape
from exe.webui.blockfactory   import g_blockFactory
from exe.engine.error         import Error
from exe.engine.path          import Path
from exe.export.singlepage    import SinglePage

import logging
log = logging.getLogger(__name__)


# ===========================================================================
class SinglePageExport(object):
    """
    SinglePageExport will export a package as a website of HTML pages
    """
    def __init__(self, stylesDir, outputDir, imagesDir, scriptsDir, templatesDir):
        """
        'stylesDir' is the directory where we can copy the stylesheets from
        'outputDir' is the directory that will be [over]written
        with the website
        """
        self.html         = ""
        self.style        = None
        self.name         = None
        self.stylesDir    = Path(stylesDir)
        self.outputDir    = Path(outputDir)
        self.imagesDir    = Path(imagesDir)
        self.scriptsDir   = Path(scriptsDir)
        self.templatesDir = Path(templatesDir)
	self.page         = None

        # Create the output dir if it doesn't already exist
        if not self.outputDir.exists(): 
            self.outputDir.mkdir()


    def export(self, package, for_print=0):
        """ 
        Export web site
        Cleans up the previous packages pages and performs the export
        """
        self.style = package.style       
	
	self.page = SinglePage("index", 1, package.root)

        self.page.save(self.outputDir/"index.html", for_print)
	
	self.copyFiles(package)


    def copyFiles(self, package):
        """
        Copy all the files used by the website.
        """
        # Copy the style sheet files to the output dir
        # But not nav.css
        styleFiles  = [self.stylesDir/'..'/'base.css']
	styleFiles += [self.stylesDir/'..'/'popup_bg.gif']
        styleFiles += self.stylesDir.files("*.css")
        if "nav.css" in styleFiles:
            styleFiles.remove("nav.css")
        styleFiles += self.stylesDir.files("*.jpg")
        styleFiles += self.stylesDir.files("*.gif")
        styleFiles += self.stylesDir.files("*.png")
        styleFiles += self.stylesDir.files("*.js")
        styleFiles += self.stylesDir.files("*.html")
        self.stylesDir.copylist(styleFiles, self.outputDir)

        # copy the package's resource files
        package.resourceDir.copyfiles(self.outputDir)

        # copy script files.
        self.scriptsDir.copylist(('libot_drag.js', 'common.js'), 
                                     self.outputDir)
	
	# copy players for media idevices.                
        hasFlowplayer     = False
        hasMagnifier      = False
        hasXspfplayer     = False

	for idevice in self.page.node.idevices:
	    if (hasFlowplayer and hasMagnifier and hasXspfplayer):
		break
	    if not hasFlowplayer:
		if 'flowPlayer.swf' in idevice.systemResources:
		    hasFlowplayer = True
	    if not hasMagnifier:
		if 'magnifier.swf' in idevice.systemResources:
		    hasMagnifier = True
	    if not hasXspfplayer:
		if 'xspf_player.swf' in idevice.systemResources:
		    hasXspfplayer = True
                        
        if hasFlowplayer:
            videofile = (self.templatesDir/'flowPlayer.swf')
            videofile.copyfile(self.outputDir/'flowPlayer.swf')
        if hasMagnifier:
            videofile = (self.templatesDir/'magnifier.swf')
            videofile.copyfile(self.outputDir/'magnifier.swf')
        if hasXspfplayer:
            videofile = (self.templatesDir/'xspf_player.swf')
            videofile.copyfile(self.outputDir/'xspf_player.swf')


        if package.license == "GNU Free Documentation License":
            # include a copy of the GNU Free Documentation Licence
            (self.templatesDir/'fdl.html').copyfile(self.outputDir/'fdl.html')


# ===========================================================================
