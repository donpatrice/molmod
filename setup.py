#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MolMod is a collection of molecular modelling tools for python.
# Copyright (C) 2007 - 2012 Toon Verstraelen <Toon.Verstraelen@UGent.be>, Center
# for Molecular Modeling (CMM), Ghent University, Ghent, Belgium; all rights
# reserved unless otherwise stated.
#
# This file is part of MolMod.
#
# MolMod is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# MolMod is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--


import os
import subprocess
import sys
from glob import glob

import numpy as np
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
from distutils.command.install_data import install_data
import Cython.Build


# Try to get the version from git describe
__version__ = None
try:
    __version__ = subprocess.check_output(["git", "describe", "--tags"])
    __version__ = __version__.decode('utf-8').strip().replace('-', '_')
except subprocess.CalledProcessError:
    pass

# Interact with version.py
fn_version = os.path.join(os.path.dirname(__file__), 'molmod', 'version.py')
version_template = """\
\"""Do not edit this file, versioning is governed by ``git describe --tags`` and ``setup.py``.\"""
__version__ = '{}'
"""
if __version__ is None:
    # Try to load the git version tag from version.py
    try:
        with open(fn_version, 'r') as fh:
            __version__ = fh.read().split('=')[-1].replace('\'', '').strip()
    except IOError:
        print('Could not determine version. Giving up.')
        sys.exit(1)
else:
    # Store the git version tag in version.py
    with open(fn_version, 'w') as fh:
        fh.write(version_template.format(__version__))


class MyInstallData(install_data):
    """Add a datadir.txt file that points to the root for the data files. It is
       otherwise impossible to figure out the location of these data files at
       runtime.
    """
    def run(self):
        # Do the normal install_data
        install_data.run(self)
        # Create the file datadir.txt. It's exact content is only known
        # at installation time.
        dist = self.distribution
        libdir = dist.command_obj["install_lib"].install_dir
        for name in dist.packages:
            if '.' not in name:
                destination = os.path.join(libdir, name, "datadir.txt")
                print "Creating %s" % destination
                if not self.dry_run:
                    f = file(destination, "w")
                    print >> f, self.install_dir
                    f.close()


setup(
    name='molmod',
    version=__version__,
    description='MolMod is a collection of molecular modelling tools for python.',
    author='Toon Verstraelen',
    author_email='Toon.Verstraelen@UGent.be',
    url='http://molmod.ugent.be/code/',
    cmdclass={'install_data': MyInstallData, 'build_ext': Cython.Build.build_ext},
    package_dir = {'molmod': 'molmod'},
    packages=[
        'molmod', 'molmod.test',
        'molmod.io', 'molmod.io.test',
    ],
    data_files=[
        ('share/molmod', [
            "data/periodic.csv", "data/bonds.csv",
            "data/mass.mas03", "data/nubtab03.asc",
            "data/toyff_angles.txt"
        ]),
        ('share/molmod/test', glob('data/test/*')),
    ] + [
        ('share/molmod/examples/%s' % os.path.basename(dn), glob('%s/*.*' % dn))
        for dn in glob('data/examples/???_*')
    ],
    ext_modules=[
        Extension(
            "molmod.ext",
            sources=["molmod/ext.pyx", "molmod/common.c", "molmod/ff.c",
                     "molmod/graphs.c", "molmod/similarity.c", "molmod/molecules.c",
                     "molmod/unit_cells.c"],
            depends=["molmod/common.h", "molmod/ff.h", "molmod/ff.pxd", "molmod/graphs.h",
                     "molmod/graphs.pxd", "molmod/similarity.h", "molmod/similarity.pxd",
                     "molmod/molecules.h", "molmod/molecules.pxd", "molmod/unit_cells.h",
                     "molmod/unit_cells.pxd"],
            include_dirs=[np.get_include()],
         ),
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Science/Engineering :: Molecular Science'
    ],
)


