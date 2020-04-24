
#note: pyexe only can fullsupport python3.4 ,
#please use pyinstaller pyif you found tuple index out of range wiht python 3.6

from distutils.core import setup
import py2exe

setup(console= ['py_exe.py'] )
