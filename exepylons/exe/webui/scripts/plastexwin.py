import sys,os
from plasTeX                  import TeX, TeXDocument
from plasTeX.Config           import config as texConfig
from plasTeX.Renderers.XHTML  import Renderer

FILE = sys.argv[1]
tempdir = sys.argv[2]
texConfig['files']['split-level'] = -10
texConfig['files']['filename'] = u'index$num(0).html'
texConfig['general']['theme'] = 'minimal'
cwd = os.getcwd()
os.chdir(tempdir)
document = TeXDocument(config = texConfig)
tex = TeX.TeX(document, file = FILE)
Renderer().render(tex.parse())
os.chdir(cwd)