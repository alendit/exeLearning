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
iDevice for pdf
"""

from exe.engine.idevice import Idevice
# For backward compatibility Jelly expects to find a Field class
from exe.engine.field   import Field, TextField, TextAreaField, FeedbackField 
from exe.engine.field   import ImageField, AttachmentField
from exe.engine.path    import Path, toUnicode
from exe.engine.resource import Resource
from pyPdf              import PdfFileWriter, PdfFileReader
from re                 import search, sub
import os

import logging
log = logging.getLogger(__name__)


# ===========================================================================
class PdfIdevice(Idevice):
    """
    Idevice for pdf integration
    """
    persistenceVersion = 11
    
    def __init__(self):
        """
        Initialize 
        """
        self.title = _("Pdf iDevice")
        self.class_ = "Pdf Device"
        self.author = "Dimitri Vorona"
        self.purpose = _("Import local pdf and display them with Acrobat Reader plugin (must be installed first)")
        
        self.file = None 
        self.path = ""
        self.group = ""
        self.pages = ""
        self.height = '500'
        self.emphasis = Idevice.NoEmphasis
        tip = ""
        if self.class_ in ("objectives", "activity", "reading", "preknowledge"):
            icon = class_
        else:
            icon = None
        Idevice.__init__(self, self.title, self.author, self.purpose, \
        "", None)
        self.group = Idevice.Content
        self.pagesInstruc = _("Input coma-separated pages or page ranges to import. For example: 1,2,3-8. Leave empty to import all pages")
        self.appletInstruc = _("This applet imports a local pdf into your package. It can also import specified pages only")
        self.icon    = icon
        self.fields  = []
        self.nextFieldId = 0
        self.systemResources.append('common.js')
        self.systemResources.append('libot_drag.js')



    def getResourcesField(self, this_resource):
        """
        implement the specific resource finding mechanism for these 
        Generic iDevices:
        """
        if this_resource in self.userResources:
            return this_resource

        return None

    @staticmethod
    def __parseImportPages(importString, lastPage):
        """
        Parses a string to an array of page numbers to import
        """
        importString = sub('[^\d,-]', '', importString)
        toimport = []
        if importString != "":
            singleranges = importString.split(",")
            for onerange in singleranges:
                if "-" in onerange:
                    # look how awesome I am xD
                    start, end = map(lambda x : x != '' and \
                       int(x) or -1, onerange.split("-"))
                    if start == -1 or start > lastPage:
                        start = 1
                    if end == -1 or end > lastPage:
                        end = lastPage + 1
                    start, end = min(start, end), max(start, end)

                    toimport += [page for page in range(start - 1, end) \
                        if not page in toimport]
                else :
                    if onerange != '':
                        page = min(int(onerange) - 1, lastPage)
                        if not page in toimport:
                            toimport += [page]
        else:
            toimport = range(lastPage + 1)
        return toimport



    def uploadFile(self):
        '''Store pdf in package, gets sides from pdf, if self.sides
        isn't empty
        '''
        filePath = self.path
        log.debug(u"uploadFile " + unicode(filePath))
        if not self.parentNode or not self.parentNode.package:
            log.error('something is wrong with the file')
        ## replace all non-digits and non-usefull stuff with ''
        self.pages = sub('[^\d,-]', '', self.pages)
        if self.pages != "":
            input = PdfFileReader(file(filePath, "rb"))
            lastPage = input.getNumPages() - 1 # last page
            toimport = PdfIdevice.__parseImportPages(self.pages, lastPage)
            log.debug("Parsed pages: " + str(toimport))
            output = PdfFileWriter()

            for page in toimport:
                output.addPage(input.getPage(page))
            log.debug("Found pages to import %s" % toimport)
            tmp = os.tmpnam() + ".pdf"
            log.debug('Tempfile is %s' % tmp)
            outputStream = file(tmp, "wb")
            output.write(outputStream)
            outputStream.close()
            resourceFile = Path(tmp)
            self.file = Resource(self, resourceFile)
            log.debug("Uploaded %s, pages: %s" % (tmp, toimport)) 
            os.remove(tmp)
            filePath = tmp
        resourceFile = Path(filePath)
        if resourceFile.isfile():
            self.file = Resource(self, resourceFile)
            log.debug(u"uploaded " + self.path)

      
    def getRichTextFields(self):
        """
        Like getResourcesField(), a general helper to allow nodes to search 
        through all of their fields without having to know the specifics of each
        iDevice type.  
        """
        return []

    def burstHTML(self, i):
        """
        takes a BeautifulSoup fragment (i) and bursts its contents to 
        import this idevice from a CommonCartridge export
        """
        # Generic Idevice, with content in fields[]:
        title = i.find(name='span', 
                attrs={'class' : 'iDeviceTitle' }) 
        inner = i.find(name='iframe').__str__()
        self.path = search("<iframe .* src=\"(.*?)\">", inner)
        self.uploadFile(path)
        
 
    def upgradeToVersion1(self):
        """
        Upgrades the node from version 0 (eXe version 0.4) to 1.
        Adds icon
        """
        log.debug("Upgrading iDevice")
        if self.class_ in ("objectives", "activity", "reading", "preknowledge"):
            self.icon = self.class_
        else:
            self.icon = "generic"


    def upgradeToVersion2(self):
        """
        Upgrades the node from version 1 (not released) to 2
        Use new Field classes
        """
        oldFields   = self.fields
        self.fields = []
        for oldField in oldFields:
            if oldField.fieldType == "Text":
                self.addField(TextField(oldField.__dict__['name'],
                                        oldField.instruction,
                                        oldField.content))
            elif oldField.fieldType == "TextArea":
                self.addField(TextAreaField(oldField.__dict__['name'],
                                            oldField.instruction,
                                            oldField.content))
            else:
                log.error(u"Unknown field type in upgrade "+oldField.fieldType)


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
        Upgrades exe to v0.10
        """
        self._upgradeIdeviceToVersion1()


    def upgradeToVersion6(self):
        """
        Upgrades to v0.12
        """
        self._upgradeIdeviceToVersion2()

        for field in self.fields:
            field._upgradeFieldToVersion2()

        self.systemResources += ["common.js", "libot_drag.js"]

    def upgradeToVersion7(self):
        """
        Upgrades to v0.13
        """
        # Upgrade old style reading activity's feedback field
        if self.class_ == 'reading':
            # Upgrade the feedback field
            for i, field in enumerate(self.fields):
                if isinstance(field, TextAreaField) \
                and hasattr(field, 'name') \
                and field.name in (_(u'Feedback'), u'Feedback'):
                    newField = FeedbackField(field.name, field.instruc)
                    Field.nextId -= 1
                    newField._id = field._id
                    newField.feedback = field.content
                    newField.idevice = self
                    self.fields[i] = newField
            # Upgrade the title
            if self.title == _(u'Reading Activity 0.11'):
                # If created in non-english, upgrade in non-english
                self.title = x_(u'Reading Activity')
            if self.title == u'Reading Activity 0.11':
                # If created in english, upgrade in english
                self.title = u'Reading Activity'
                
    def upgradeToVersion8(self):
        """
        Upgrades to v0.20
        """
        self.nextFieldId = 0
        
    def upgradeToVersion9(self):
        """
        Upgrades to v0.24
        """
        for field in self.fields:
            if isinstance(field, ImageField):
                field.isFeedback = False


    def upgradeToVersion9(self):
        """
        Upgrades to somewhere before version 0.25 (post-v0.24) 
        Taking the old unicode string fields, and converting them 
        into image-enabled TextAreaFields:
        [see also the upgrade in field.py's FeedbackField and 
         idevicestore.py's  __upgradeGeneric() ]
        """
        # Upgrade reading activity's FeedbackField
        # which will PROBABLY already go through the proper upgrade path
        # from its own field persistence, BUT since this is a generic idevice
        # and is often handled differently, with generic.data and whatnot,
        # go ahead and throw in this possibly redundant upgrade check:
        if self.class_ == 'reading':
            # Upgrade the FeedbackField
            for i, field in enumerate(self.fields):
                if isinstance(field, FeedbackField):
                    if not hasattr(field,"content"): 
                        # this FeedbackField has NOT been upgraded: 
                        field.content = field.feedback 
                        field.content_w_resourcePaths = field.feedback 
                        field.content_wo_resourcePaths = field.feedback
    def upgradeToVersion10(self):
        """
        Adds height to choose
        """
        self.height = '500'

    def upgradeToVersion11(self):
        """
        Adds group to idevice
        """
        self.group = Idevice.Content
 

# ===========================================================================
