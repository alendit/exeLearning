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
Simple feedback iDevice, just pasts a mailto link
"""

from exe.engine.idevice import Idevice
# For backward compatibility Jelly expects to find a Field class
from exe.engine.field   import Field, TextField, TextAreaField, FeedbackField 
from exe.engine.field   import ImageField, AttachmentField
import re
import logging
log = logging.getLogger(__name__)


# ===========================================================================
class FeedbackIdevice(Idevice):
    """
    Simple feedback iDevice, pasts a mailto link with a defined content
    """
    persistenceVersion = 10
    
    def __init__(self):
        """
        Initialize 
        """
        self.title = _("Feedback")
        self.class_ = "Feedback"
        self.author = "Dimitri Vorona"
        self.purpose = _("Feedback to the author")
        self.tip = _("Use it to put a feedback link to your documents")
        if self.class_ in ("objectives", "activity", "reading", "preknowledge"):
            icon = class_
        else:
            icon = None
        Idevice.__init__(self, self.title, self.author, self.purpose, \
            self.tip, None)
        self.icon    = u"question"
        self.address = ""
        self.subject = "" 
        self.comment = ""
        self.instruc = _("Use this iDevice to put feedback link in your" + \
            "documents")
        self.fields  = []
        self.nextFieldId = 0
        self.group = Idevice.Communication
        self.systemResources.append('common.js')
        self.systemResources.append('libot_drag.js')


    def __iter__(self):
        return iter(self.fields)

    def getResourcesField(self, this_resource):
        """
        implement the specific resource finding mechanism for these 
        Generic iDevices:
        """
        return None

      
    def getRichTextFields(self):
        """
        Like getResourcesField(), a general helper to allow nodes to search 
        through all of their fields without having to know the specifics of each
        iDevice type.  
        """
        # All of Generic iDevice's rich-text fields are in... fields!
        # Some of the fields may NOT be rich-text, though,
        # so this needs a bit more parsing:
        fields_list = []
        return fields_list

    def burstHTML(self, i):
        """
        takes a BeautifulSoup fragment (i) and bursts its contents to 
        import this idevice from a CommonCartridge export
        """
        # feedback iDevice
        title = i.find(name='span', 
                attrs={'class' : 'iDeviceTitle' }) 
        self.title = title.renderContents().decode('utf-8') 

        #TODO
        if self.class_ in ("objectives", "activity", "preknowledge", "generic"):
            inner = i.find(name='div', 
                attrs={'class' : 'iDevice_inner' }) 
            inner_content = inner.find(name='div', 
                    attrs={'id' : re.compile('^ta') }) 
            self.fields[0].content_wo_resourcePaths = \
                inner_content.renderContents().decode('utf-8') 
            # and add the LOCAL resources back in: 
            self.fields[0].content_w_resourcePaths = \
                self.fields[0].MassageResourceDirsIntoContent( \
                self.fields[0].content_wo_resourcePaths)
            self.fields[0].content = self.fields[0].content_w_resourcePaths

        elif self.class_ == "reading":
            readings = i.findAll(name='div', attrs={'id' : re.compile('^ta') }) 
            # should be exactly two of these:                    
            # 1st = field[0] == What to Read 
            if len(readings) >= 1: 
                self.fields[0].content_wo_resourcePaths = \
                        readings[0].renderContents().decode('utf-8') 
                # and add the LOCAL resource paths back in:
                self.fields[0].content_w_resourcePaths = \
                    self.fields[0].MassageResourceDirsIntoContent( \
                        self.fields[0].content_wo_resourcePaths)
                self.fields[0].content = \
                    self.fields[0].content_w_resourcePaths
            # 2nd = field[1] == Activity
            if len(readings) >= 2: 
                self.fields[1].content_wo_resourcePaths = \
                        readings[1].renderContents().decode('utf-8')
                # and add the LOCAL resource paths back in:
                self.fields[1].content_w_resourcePaths = \
                    self.fields[1].MassageResourceDirsIntoContent(\
                        self.fields[1].content_wo_resourcePaths)
                self.fields[1].content = \
                    self.fields[1].content_w_resourcePaths
            # if available, feedback is the 3rd field:
            feedback = i.find(name='div', attrs={'class' : 'feedback' , \
                    'id' : re.compile('^fb')  })
            if feedback is not None:
                self.fields[2].content_wo_resourcePaths = \
                    feedback.renderContents().decode('utf-8')
                # and add the LOCAL resource paths back in:
                self.fields[2].content_w_resourcePaths = \
                    self.fields[2].MassageResourceDirsIntoContent( \
                        self.fields[2].content_wo_resourcePaths)
                self.fields[2].content = \
                        self.fields[2].content_w_resourcePaths


    def upgradeToVersion10(self):
        """
        Adds group to idevice
        """
        self.group = Idevice.Communication
 
# ===========================================================================
