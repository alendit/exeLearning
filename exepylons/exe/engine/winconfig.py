# ===========================================================================
# eXe config
# Copyright 2004-2006, University of Auckland
# Copyright 2007 eXe Project, New Zealand Tertiary Education Commission
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
The WinConfig overrides the Config class with Windows specific
configuration
"""

from exe.engine.config import Config
from exe.engine.path   import Path

# Constants for directory name codes
APPDATA        = 0x001a
COMMON_APPDATA = 0x0023
MYDOCUMENTS    = 0x0005 # Code for c:\documents and settings\myuser\My Documents
PROGRAMFILES   = 0x0026

# ===========================================================================
class WinConfig(Config):
    """
    The WinConfig overrides the Config class with Windows specific
    configuration
    """

    def _overrideDefaultVals(self):
        """Sets the default values
        for windows"""
        exeDir = self.exePath.dirname()
        self.browserPath = exeDir/'Mozilla Firefox'/'firefox.exe'
        if not self.browserPath.isfile():
            programFiles = Path(self._getWinFolder(PROGRAMFILES))
            self.browserPath = programFiles/'Mozilla Firefox'/'firefox.exe'
        self.dataDir   = Path(self._getWinFolder(MYDOCUMENTS))
        self.configDir = Path(self._getWinFolder(APPDATA))/'exe'

    def _getConfigPathOptions(self):
        """
        Returns the best options for the
        location of the config file under windows
        """
        # Find out where our nice config file is
        folders = map(self._getWinFolder, [APPDATA, COMMON_APPDATA])
        # Add unique dir names
        folders = [folder/'exe' for folder in folders] 
        folders.append(self.__getInstallDir())
        folders.append('.')
        # Filter out non existant folders
        options = [folder/'exe.conf' for folder in map(Path, folders)]
        return options
    
    def __getInstallDir(self):
        """
        Returns the path to where we were installed
        """
        from _winreg import OpenKey, QueryValue, HKEY_LOCAL_MACHINE
        try:
            exeKey = None
            softwareKey = None
            try:
                softwareKey = OpenKey(HKEY_LOCAL_MACHINE, 'SOFTWARE')
                exeKey = OpenKey(softwareKey, 'exe')
                return Path(QueryValue(exeKey, ''))
            finally:
                if exeKey:
                    exeKey.Close()
                if softwareKey:
                    softwareKey.Close()
        except WindowsError:
            return Path('')

    def getLongPathName(self, path):
        """
        Convert from Win32 short pathname to long pathname
        """
        from ctypes import windll, create_unicode_buffer
        buf = create_unicode_buffer(260)
        r = windll.kernel32.GetLongPathNameW(unicode(path), buf, 260)
        if r == 0 or r > 260:
            return path
        else:
            return buf.value

# ===========================================================================
