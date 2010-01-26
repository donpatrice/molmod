# MolMod is a collection of molecular modelling tools for python.
# Copyright (C) 2007 - 2010 Toon Verstraelen <Toon.Verstraelen@UGent.be>, Center
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
# --


from common import BaseTestCase

from molmod.io.gromacs import *
from molmod.units import *

import numpy


__all__ = ["GromacsTestCase"]


class GromacsTestCase(BaseTestCase):
    def test_reader(self):
        gr = GroReader("input/water2.gro")
        gr.next() # skip one
        for time, pos, vel, cell in gr:
            self.assertAlmostEqual(time/picosecond, 1.0)
            self.assertAlmostEqual(pos[0,1]/nanometer, 1.624,6)
            self.assertAlmostEqual(vel[3,2]/nanometer*picosecond, -0.1734)
            self.assertAlmostEqual(cell[0,0]/nanometer, 1.82060)
            break


