from distutils.core import setup
import py2exe

setup(console=['plastexwin.py'], options = {"py2exe": {"skip_archive":1}})