# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
# Copyright 2006-2008 eXe Project, http://eXeLearning.org/
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
Converts latex source file into html
"""

import re, os, sys, subprocess
import tempfile
from exe.engine.beautifulsoup import BeautifulSoup
from exe.engine.idevice       import Idevice
from exe.engine.field         import TextAreaField
from urllib                   import quote
from cgi                      import escape
from exe.engine.translate     import lateTranslate
from exe.engine.path          import Path, TempDirPath
from exe.engine.resource      import Resource
from exe.export.websiteexport import WebsitePage
from exe                      import globals as G


import logging
log = logging.getLogger(__name__)

# ===========================================================================
class TOCIdevice(Idevice):
    """
    Build a table of content
    """
    persistenceVersion = 9

    def __init__(self):
        Idevice.__init__(self, x_(u"TOC"), 
                         x_(u"TUM"), 
                         x_(u"""Insert a table of content"""), 
                         u"", u"")
        self.emphasis         = Idevice.NoEmphasis
        self.group            = Idevice.Content
        self.source           = u""
        self.article          = TextAreaField(x_(u"Article"))
        self.article.idevice  = self
        self.images           = {}
        self.icon             = u"inter"

    def generateTOC(self):
        '''Generates toc like as we were exporting'''

        
        root = self.parentNode.package.root
        pageNumbers = {}
        html = self.generateTOCEntry(root, pageNumbers)
        self.article.content_w_resourcePaths = html
        self.article.content_wo_resourcePaths = html


    def generateTOCEntry(self, page, pageNumbers):
        '''recursively generates a TOC entry for a page'''

        html  = u'<ul class="toc">\n'
        pageName = page.titleShort.lower().replace(" ", "_")
        pageName = re.sub(r"\W", "", pageName)
        if pageName in pageNumbers:
            pageNumbers[pageName] += 1
            pageName += str(pageNumbers[pageName])
        else:
            pageNumbers[pageName] = 0
        html += u'<a href="%s.html">%s</a>\n' % \
                (quote(pageName), escape(page.titleShort))
        if page.children:
            for child in page.children:
                html += u'<li>\n' + self.\
                        generateTOCEntry(child, pageNumbers) + '</li>\n'
        html += u'</ul>\n'

        return html


    def getRichTextFields(self):
        """
        Like getResourcesField(), a general helper to allow nodes to search 
        through all of their fields without having to know the specifics of each
        iDevice type.  
        """
        fields_list = []
        if hasattr(self, 'article'):
            fields_list.append(self.article)

        return fields_list


    def burstHTML(self, i):
        """
        takes a BeautifulSoup fragment (i) and bursts its contents to 
        import this idevice from a CommonCartridge export
        """
        # Wiki Article Idevice:
        # option title for Wikipedia, with mode emphasis:
        title = i.find(name='span', attrs={'class' : 'iDeviceTitle' })
        if title is not None: 
            self.title = title.renderContents().decode('utf-8')
            self.emphasis=Idevice.SomeEmphasis

        wiki = i.find(name='div', attrs={'id' : re.compile('^ta') })
        self.article.content_wo_resourcePaths = \
                wiki.renderContents().decode('utf-8')
        # and add the LOCAL resource paths back in:
        self.article.content_w_resourcePaths = \
                self.article.MassageResourceDirsIntoContent( \
                    self.article.content_wo_resourcePaths)
        self.article.content = self.article.content_w_resourcePaths

        site = i.find(name='div', attrs={'class' : 'wiki_site' })
        if site is not None: 
            self.site = site.attrMap['value'].decode('utf-8')

        name = i.find(name='div', attrs={'class' : 'article_name' })
        if name is not None: 
            # WARNING: the following crashes on accented characters, eg:
            #  'ascii' codec can't encode character u'\xe8' in 
            #  position 11: ordinal not in range(128)
            self.articleName = name.attrMap['value'].decode('utf-8')

        own_url = i.find(name='div', attrs={'class' : 'own_url' })
        if own_url is not None: 
            self.own_url = own_url.attrMap['value'].decode('utf-8')

# ===========================================================================

