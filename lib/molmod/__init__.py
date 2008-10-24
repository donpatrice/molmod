# MolMod is a collection of molecular modelling tools for python.
# Copyright (C) 2007 - 2008 Toon Verstraelen <Toon.Verstraelen@UGent.be>
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


import sys, os


__all__ = ["context"]


class Error(Exception):
    pass


class Context(object):
    def __init__(self):
        self.share_path = "%s/share/molmod/" % (sys.prefix)
        if not os.path.isdir(self.share_path):
            self.share_path = "%s/share/molmod/" % os.getenv("HOME")
        if not os.path.isdir(self.share_path):
            raise Error("Could not find shared files.")

context = Context()




