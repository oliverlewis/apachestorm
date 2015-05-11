#!/usr/bin/env python

version = "1.0"


from setuptools import setup, find_packages
from setuptools.command.install import install
import glob
import os

package_name = "cloudmesh_apachestorm"

try:
    from cloudmesh_base.util import banner
except:
    os.system("pip install cloudmesh_base")

from cloudmesh_base.util import banner
from cloudmesh_base.util import path_expand
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import auto_create_version
from cloudmesh_base.util import auto_create_requirements


banner("Installing Cloudmesh " + package_name)

home = os.path.expanduser("~")

auto_create_version(package_name, version)


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


requirements = parse_requirements('requirements.txt')


class UploadToPypi(install):
    """Upload the package to pypi."""
    def run(self):
        os.system("Make clean Install")
        os.system("python setup.py.in install")
        banner("Build Distribution")
        os.system("python setup.py.in sdist --format=bztar,zip upload")


class RegisterWithPypi(install):
    """Upload the package to pypi."""
    def run(self):
        banner("Register with Pypi")
        os.system("python setup.py.in register")


class InstallBase(install):
    """Install the package."""
    def run(self):
        banner("Installing Cloudmesh " + package_name)
        install.run(self)


class InstallRequirements(install):
    """Install the requirements."""
    def run(self):
        banner("Installing Requirements for Cloudmesh " + package_name)
        os.system("pip install -r requirements.txt")


class InstallAll(install):
    """Install requirements and the package."""
    def run(self):
        banner("Installing Requirements for Cloudmesh " + package_name)
        os.system("pip install -r requirements.txt")
        banner("Installing Cloudmesh " + package_name)
        install.run(self)


data_files= [ (home + '/.cloudmesh/cloudmesh_apachestorm/' + d.lstrip('cloudmesh_apachestorm/'),
                [os.path.join(d, f) for f in files]) for d, folders, files in os.walk('cloudmesh_apachestorm/etc')]

# TODO: delete the copied over __init__.py file from the prefix

import fnmatch
import os

matches = []
for root, dirnames, filenames in os.walk('apachestorm/etc'):
  for filename in fnmatch.filter(filenames, '*'):
    matches.append(os.path.join(root, filename).lstrip('apachestorm/'))
data_dirs = matches


setup(
    name='MODULE',
    version=version,
    description='A set of simple base functions and classes useful for cloudmesh and other programs',
    # description-file =
    #    README.rst
    author='The Cloudmesh Team',
    author_email='laszewski@gmail.com',
    url='http://github.org/cloudmesh/base',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Clustering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Boot',
        'Topic :: System :: Systems Administration',
        'Framework :: Flask',
        'Environment :: OpenStack',
    ],
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    data_files= data_files,
    package_data={'apachestorm': data_dirs},
    cmdclass={
        'install': InstallBase,
        'requirements': InstallRequirements,
        'all': InstallAll,
        'pypi': UploadToPypi,
        'pypiregister': RegisterWithPypi,
        },
)

