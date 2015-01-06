def capture(grid_definition, maxlevel=1000):
    pcs = [PC(row, i) for i, row in enumerate(grid_definition)]

    number_of_ticks = 0
    virus = Virus(pcs)
    pcs[0].installed.add(virus.spread)
    virus.spread(pcs[0])
    while not all(virus in pc.installed for pc in pcs):
        for pc in pcs:
            pc.tick()
        number_of_ticks += 1
        if number_of_ticks > maxlevel: raise AssertionError("exceeded maximum number of ticks")

    return number_of_ticks


class PC:
    def __init__(self, row, i):
        self.__connections = [j for j, v in enumerate(row) if j != i and v]
        self.__security_level = row[i]
        self.connections = lambda: self.__connections
        self.security_level = lambda: self.__security_level
        self.state = self.clean
        self.installed = set()

    def tick(self):
        self.state()

    def install(self, program):
        if program in self.installed: pass
        if self.state != self.clean: pass
        counter = self.security_level()
        def countdown():
            nonlocal counter
            counter -= 1
            if counter == 0:
                program(self)
                self.installed.add(program)
                self.state = self.infected

        self.state = countdown

    def clean(self):
        pass

    def infected(self):
        pass


class Virus:
    def __init__(self, pcs):
        self.pcs = pcs

    def spread(self, pc):
        for c in pc.connections():
            self.pcs[c].install(self.spread)

from unittest import TestCase
from mockito import mock, verify, when
from mockito.mocking import mock

class TestCapture(TestCase):

    def test_PC_initialization(self):
        self.assertEqual([0, 2, 3], PC([1, 8, 1, 1, 0, 0], 1).connections())
        self.assertEqual(8, PC([1, 8, 1, 1, 0, 0], 1).security_level())

    def test_after_n_ticks_virus_spreads(self):
        pc = PC([1, 3, 1, 1, 0, 0], 1)
        virus = mock()
        pc.install(virus.execute)
        pc.tick()
        pc.tick()
        verify(virus, 0).execute(pc)
        pc.tick()
        verify(virus).execute(pc)

    def test_virus_spreads_to_connections(self):
        pc = mock()
        pcs = [pc, mock(), mock()]
        when(pc).connections().thenReturn([1, 2])
        v = Virus(pcs)
        v.spread(pc)

    def test_Given(self):
        self.assertEqual(capture(
            [[0, 1, 1],
             [1, 2, 1],
             [1, 1, 2]]), 2)
        self.assertEqual(capture(
            [[0, 1, 0, 1, 0, 1],
             [1, 8, 1, 0, 0, 0],
             [0, 1, 2, 0, 0, 1],
             [1, 0, 0, 1, 1, 0],
             [0, 0, 0, 1, 3, 1],
             [1, 0, 1, 0, 1, 2]]), 8)
        self.assertEqual(capture(
            [[0, 1, 0, 1, 0, 1],
             [1, 1, 1, 0, 0, 0],
             [0, 1, 2, 0, 0, 1],
             [1, 0, 0, 1, 1, 0],
             [0, 0, 0, 1, 3, 1],
             [1, 0, 1, 0, 1, 2]]), 4)

