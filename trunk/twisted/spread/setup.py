from distutils.core import setup, Extension

module1 = Extension("cBanana", sources = ['cBanana.c'])

setup (name = "cBanana",
       version = '1.0',
       description = "cBanana from twisted",
       ext_modules = [module1])


