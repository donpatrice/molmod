# MolMod is a collection of molecular modelling tools for python.
# Copyright (C) 2005 Toon Verstraelen
#
# This file is part of MolMod.
#
# MolMod is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# --


from molmod.flexff import *
from ccop.xyz import XYZFile
from molmod.molecular_graphs import MolecularGraph, HasAtomNumber, MolecularAnd, HasNeighborNumbers
from molmod.molecules import Molecule
from molmod.unit_cell import UnitCell
from molmod.units import angstrom

import unittest, numpy, math


__all__ = ["FlexFFTestCase"]


class FlexFFTestCase(unittest.TestCase):
    def get_system(self, name):
        if name == "chabazite_octane":
            molecule = XYZFile("input/chabazite_octane.xyz").get_molecule()
            unit_cell = UnitCell(
                numpy.array([
                    [14.767, 0, 0],
                    [0, 23.686, 0],
                    [0, 0, 13.675],
                ])*angstrom,
                numpy.array([True, True, True], bool),
            )
            molecular_graph = MolecularGraph(molecule)
            return molecule.coordinates, molecular_graph, unit_cell
        elif name == "sodalite_ethane":
            molecule = XYZFile("input/sodalite_ethane.xyz").get_molecule()
            unit_cell = UnitCell(
                numpy.array([
                    [8.956, 0, 0],
                    [0, 8.956, 0],
                    [0, 0, 8.956],
                ])*angstrom,
                numpy.array([True, True, True], bool),
            )
            molecular_graph = MolecularGraph(molecule)
            return molecule.coordinates, molecular_graph, unit_cell
        else:
            raise Exception("Unknown system.")

    def get_gcm(self):
        criteria = {
            "C": HasAtomNumber(6),
            "Hc": MolecularAnd(HasAtomNumber(1),HasNeighborNumbers([6])),
            "Si": HasAtomNumber(14),
            "O": HasAtomNumber(8),
            "Ho": MolecularAnd(HasAtomNumber(1),HasNeighborNumbers([8])),
        }
        def gc(*symbols):
            return [criteria[symbol] for symbol in symbols]

        filter14 = (lambda n: n==0 or n >= 4)
        filter13 = (lambda n: n==0 or n >= 3)
        cutoff = 8.0*angstrom

        return [
            NonbondTerm("CC_nonbond", (lambda q: ((((-0.00010285843695)*q**(-1)) + (0.00106760594993*q**(-2)) + (0.0153188176448*q**(-3)) + ((-0.103465419057)*q**(-4)) + ((-4.57468402587)*q**(-5)) + ((-57.5937848714)*q**(-6)) + ((-377.191433235)*q**(-7)) + ((-567.749456207)*q**(-8)) + (16946.1527528*q**(-9)) + (231373.78203*q**(-10))), ((0.00010285843695*q**(-2)) + ((-0.00213521189986)*q**(-3)) + ((-0.0459564529345)*q**(-4)) + (0.413861676227*q**(-5)) + (22.8734201293*q**(-6)) + (345.562709228*q**(-7)) + (2640.34003265*q**(-8)) + (4541.99564966*q**(-9)) + ((-152515.374775)*q**(-10)) + ((-2313737.8203)*q**(-11))))), gc("C", "C"), filter14, cutoff),
            NonbondTerm("CHc_nonbond", (lambda q: ((((-6.79405707369e-05)*q**(-1)) + (0.00603834435677*q**(-2)) + ((-0.243829312005)*q**(-3)) + (5.8647327508*q**(-4)) + ((-87.0906441875)*q**(-5)) + (803.66952513*q**(-6)) + ((-4831.78404124)*q**(-7)) + (18002.8414089*q**(-8)) + ((-35899.7428532)*q**(-9)) + (29146.0343697*q**(-10))), ((6.79405707369e-05*q**(-2)) + ((-0.0120766887135)*q**(-3)) + (0.731487936014*q**(-4)) + ((-23.4589310032)*q**(-5)) + (435.453220938*q**(-6)) + ((-4822.01715078)*q**(-7)) + (33822.4882887*q**(-8)) + ((-144022.731271)*q**(-9)) + (323097.685679*q**(-10)) + ((-291460.343697)*q**(-11))))), gc("C", "Hc"), filter14, cutoff),
            NonbondTerm("CSi_nonbond", (lambda q: (((0.000357386899716*q**(-1)) + (0.0682098995626*q**(-2)) + (0.343595460021*q**(-3)) + ((-1.68015917792)*q**(-4)) + ((-29.3103753296)*q**(-5)) + ((-162.015188858)*q**(-6)) + ((-395.670757538)*q**(-7)) + (672.518086*q**(-8)) + (11245.9157908*q**(-9)) + (57424.4399919*q**(-10))), (((-0.000357386899716)*q**(-2)) + ((-0.136419799125)*q**(-3)) + ((-1.03078638006)*q**(-4)) + (6.72063671168*q**(-5)) + (146.551876648*q**(-6)) + (972.091133146*q**(-7)) + (2769.69530277*q**(-8)) + ((-5380.144688)*q**(-9)) + ((-101213.242117)*q**(-10)) + ((-574244.399919)*q**(-11))))), gc("C", "Si"), filter14, cutoff),
            NonbondTerm("CO_nonbond", (lambda q: ((((-0.000801753954104)*q**(-1)) + ((-0.00289999701532)*q**(-2)) + ((-0.147915724447)*q**(-3)) + ((-1.50211631966)*q**(-4)) + ((-3.48742912283)*q**(-5)) + (35.9400214381*q**(-6)) + (358.790991605*q**(-7)) + (1583.52138638*q**(-8)) + (2742.59838323*q**(-9)) + ((-18012.3521758)*q**(-10))), ((0.000801753954104*q**(-2)) + (0.00579999403063*q**(-3)) + (0.44374717334*q**(-4)) + (6.00846527862*q**(-5)) + (17.4371456141*q**(-6)) + ((-215.640128629)*q**(-7)) + ((-2511.53694124)*q**(-8)) + ((-12668.1710911)*q**(-9)) + ((-24683.3854491)*q**(-10)) + (180123.521758*q**(-11))))), gc("C", "O"), filter14, cutoff),
            NonbondTerm("CHo_nonbond", (lambda q: ((((-0.000272283340219)*q**(-1)) + (0.00969319618634*q**(-2)) + ((-0.00787291020275)*q**(-3)) + ((-0.770304262403)*q**(-4)) + ((-4.86808707695)*q**(-5)) + ((-13.0580831063)*q**(-6)) + ((-7.29516401488)*q**(-7)) + (89.2328792629*q**(-8)) + (525.860217713*q**(-9)) + (2189.70612975*q**(-10))), ((0.000272283340219*q**(-2)) + ((-0.0193863923727)*q**(-3)) + (0.0236187306083*q**(-4)) + (3.08121704961*q**(-5)) + (24.3404353848*q**(-6)) + (78.3484986378*q**(-7)) + (51.0661481042*q**(-8)) + ((-713.863034103)*q**(-9)) + ((-4732.74195942)*q**(-10)) + ((-21897.0612975)*q**(-11))))), gc("C", "Ho"), filter14, cutoff),
            NonbondTerm("HcHc_nonbond", (lambda q: ((((-8.19310395506e-05)*q**(-1)) + (0.00712353056597*q**(-2)) + ((-0.247338009997)*q**(-3)) + (4.86995222695*q**(-4)) + ((-58.4879433579)*q**(-5)) + (432.581255689*q**(-6)) + ((-2019.16783725)*q**(-7)) + (5843.06563184*q**(-8)) + ((-9094.7077725)*q**(-9)) + (5653.24249392*q**(-10))), ((8.19310395506e-05*q**(-2)) + ((-0.0142470611319)*q**(-3)) + (0.742014029991*q**(-4)) + ((-19.4798089078)*q**(-5)) + (292.439716789*q**(-6)) + ((-2595.48753413)*q**(-7)) + (14134.1748607*q**(-8)) + ((-46744.5250547)*q**(-9)) + (81852.3699525*q**(-10)) + ((-56532.4249392)*q**(-11))))), gc("Hc", "Hc"), filter14, cutoff),
            NonbondTerm("HcSi_nonbond", (lambda q: ((((-0.0736155412793)*q**(-1)) + (5.12312046976*q**(-2)) + ((-149.892844497)*q**(-3)) + (2474.97873355*q**(-4)) + ((-25293.2199857)*q**(-5)) + (166321.490862*q**(-6)) + ((-704975.377313)*q**(-7)) + (1862493.34368*q**(-8)) + ((-2785270.93099)*q**(-9)) + (1796054.0327*q**(-10))), ((0.0736155412793*q**(-2)) + ((-10.2462409395)*q**(-3)) + (449.678533491*q**(-4)) + ((-9899.91493419)*q**(-5)) + (126466.099929*q**(-6)) + ((-997928.945172)*q**(-7)) + (4934827.64119*q**(-8)) + ((-14899946.7494)*q**(-9)) + (25067438.3789*q**(-10)) + ((-17960540.327)*q**(-11))))), gc("Hc", "Si"), filter14, cutoff),
            NonbondTerm("HcO_nonbond", (lambda q: ((((-0.116303149849)*q**(-1)) + (7.30409289304*q**(-2)) + ((-193.258510456)*q**(-3)) + (2824.30915763*q**(-4)) + ((-25234.2733437)*q**(-5)) + (143267.181527*q**(-6)) + ((-518563.789651)*q**(-7)) + (1158349.13438*q**(-8)) + ((-1452731.92738)*q**(-9)) + (780953.236887*q**(-10))), ((0.116303149849*q**(-2)) + ((-14.6081857861)*q**(-3)) + (579.775531368*q**(-4)) + ((-11297.2366305)*q**(-5)) + (126171.366719*q**(-6)) + ((-859603.089164)*q**(-7)) + (3629946.52756*q**(-8)) + ((-9266793.07504)*q**(-9)) + (13074587.3464*q**(-10)) + ((-7809532.36887)*q**(-11))))), gc("Hc", "O"), filter14, cutoff),
            NonbondTerm("HcHo_nonbond", (lambda q: ((((-0.0168320851806)*q**(-1)) + (1.07781010617*q**(-2)) + ((-28.6391391053)*q**(-3)) + (421.267472196*q**(-4)) + ((-3773.96185987)*q**(-5)) + (21445.100352*q**(-6)) + ((-77520.4769375)*q**(-7)) + (172648.147008*q**(-8)) + ((-215627.28935)*q**(-9)) + (115302.775111*q**(-10))), ((0.0168320851806*q**(-2)) + ((-2.15562021234)*q**(-3)) + (85.9174173158*q**(-4)) + ((-1685.06988878)*q**(-5)) + (18869.8092994*q**(-6)) + ((-128670.602112)*q**(-7)) + (542643.338563*q**(-8)) + ((-1381185.17606)*q**(-9)) + (1940645.60415*q**(-10)) + ((-1153027.75111)*q**(-11))))), gc("Hc", "Ho"), filter14, cutoff),
            NonbondTerm("SiSi_nonbond", (lambda q: ((((-0.00590775067428)*q**(-1)) + (0.0225014502814*q**(-2)) + (0.415306107986*q**(-3)) + (0.9820582546*q**(-4)) + ((-29.8470490202)*q**(-5)) + ((-483.373661879)*q**(-6)) + ((-4244.28611754)*q**(-7)) + ((-22073.8523416)*q**(-8)) + (19424.7989518*q**(-9)) + (2256168.04335*q**(-10))), ((0.00590775067428*q**(-2)) + ((-0.0450029005627)*q**(-3)) + ((-1.24591832396)*q**(-4)) + ((-3.9282330184)*q**(-5)) + (149.235245101*q**(-6)) + (2900.24197128*q**(-7)) + (29710.0028228*q**(-8)) + (176590.818733*q**(-9)) + ((-174823.190566)*q**(-10)) + ((-22561680.4335)*q**(-11))))), gc("Si", "Si"), filter14, cutoff),
            NonbondTerm("SiSi_coulomb", (lambda q: ((2.3104*q**(-1)), ((-2.3104)*q**(-2)))), gc("Si", "Si"), filter13, cutoff),
            NonbondTerm("SiO_nonbond", (lambda q: ((((-0.0554790771797)*q**(-1)) + (5.09921176945*q**(-2)) + ((-201.020307842)*q**(-3)) + (4458.49407389*q**(-4)) + ((-61337.4608396)*q**(-5)) + (543717.763033*q**(-6)) + ((-3111230.76229)*q**(-7)) + (11106763.4322*q**(-8)) + ((-22466229.5101)*q**(-9)) + (19615252.5789*q**(-10))), ((0.0554790771797*q**(-2)) + ((-10.1984235389)*q**(-3)) + (603.060923525*q**(-4)) + ((-17833.9762956)*q**(-5)) + (306687.304198*q**(-6)) + ((-3262306.5782)*q**(-7)) + (21778615.3361*q**(-8)) + ((-88854107.458)*q**(-9)) + (202196065.591*q**(-10)) + ((-196152525.789)*q**(-11))))), gc("Si", "O"), filter13, cutoff),
            NonbondTerm("SiO_coulomb", (lambda q: (((-1.1552)*q**(-1)), (1.1552*q**(-2)))), gc("Si", "O"), filter13, cutoff),
            NonbondTerm("SiHo_nonbond", (lambda q: (((0.000190537354576*q**(-1)) + (0.00522536784613*q**(-2)) + (0.0108333835809*q**(-3)) + ((-0.213462318669)*q**(-4)) + ((-2.34267866631)*q**(-5)) + ((-14.1983909642)*q**(-6)) + ((-59.7196654491)*q**(-7)) + ((-100.694075109)*q**(-8)) + (1463.84186009*q**(-9)) + (23601.1789917*q**(-10))), (((-0.000190537354576)*q**(-2)) + ((-0.0104507356923)*q**(-3)) + ((-0.0325001507427)*q**(-4)) + (0.853849274674*q**(-5)) + (11.7133933315*q**(-6)) + (85.1903457849*q**(-7)) + (418.037658144*q**(-8)) + (805.552600869*q**(-9)) + ((-13174.5767408)*q**(-10)) + ((-236011.789917)*q**(-11))))), gc("Si", "Ho"), filter14, cutoff),
            NonbondTerm("SiHo_coulomb", (lambda q: ((0.5776*q**(-1)), ((-0.5776)*q**(-2)))), gc("Si", "Ho"), filter13, cutoff),
            NonbondTerm("OO_nonbond", (lambda q: (((0.00011934874442*q**(-1)) + (0.000881657062474*q**(-2)) + ((-0.065338435779)*q**(-3)) + ((-0.959882041412)*q**(-4)) + ((-5.31504951943)*q**(-5)) + ((-1.02251360471)*q**(-6)) + (200.08161139*q**(-7)) + (1629.10047254*q**(-8)) + (5833.95444082*q**(-9)) + ((-14957.9962996)*q**(-10))), (((-0.00011934874442)*q**(-2)) + ((-0.00176331412495)*q**(-3)) + (0.196015307337*q**(-4)) + (3.83952816565*q**(-5)) + (26.5752475972*q**(-6)) + (6.13508162826*q**(-7)) + ((-1400.57127973)*q**(-8)) + ((-13032.8037803)*q**(-9)) + ((-52505.5899674)*q**(-10)) + (149579.962996*q**(-11))))), gc("O", "O"), filter14, cutoff),
            NonbondTerm("OO_coulomb", (lambda q: ((0.5776*q**(-1)), ((-0.5776)*q**(-2)))), gc("O", "O"), filter13, cutoff),
            NonbondTerm("OHo_nonbond", (lambda q: ((((-0.00189459968478)*q**(-1)) + (0.147222675777*q**(-2)) + ((-4.36631734278)*q**(-3)) + (68.6794218725*q**(-4)) + ((-664.760658196)*q**(-5)) + (4012.93275503*q**(-6)) + ((-15307.6396171)*q**(-7)) + (35824.9574422*q**(-8)) + ((-46607.0750454)*q**(-9)) + (25707.733031*q**(-10))), ((0.00189459968478*q**(-2)) + ((-0.294445351554)*q**(-3)) + (13.0989520284*q**(-4)) + ((-274.71768749)*q**(-5)) + (3323.80329098*q**(-6)) + ((-24077.5965302)*q**(-7)) + (107153.47732*q**(-8)) + ((-286599.659538)*q**(-9)) + (419463.675409*q**(-10)) + ((-257077.33031)*q**(-11))))), gc("O", "Ho"), filter13, cutoff),
            NonbondTerm("OHo_coulomb", (lambda q: (((-0.2888)*q**(-1)), (0.2888*q**(-2)))), gc("O", "Ho"), filter13, cutoff),
            NonbondTerm("HoHo_nonbond", (lambda q: ((((-0.0508102415326)*q**(-1)) + (3.67681886432*q**(-2)) + ((-107.948941202)*q**(-3)) + (1722.51364341*q**(-4)) + ((-16539.3212397)*q**(-5)) + (99641.5350164*q**(-6)) + ((-378664.046288)*q**(-7)) + (880130.049901*q**(-8)) + ((-1140850.85013)*q**(-9)) + (630991.488146*q**(-10))), ((0.0508102415326*q**(-2)) + ((-7.35363772864)*q**(-3)) + (323.846823607*q**(-4)) + ((-6890.05457366)*q**(-5)) + (82696.6061983*q**(-6)) + ((-597849.210098)*q**(-7)) + (2650648.32402*q**(-8)) + ((-7041040.39921)*q**(-9)) + (10267657.6512*q**(-10)) + ((-6309914.88146)*q**(-11))))), gc("Ho", "Ho"), filter14, cutoff),
            NonbondTerm("HoHo_coulomb", (lambda q: ((0.1444*q**(-1)), ((-0.1444)*q**(-2)))), gc("Ho", "Ho"), filter13, cutoff),
            BondStretchTerm("CHc_bond", (lambda q: (((1.1850257698*q**(-1)) + ((-8.00371826001)*q**(-2)) + (13.0107681545*q**(-3)) + ((-5.67536327462)*q**(-4))), (((-1.1850257698)*q**(-2)) + (16.00743652*q**(-3)) + ((-39.0323044636)*q**(-4)) + (22.7014530985*q**(-5))))), gc("C", "Hc")),
            BondStretchTerm("CC_bond", (lambda q: (((0.830873310288*q**(-1)) + (2.04065952719*q**(-2)) + ((-28.3928039246)*q**(-3)) + (48.0749714443*q**(-4))), (((-0.830873310288)*q**(-2)) + ((-4.08131905439)*q**(-3)) + (85.1784117737*q**(-4)) + ((-192.299885777)*q**(-5))))), gc("C", "C")),
            BondStretchTerm("SiO_bond", (lambda q: (((0.776542023552*q**(-1)) + (0.651652346322*q**(-2)) + ((-34.0778832976)*q**(-3)) + (71.2093541589*q**(-4))), (((-0.776542023552)*q**(-2)) + ((-1.30330469264)*q**(-3)) + (102.233649893*q**(-4)) + ((-284.837416636)*q**(-5))))), gc("Si", "O")),
            BondStretchTerm("OHo_bond", (lambda q: (((1.51587649357*q**(-1)) + ((-8.49660027342)*q**(-2)) + (11.9766296564*q**(-3)) + ((-4.59451918516)*q**(-4))), (((-1.51587649357)*q**(-2)) + (16.9932005468*q**(-3)) + ((-35.9298889692)*q**(-4)) + (18.3780767406*q**(-5))))), gc("O", "Ho")),
            BendingCosineTerm("HcCHc_bend", (lambda q: (((-0.0774205063635) + (0.0331613707696*q) + (0.0486416679525*q**2) + ((-0.0110244868062)*q**3)), (0.0331613707696 + (0.097283335905*q) + ((-0.0330734604185)*q**2)))), gc("Hc", "C", "Hc")),
            UreyBradleyTerm("HcCHc_span", (lambda q: (((1.80755401956*q**(-1)) + ((-18.746529676)*q**(-2)) + (76.9595992123*q**(-3)) + ((-153.060024135)*q**(-4)) + (146.732797538*q**(-5)) + ((-52.0301994455)*q**(-6))), (((-1.80755401956)*q**(-2)) + (37.4930593519*q**(-3)) + ((-230.878797637)*q**(-4)) + (612.240096541*q**(-5)) + ((-733.663987691)*q**(-6)) + (312.181196673*q**(-7))))), gc("Hc", "C", "Hc")),
            BendingCosineTerm("HcCC_bend", (lambda q: (((-0.0533422188737) + (0.0440446728273*q) + (0.049231118776*q**2) + ((-0.0247810626446)*q**3)), (0.0440446728273 + (0.0984622375521*q) + ((-0.0743431879338)*q**2)))), gc("Hc", "C", "C")),
            UreyBradleyTerm("HcCC_span", (lambda q: (((1.34221287632*q**(-1)) + ((-9.10502825287)*q**(-2)) + (21.2769008863*q**(-3)) + ((-11.9604542193)*q**(-4))), (((-1.34221287632)*q**(-2)) + (18.2100565057*q**(-3)) + ((-63.830702659)*q**(-4)) + (47.8418168772*q**(-5))))), gc("Hc", "C", "C")),
            BendingCosineTerm("CCC_bend", (lambda q: (((-0.0310603546078) + (0.0650680429641*q) + (0.0397869353751*q**2) + ((-0.0667948363661)*q**3)), (0.0650680429641 + (0.0795738707503*q) + ((-0.200384509098)*q**2)))), gc("C", "C", "C")),
            UreyBradleyTerm("CCC_span", (lambda q: (((2.62165913015*q**(-1)) + (9.62076832794*q**(-2)) + ((-138.344364869)*q**(-3)) + (314.200546892*q**(-4))), (((-2.62165913015)*q**(-2)) + ((-19.2415366559)*q**(-3)) + (415.033094607*q**(-4)) + ((-1256.80218757)*q**(-5))))), gc("C", "C", "C")),
            BendingCosineTerm("SiOSi_bend", (lambda q: ((0.0161348206173 + (0.0226728952652*q) + (0.0153398274977*q**2) + (0.00779928757664*q**3)), (0.0226728952652 + (0.0306796549954*q) + (0.0233978627299*q**2)))), gc("Si", "O", "Si")),
            UreyBradleyTerm("SiOSi_span", (lambda q: (((10.1267531464*q**(-1)) + (10.7536327854*q**(-2)) + ((-420.100806334)*q**(-3)) + (1239.79098121*q**(-4))), (((-10.1267531464)*q**(-2)) + ((-21.5072655709)*q**(-3)) + (1260.302419*q**(-4)) + ((-4959.16392482)*q**(-5))))), gc("Si", "O", "Si")),
            BendingCosineTerm("OSiO_bend", (lambda q: (((-0.075186269622) + (0.0680057462837*q) + (0.0899624438739*q**2) + (0.0052539830334*q**3)), (0.0680057462837 + (0.179924887748*q) + (0.0157619491002*q**2)))), gc("O", "Si", "O")),
            UreyBradleyTerm("OSiO_span", (lambda q: (((1.53504643653*q**(-1)) + ((-11.7078080597)*q**(-2)) + (21.5312099026*q**(-3)) + (19.6001114662*q**(-4))), (((-1.53504643653)*q**(-2)) + (23.4156161194*q**(-3)) + ((-64.5936297079)*q**(-4)) + ((-78.4004458648)*q**(-5))))), gc("O", "Si", "O")),
            BendingCosineTerm("SiOHo_bend", (lambda q: (((-0.0215868829721) + (0.0140569197437*q) + (0.00572625667207*q**2) + ((-0.0138633214349)*q**3)), (0.0140569197437 + (0.0114525133441*q) + ((-0.0415899643047)*q**2)))), gc("Si", "O", "Ho")),
            UreyBradleyTerm("SiOHo_span", (lambda q: ((((-1.64634848807)*q**(-1)) + (35.959407274*q**(-2)) + ((-179.117367853)*q**(-3)) + (283.508480599*q**(-4))), ((1.64634848807*q**(-2)) + ((-71.9188145481)*q**(-3)) + (537.352103558*q**(-4)) + ((-1134.0339224)*q**(-5))))), gc("Si", "O", "Ho")),
            DihedralCosineTerm("HcCCHc_dihed", (lambda q: ((0.0302200282399 + ((-0.00430880719367)*q) + ((-0.00374498105177)*q**2) + (0.00085852777194*q**3) + (0.000135273632125*q**4)), ((-0.00430880719367) + ((-0.00748996210353)*q) + (0.00257558331582*q**2) + (0.000541094528501*q**3)))), gc("Hc", "C", "C", "Hc")),
            OneFourTerm("HcHc_nonbond14", (lambda q: ((((-0.00145401171262)*q**(-1)) + (0.102750800031*q**(-2)) + ((-2.65840321051)*q**(-3)) + (36.5277443771*q**(-4)) + ((-309.936749171)*q**(-5)) + (1696.29773575*q**(-6)) + ((-6030.59065733)*q**(-7)) + (13518.0078871*q**(-8)) + ((-17348.5368741)*q**(-9)) + (9706.23686837*q**(-10))), ((0.00145401171262*q**(-2)) + ((-0.205501600063)*q**(-3)) + (7.97520963154*q**(-4)) + ((-146.110977508)*q**(-5)) + (1549.68374586*q**(-6)) + ((-10177.7864145)*q**(-7)) + (42214.1346013*q**(-8)) + ((-108144.063097)*q**(-9)) + (156136.831867*q**(-10)) + ((-97062.3686837)*q**(-11))))), gc("Hc", "C", "C", "Hc")),
            DihedralCosineTerm("CCCHc_dihed", (lambda q: ((0.0305927326822 + ((-0.00683579601553)*q) + ((-0.00383964690045)*q**2) + (0.00208067062392*q**3) + (0.0001633147977*q**4)), ((-0.00683579601553) + ((-0.0076792938009)*q) + (0.00624201187177*q**2) + (0.000653259190799*q**3)))), gc("C", "C", "C", "Hc")),
            OneFourTerm("CHc_nonbond14", (lambda q: (((0.00270467555993*q**(-1)) + (0.0128697368764*q**(-2)) + (0.0407965382833*q**(-3)) + (0.051903179305*q**(-4)) + ((-0.374214264667)*q**(-5)) + ((-3.60815743644)*q**(-6)) + ((-18.5844883106)*q**(-7)) + ((-59.3022119505)*q**(-8)) + (6.90647746297*q**(-9)) + (1942.6854226*q**(-10))), (((-0.00270467555993)*q**(-2)) + ((-0.0257394737528)*q**(-3)) + ((-0.12238961485)*q**(-4)) + ((-0.20761271722)*q**(-5)) + (1.87107132334*q**(-6)) + (21.6489446186*q**(-7)) + (130.091418174*q**(-8)) + (474.417695604*q**(-9)) + ((-62.1582971668)*q**(-10)) + ((-19426.854226)*q**(-11))))), gc("C", "C", "C", "Hc")),
            DihedralCosineTerm("CCCC_dihed", (lambda q: ((0.0570666839068 + ((-0.0114744958062)*q) + ((-0.00226484625972)*q**2) + (0.00465418453724*q**3) + ((-0.000523736736229)*q**4)), ((-0.0114744958062) + ((-0.00452969251944)*q) + (0.0139625536117*q**2) + ((-0.00209494694492)*q**3)))), gc("C", "C", "C", "C")),
            OneFourTerm("CC_nonbond14", (lambda q: ((((-32.6049423322)*q**(-1)) + (2174.04358044*q**(-2)) + ((-63109.6381748)*q**(-3)) + (1050093.49612*q**(-4)) + ((-11062984.0042)*q**(-5)) + (76661810.4685*q**(-6)) + ((-349887921.048)*q**(-7)) + (1015297070.44*q**(-8)) + ((-1701178001.15)*q**(-9)) + (1254877736.06*q**(-10))), ((32.6049423322*q**(-2)) + ((-4348.08716087)*q**(-3)) + (189328.914524*q**(-4)) + ((-4200373.98449)*q**(-5)) + (55314920.0209*q**(-6)) + ((-459970862.811)*q**(-7)) + (2449215447.34*q**(-8)) + ((-8122376563.56)*q**(-9)) + (15310602010.3*q**(-10)) + ((-12548777360.6)*q**(-11))))), gc("C", "C", "C", "C")),
        ]

    def get_reduced(self):
        criteria = {
            "C": HasAtomNumber(6),
            "Hc": MolecularAnd(HasAtomNumber(1),HasNeighborNumbers([6])),
            "Si": HasAtomNumber(14),
            "O": HasAtomNumber(8),
            "Ho": MolecularAnd(HasAtomNumber(1),HasNeighborNumbers([8])),
        }
        def gc(*symbols):
            return [criteria[symbol] for symbol in symbols]

        filter14 = (lambda n: n==0 or n >= 4)
        filter13 = (lambda n: n==0 or n >= 3)
        cutoff = 15.0*angstrom

        return [
            NonbondTerm("CC_nonbond", (lambda q: ((((-0.00010285843695)*q**(-1)) + (0.00106760594993*q**(-2)) + (0.0153188176448*q**(-3)) + ((-0.103465419057)*q**(-4)) + ((-4.57468402587)*q**(-5)) + ((-57.5937848714)*q**(-6)) + ((-377.191433235)*q**(-7)) + ((-567.749456207)*q**(-8)) + (16946.1527528*q**(-9)) + (231373.78203*q**(-10))), ((0.00010285843695*q**(-2)) + ((-0.00213521189986)*q**(-3)) + ((-0.0459564529345)*q**(-4)) + (0.413861676227*q**(-5)) + (22.8734201293*q**(-6)) + (345.562709228*q**(-7)) + (2640.34003265*q**(-8)) + (4541.99564966*q**(-9)) + ((-152515.374775)*q**(-10)) + ((-2313737.8203)*q**(-11))))), gc("C", "C"), filter14, cutoff),
            BondStretchTerm("CHc_bond", (lambda q: (((1.1850257698*q**(-1)) + ((-8.00371826001)*q**(-2)) + (13.0107681545*q**(-3)) + ((-5.67536327462)*q**(-4))), (((-1.1850257698)*q**(-2)) + (16.00743652*q**(-3)) + ((-39.0323044636)*q**(-4)) + (22.7014530985*q**(-5))))), gc("C", "Hc")),
            BendingCosineTerm("HcCHc_bend", (lambda q: (((-0.0774205063635) + (0.0331613707696*q) + (0.0486416679525*q**2) + ((-0.0110244868062)*q**3)), (0.0331613707696 + (0.097283335905*q) + ((-0.0330734604185)*q**2)))), gc("Hc", "C", "Hc")),
            UreyBradleyTerm("HcCHc_span", (lambda q: (((1.80755401956*q**(-1)) + ((-18.746529676)*q**(-2)) + (76.9595992123*q**(-3)) + ((-153.060024135)*q**(-4)) + (146.732797538*q**(-5)) + ((-52.0301994455)*q**(-6))), (((-1.80755401956)*q**(-2)) + (37.4930593519*q**(-3)) + ((-230.878797637)*q**(-4)) + (612.240096541*q**(-5)) + ((-733.663987691)*q**(-6)) + (312.181196673*q**(-7))))), gc("Hc", "C", "Hc")),
            DihedralCosineTerm("HcCCHc_dihed", (lambda q: ((0.0302200282399 + ((-0.00430880719367)*q) + ((-0.00374498105177)*q**2) + (0.00085852777194*q**3) + (0.000135273632125*q**4)), ((-0.00430880719367) + ((-0.00748996210353)*q) + (0.00257558331582*q**2) + (0.000541094528501*q**3)))), gc("Hc", "C", "C", "Hc")),
            OneFourTerm("HcHc_nonbond14", (lambda q: ((((-0.00145401171262)*q**(-1)) + (0.102750800031*q**(-2)) + ((-2.65840321051)*q**(-3)) + (36.5277443771*q**(-4)) + ((-309.936749171)*q**(-5)) + (1696.29773575*q**(-6)) + ((-6030.59065733)*q**(-7)) + (13518.0078871*q**(-8)) + ((-17348.5368741)*q**(-9)) + (9706.23686837*q**(-10))), ((0.00145401171262*q**(-2)) + ((-0.205501600063)*q**(-3)) + (7.97520963154*q**(-4)) + ((-146.110977508)*q**(-5)) + (1549.68374586*q**(-6)) + ((-10177.7864145)*q**(-7)) + (42214.1346013*q**(-8)) + ((-108144.063097)*q**(-9)) + (156136.831867*q**(-10)) + ((-97062.3686837)*q**(-11))))), gc("Hc", "Hc")),
        ]

    def test_blind(self):
        coordinates, molecular_graph, unit_cell = self.get_system("sodalite_ethane")
        terms = self.get_reduced()
        ff = ForceField(molecular_graph, unit_cell, terms)
        ff(coordinates)

    def test_jacobians(self):
        terms = [
            (2, BondStretchTerm("test", lambda x: x, [None, None])),
            (3, BendingCosineTerm("test", lambda x: x, [None, None, None])),
            (3, UreyBradleyTerm("test", lambda x: x, [None, None, None])),
            (4, DihedralCosineTerm("test", lambda x: x, [None, None, None, None])),
            (4, OneFourTerm("test", lambda x: x, [None, None, None, None])),
        ]
        for n, term in terms:
            for counter in xrange(100):
                coordinates = numpy.random.uniform(-3,3,(n,3))
                ic1, jacobian1 = term.calculate_ic(coordinates)
                epsilon = 1e-4
                delta = numpy.random.uniform(-epsilon,epsilon,(n,3))
                ic2, jacobian2 = term.calculate_ic(coordinates + delta)
                error = abs((ic2 - ic1) - numpy.dot(0.5*(jacobian1+jacobian2).ravel(), delta.ravel()))
                oom = abs(ic2 - ic1)
                self.assert_(error/oom < 1e-4, "error=%s, oom=%s" % (error, oom))

    def test_gcm_gradients(self):
        for term in self.get_gcm():
            for counter in xrange(100):
                x = numpy.random.uniform(1, 2)
                epsilon = 1e-5
                e1, g1 = term.calculate_eg(x)
                e2, g2 = term.calculate_eg(x+epsilon)
                error = abs((e2-e1) - epsilon*0.5*(g1+g2))
                oom = abs(e2-e1)
                self.assert_(error/oom < 1e-4, "error=%s, oom=%s" % (error, oom))

    def test_ic_bond(self):
        term = BondStretchTerm("test", lambda x: x, [None, None])
        ic, foo = term.calculate_ic(numpy.array([[0.1, 1.0, 1.1], [1.1, 0.0, 0.1]], float))
        self.assert_(ic == numpy.sqrt(3.0))

    def test_ic_bend(self):
        term = BendingCosineTerm("test", lambda x: x, [None, None, None])
        ic, foo = term.calculate_ic(numpy.array([[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], float))
        self.assert_(ic == 0.0)
        ic, foo = term.calculate_ic(numpy.array([[0.0, 2.0, 0.0], [0.0, 0.0, 0.0], [0.0, -3.0, 0.0]], float))
        self.assert_(ic == -1.0)
        ic, foo = term.calculate_ic(numpy.array([[0.0, 2.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0]], float))
        self.assert_(ic == 1.0)

    def test_ic_ub(self):
        term = UreyBradleyTerm("test", lambda x: x, [None, None, None])
        ic, foo = term.calculate_ic(numpy.array([[0.1, 1.0, 1.1], [0.0, 0.0, 0.0], [1.1, 0.0, 0.1]], float))
        self.assert_(ic == numpy.sqrt(3.0))

    def test_ic_dihedral(self):
        term = DihedralCosineTerm("test", lambda x: x, [None, None, None, None])
        ic, foo = term.calculate_ic(numpy.array([[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0]], float))
        self.assert_(ic == 0.0)
        ic, foo = term.calculate_ic(numpy.array([[0.0, 2.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, -3.0, 1.0]], float))
        self.assert_(ic == -1.0)
        ic, foo = term.calculate_ic(numpy.array([[0.0, 2.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 1.0]], float))
        self.assert_(ic == 1.0)

    def test_ic_one_four(self):
        term = OneFourTerm("test", lambda x: x, [None, None, None, None])
        ic, foo = term.calculate_ic(numpy.array([[0.1, 1.0, 1.1], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.1, 0.0, 0.1]], float))
        self.assert_(ic == numpy.sqrt(3.0))

    def test_global_gradient(self):
        coordinates, molecular_graph, unit_cell = self.get_system("sodalite_ethane")
        terms = self.get_reduced()
        for term in terms:
            #print term.label
            ff = ForceField(molecular_graph, unit_cell, [term])
            for counter in xrange(3):
                #print counter
                epsilon = 1e-5
                e1, g1 = ff(coordinates)
                delta = numpy.random.uniform(-epsilon,epsilon,coordinates.shape)
                e2, g2 = ff(coordinates + delta)
                error = abs((e2-e1) - 0.5*numpy.dot(delta.ravel(), (g1+g2).ravel()))
                oom = abs(e2-e1)
                if error > 0:
                    #print error/oom, error, oom
                    self.assert_(error/oom < 1e-2, "error=%s, oom=%s" % (error, oom))

