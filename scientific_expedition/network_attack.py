from collections import defaultdict
from functools import partial


def capture(grid_definition):
    clock = Clock()

    pcs = [PC(row, i, clock) for i, row in enumerate(grid_definition)]
    for pc in pcs:
        pc.update_connections(pcs)

    pcs[0].infected_time = clock.time()
    spread_virus(pcs[0].connections())

    while any(not pc.infected() for pc in pcs):
        clock.tick()

    return max(pc.infected_time for pc in pcs)


class PC:
    def __init__(self, row, i, clock):
        self.__connected_indices = [j for j, v in enumerate(row) if j != i and v]
        self.security_level = row[i]
        self.infected_time = None
        self.clock = clock

    def update_connections(self, pcs):
        self.__connections = [pcs[i] for i in self.__connected_indices]

    def infected(self):
        return self.infected_time != None and \
               self.infected_time <= self.clock.time()

    def connections(self):
        return self.__connections

    def start_infection(self, virus):
        infection_done = self.clock.time() + self.security_level
        if self.infect(infection_done):
            self.clock.schedule(infection_done, partial(virus, self.__connections))

    def infect(self, time):
        if not self.infected_time:
            self.infected_time = time
            return True
        else:
            return False


def spread_virus(connections):
    for target in connections:
        target.start_infection(spread_virus)


class Clock:
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

class TestCapture(TestCase):


    def test_clock_executes_when_time_is_due(self):
        m = mock()
        c = Clock(9)
        c.schedule(10, m.exec)
        c.schedule(10, m.exec)
        c.tick()
        verify(m, 0).exec()
        c.tick()
        verify(m, 2).exec()

    def test_PC_initialization(self):
        pc = PC([1, 8, 1, 1, 0, 0], 1, mock())
        pcs = [mock(), mock(), mock(), mock(), mock(), mock()]
        pc.update_connections(pcs)
        self.assertEqual([pcs[0], pcs[2], pcs[3]], pc.connections())
        self.assertEqual(8, pc.security_level)

    def test_pc_infection_takes_time(self):
        clock = mock()
        pc = PC([1, 8, 1, 1, 0, 0], 1, clock)
        pc.infect(10)
        when(clock).time().thenReturn(9)
        self.assertFalse(pc.infected())
        when(clock).time().thenReturn(10)
        self.assertTrue(pc.infected())

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

