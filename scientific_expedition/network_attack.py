from collections import defaultdict
from functools import partial

def capture(grid_definition, maxlevel=1000):

    pcs = [PC(row, i) for i, row in enumerate(grid_definition)]
    for pc in pcs:
        pc.update_connections(pcs)

    clock = Ticker()
    virus = Virus()
    pcs[0].infect(clock.time())
    virus.spread(pcs[0], clock)

    while any(not pc.infected(clock.time()) for pc in pcs):
        clock.tick()

    return max(pc.infected_time for pc in pcs)


class PC:
    def __init__(self, row, i):
        self.connected_indices = [j for j, v in enumerate(row) if j != i and v]
        self.security_level = lambda: row[i]
        self.infected_time = None

    def infected(self, t):
        if self.infected_time:
            return self.infected_time <= t
        else:
            return False

    def update_connections(self, pcs):
        self.__connections = [pcs[i] for i in self.connected_indices]

    def connections(self):
        return self.__connections

    def start_infection(self, virus, clock):
        infection_done = clock.time() + self.security_level()
        if self.infect(infection_done):
            clock.schedule(infection_done, partial(virus.spread, self, clock))

    def infect(self, time):
        if not self.infected_time:
            self.infected_time = time
            return True
        else:
            return False


class Virus:
    def spread(self, origin, clock):
        for target in origin.connections():
            target.start_infection(self, clock)


class Ticker:
    def __init__(self, t=0):
        self.q = defaultdict()
        self.__time = t

    def time(self):
        return self.__time

    def schedule(self, time, task):
        tasks = self.q.get(time, [])
        tasks.append(task)
        self.q[time] = tasks

    def tick(self):
        for t in self.q.get(self.__time, []):
            t()
        self.__time += 1



from unittest import TestCase
from mockito import mock, verify, when
from mockito.mocking import mock
from mockito.matchers import any as matchany

class TestCapture(TestCase):


    def test_clock_executes_when_time_is_due(self):
        m = mock()
        c = Ticker(9)
        c.schedule(10, m.exec)
        c.schedule(10, m.exec)
        c.tick()
        verify(m, 0).exec()
        c.tick()
        verify(m, 2).exec()

    def test_spreading_schedules_after_due_time(self):
        clock = mock()
        pc = mock()
        connections = [mock(), mock()]
        for target in connections:
            when(target).connections().thenReturn([])
            when(target).security_level().thenReturn(1)
            when(target).infect(6).thenReturn(True)
        when(pc).connections().thenReturn(connections)
        when(clock).time().thenReturn(5)

        v = Virus()
        v.spread(pc, clock)

        verify(clock, 2).schedule(6, matchany())

    def test_PC_initialization(self):
        pc = PC([1, 8, 1, 1, 0, 0], 1)
        pcs = [mock(), mock(), mock(), mock(), mock(), mock()]
        pc.update_connections(pcs)
        self.assertEqual([pcs[0], pcs[2], pcs[3]], pc.connections())
        self.assertEqual(8, pc.security_level())

    def test_pc_infection_takes_time(self):
        pc = PC([1, 8, 1, 1, 0, 0], 1)
        pc.infect(10)
        self.assertEqual(10, pc.infected_time)
        self.assertFalse(pc.infected(9))
        self.assertTrue(pc.infected(10))
        self.assertTrue(pc.infected(11))

    def test_virus_spreads_to_connections(self):
        pc = mock()
        clock = mock()
        pcs = [mock()]
        for pc in pcs:
            when(pc).infect(any()).thenReturn(True)
            when(pc).security_level().thenReturn(6)
        when(pc).connections().thenReturn(pcs)
        v = Virus()
        when(clock).time().thenReturn(5)
        v.spread(pc, clock)
        verify(clock).schedule(11, matchany())

    def test_Given(self):
        self.assertEqual(capture(
            [[0, 1, 1],
             [1, 2, 1],
             [1, 1, 2]]), 2)
        self.assertEqual(capture(
            [[0, 1, 1],
             [1, 3, 1],
             [1, 1, 2]]), 3)
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

