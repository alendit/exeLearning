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
ExternalUrlIdevice: just has a block of text
"""

import logging
from exe.engine.idevice import Idevice
from exe.engine.translate import lateTranslate
from exe.engine.field import GlossaryElementField
log = logging.getLogger(__name__)

# ===========================================================================
class GlossaryIdevice(Idevice):
    """
    Adds a alphabeticly sorted glossary to a package
    """
    persistenceVersion = 0

    def __init__(self, content=""):
        Idevice.__init__(self, x_(u"Glossary"), 
                         x_(u"Technical University Munich"), 
                         x_(u"""Adds a alphabethicaly sorted glossary
                         """), "", "")
        self.emphasis = Idevice.SomeEmphasis
        self.group    = Idevice.Content
        self.terms = []
        self.icon = u"summary"
       
        self.addTerm()
        self.urlInstruc = x_(u"""Add your terms and definitions""")

        #Properties


    def addTerm(self):
        """
        Add a new term to this iDevice
        """
        term = GlossaryElementField(self, x_(u'Term'))
        self.terms.insert(0, term)


    def getResourcesField(self, this_resource):
        """
        implement the specific resource finding mechanism for this iDevice:
        """ 
        for this_term in terms:
            this_field = this_term.getResourcesField(this_resource)
            if this_field:
                return this_field
        return None

      
    def getRichTextFields(self):
        """
        Like getResourcesField(), a general helper to allow nodes to search 
        through all of its fields without having to know the specifics of each 
        iDevice type.  
        """
        fields_list = []

        for this_term in self.terms:
            fields_list.extend(this_term.getRichTextFields())

        return fields_list
        
    def burstHTML(self, i):
        """
        takes a BeautifulSoup fragment (i) and bursts its contents to 
        import this idevice from a CommonCartridge export
        """
        # External Web Site Idevice:
        title = i.find(name='span', attrs={'class' : 'iDeviceTitle' })
        idevice.title = title.renderContents().decode('utf-8')

        inner = i.find(name='div', attrs={'class' : 'iDevice_inner'})

        ## TODO

    
# ===========================================================================
