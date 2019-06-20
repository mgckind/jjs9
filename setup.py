import sys
import os
from subprocess import check_call
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
prjdir = os.path.dirname(__file__)

def read(filename):
    return open(os.path.join(prjdir, filename)).read()


class PostDevelop(develop):
    def run(self):
        if os.path.exists('js9server/js9ext.py'):
            check_call("rm -rf js9server/".split())
            develop.run(self)
        else:
            check_call("git clone https://github.com/ericmandel/js9.git js9server".split())
            check_call("cp js9ext.py js9server/.".split())
            check_call("cp index_jjs9.html js9server/.".split())
            check_call("touch js9server/__init__.py".split())
            develop.run(self)

class PostInstall(install):
    def run(self):
        if os.path.exists('js9server/js9ext.py'):
            check_call("rm -rf js9server/".split())
            install.run(self)
        else:
            check_call("git clone https://github.com/ericmandel/js9.git js9server".split())
            check_call("cp js9ext.py js9server/.".split())
            check_call("cp index_jjs9.html js9server/.".split())
            check_call("touch js9server/__init__.py".split())
            install.run(self)

extra_link_args = []
libraries = []
library_dirs = []
include_dirs = []
exec(open('version.py').read())
setup(
    name='jjs9',
    version=__version__,
    author='Matias Carrasco Kind ',
    author_email='mgckind@gmail.com',
    license='LICENSE.txt',
    include_package_data = True,
    scripts=[],
    cmdclass={
        'develop': PostDevelop,
        'install': PostInstall,
    },
    py_modules=['js9ext', 'jjs9'],
    packages=['js9server'],
)
