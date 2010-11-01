# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
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
FreeTextIdevice: just has a block of text
"""

import logging
from exe.engine.idevice import Idevice
from exe.engine.field   import TextAreaField
log = logging.getLogger(__name__)

# ===========================================================================
class HintIdevice(Idevice):
    """
    HintIdevice: just has a block of text don't exporting
    """
    persistenceVersion = 9

    def __init__(self, content=""):
        Idevice.__init__(self, x_(u"Remark"), 
                         x_(u"University of Auckland"), 
                         x_(u"""Leave a commentary for
others who work on this package."""), "", "")
        self.emphasis = Idevice.SomeEmphasis
        self.icon     = u"summary"
        self.group    = Idevice.Didactics
        self.content  = TextAreaField(x_(u"Hint"), 
                                      x_(u"""Use this field to leave a
comment for people who works on this package with you. 
This iDevice won't be exported"""),
                                      content)
        self.content.idevice = self
        if content:
            self.edit = False
        # determines if the element is exported to presentation
        self.presentable = 'False' 

   
    def getResourcesField(self, this_resource):
        """
        implement the specific resource finding mechanism for this iDevice:
        """
        # be warned that before upgrading, this iDevice field could not exist:
        if hasattr(self, 'content') and hasattr(self.content, 'images'):
            for this_image in self.content.images:
                if hasattr(this_image, '_imageResource') \
                and this_resource == this_image._imageResource:
                    return self.content

        return None
       
    def getRichTextFields(self):
        """
        Like getResourcesField(), a general helper to allow nodes to search 
        through all of their fields without having to know the specifics of each
        iDevice type.  
        """
        fields_list = []
        if hasattr(self, 'content'):
            fields_list.append(self.content)
        return fields_list

    def burstHTML(self, i):
        """
        takes a BeautifulSoup fragment (i) and bursts its contents to 
        import this idevice from a CommonCartridge export
        """
        # Free Text Idevice:
        #title = i.find(name='span', attrs={'class' : 'iDeviceTitle' })
        #idevice.title = title.renderContents().decode('utf-8')
        # no title for this iDevice.

        # FreeText is also a catch-all idevice for any other which
        # is unable to be burst on its own.
        if i.attrMap['class']=="FreeTextIdevice":
            # For a REAL FreeText, just read the inner div with class:
            inner = i.find(name='div', 
                attrs={'class' : 'block' , 'style' : 'display:block' })
        else:
            # But for all others, read the whole thing:
            inner = i

        self.content.content_wo_resourcePaths = \
                inner.renderContents().decode('utf-8')
        # and add the LOCAL resource paths back in:
        self.content.content_w_resourcePaths = \
                self.content.MassageResourceDirsIntoContent( \
                    self.content.content_wo_resourcePaths)
        self.content.content = self.content.content_w_resourcePaths
        
    def upgradeToVersion1(self):
        """
        Upgrades the node from version 0 (eXe version 0.4) to 1.
        Adds icon
        """
        self.icon = ""


    def upgradeToVersion2(self):
        """
        Upgrades the node from version 1 (not released) to 2
        Use new Field classes
        """
        self.content = TextAreaField("content", 
x_(u"This is a free text field general learning content can be entered."),
                                     self.content)


    def upgradeToVersion3(self):
        """
        Upgrades the node from 2 (v0.5) to 3 (v0.6).
        Old packages will loose their icons, but they will load.
        """
        log.debug(u"Upgrading iDevice")
        self.emphasis = Idevice.NoEmphasis
        

    def upgradeToVersion4(self):
        """
        Upgrades v0.6 to v0.7.
        """
        self.lastIdevice = False
   

    def upgradeToVersion5(self):
        """
        Upgrades v0.6 to v0.7.
        """
        self._upgradeIdeviceToVersion1()

        
    def upgradeToVersion6(self):
        """
        Upgrades to v0.12
        """
        self._upgradeIdeviceToVersion2()

    def upgradeToVersion7(self):
        """
        Attach the idevice to the TextAreaField for tinyMCE image embedding:
        """
        self.content.idevice = self
    def upgradeToVersion8(self):
        """
        Attach presentable to idevice
        Tum changes
        """
        self.presentable = 'False'
   

    def upgradeToVersion9(self):
        """
        Adds group to idevice
        """
        self.group = Idevice.Content
 
   
# ===========================================================================

