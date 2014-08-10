from collections import namedtuple
from itertools import imap, ifilter, starmap, ifilterfalse, chain, islice
from math import sqrt

__author__ = 'xtofl'


from unittest import TestCase

def parse_cave(lines):
    bats = []
    alpha = []
    walls = []

    def noop(*args):
        pass
    def addbat(r, c):
        bats.append(Bat(r,c))
    def addwall(r, c):
        walls.append(Wall((r, c)))
    def addalpha(r, c):
        alpha.append(AlphaBat(r, c))

    actions = {'-': noop,
             'B': addbat,
             'A': addalpha,
             'W': addwall}
    for r, line in enumerate(lines):
        for c, cell in enumerate(line):
            actions[cell](r, c)
    if not alpha: raise ValueError("No Alpha Bat in cave")
    return Cave(bats=bats, alpha=alpha[0], walls=walls)


class Bat:
    def __init__(self, row, col):
        self.where = (row, col)

    def distance_to(self, other):
        return distance(self.where, other.where)

    def __eq__(self, other):
        return self.where == other.where

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return self.where.__hash__()

    def __repr__(self):
        return "Bat{}".format(self.where)


class AlphaBat(Bat):
    def __repr__(self):
        return "Alpha"+super(AlphaBat, self).__repr__()

class Cave:
    def __init__(self, bats, alpha, walls):
        self.bats = bats
        self.alpha = alpha
        self.walls = walls

    def __eq__(self, other):
        return (self.bats, self.walls, self.alpha) == (other.bats, other.walls, other.alpha)

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return "alpha: {}; bats: {}, walls: {}".format(self.alpha, self.bats, self.walls)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

def bat_graph(cave):
    nodes = cave.bats
    arcs = [Edge(x, y) for x in nodes for y in nodes if not x is y] + [Edge(x, cave.alpha) for x in nodes]
    arcs_no_walls = ifilterfalse(lambda arc: any(map(lambda wall: wall.intersects(arc), cave.walls)), arcs)
    return Graph(nodes, frozenset(arcs_no_walls))

def checkio(cave_lines):
    cave = parse_cave(cave_lines)
    graph = bat_graph(cave)
    return length(shortest_path(cave.bats[0], cave.alpha, graph.edges))


def distance(p0, p1):
    delta = (p1[0] - p0[0], p1[1] - p0[1])
    return sqrt(delta[0] * delta[0] + delta[1] * delta[1])


class Edge(namedtuple("Edge", ("begin", "end"))):
    def connects(self, begin, end):
        return begin == self.begin and end == self.end
    def weight(self):
        return self.begin.distance_to(self.end)

class Wall(namedtuple("Wall", ("center"))):
    def intersects(self, arc):
        return False




def paths(begin, end, edges):
    direct_edges = ifilter(lambda e: e.connects(begin, end), edges)
    for e in direct_edges:
        yield [e]

    indirect_edges = ifilter(lambda e: e.begin == begin, edges)
    for e in indirect_edges:
        rest_edges = filter(lambda edge: edge != e, edges)
        for p in paths(e.end, end, rest_edges):
            yield [e] + p


def length(path):
    return sum(map(lambda edge: edge.weight(), path))

def shortest_path(begin, end, edges):
    return min(paths(begin, end, edges), key=length)


def make_edges(*args):
    return [Edge(*(arg)) for arg in args]

class AlphaBatTest(TestCase):

    def testPaths(self):

        self.assertTrue([Edge(1, 2)] in paths(1, 2, make_edges((1, 2))))
        self.assertTrue([Edge(1, 2), Edge(2, 3)] in paths(1, 3, make_edges((1, 2), (2, 3))))
        self.assertTrue([Edge(1, 2), Edge(2, 3)] in paths(1, 3, make_edges((8, 10), (1, 2), (2, 3))))
        self.assertTrue([Edge(1, 2), Edge(2, 3)] in paths(1, 3, make_edges((8, 10), (1, 2), (2, 3), (1, 3))))
        self.assertTrue([Edge(1, 3)] in paths(1, 3, make_edges((8, 10), (1, 2), (2, 3), (1, 3))))
        self.assertTrue(make_edges((1, 3), (3, 4)) in paths(1, 4, make_edges((1, 2), (2, 3), (3, 4), (1, 3), (3, 4))))
        self.assertTrue(make_edges((1, 2), (2, 3), (3, 4)) in paths(1, 4, make_edges((1, 2), (2, 3), (3, 4), (1, 3), (3, 4))))

    def testParsingCave(self):
        small = ["B-", "-A"]
        self.assertEqual(Cave(bats=[Bat(0, 0)], alpha=Bat(1, 1), walls=[]), parse_cave(small))
        medium = ["B--",
                  "-B-",
                  "A-W"]
        self.assertEqual(Cave(bats=[Bat(0, 0), Bat(1, 1)], alpha=Bat(2, 0), walls=[Wall((2, 2))]), parse_cave(medium))
        self.assertRaises(ValueError, parse_cave, ["B-", "--"])

    def testArcsFromBats(self):
        bats = [Bat(0, 0), Bat(2, 3)]
        alpha = Bat(3, 3)
        cave = Cave(bats=bats, alpha=alpha,
                    walls=[])
        self.assertEqual(frozenset([(bats[0], bats[1]), (bats[1], bats[0]), (bats[0], alpha), (bats[1], alpha)]), bat_graph(cave).edges)

        cave = Cave(bats=bats, alpha=alpha,
                    walls=[Wall((1, 1))])
        self.assertEqual(frozenset([(bats[0], bats[1]), (bats[1], bats[0]), (bats[1], alpha)]),
                         bat_graph(cave).edges)


    def testBatsDistance(self):
        self.assertAlmostEqual(1, distance((0, 0), (1, 0)))
        self.assertAlmostEqual(2, distance((0, 0), (0, 2)))
        self.assertAlmostEqual(1.41, distance((0, 0), (1, 1)), places=2)

    def testShortestPath(self):
        class DistanceOne:
            def __init__(self, name):
                self.name = name
            def distance_to(self, other):
                return 1
            def __repr__(self):
                return self.name

        a, b, c, d = map(DistanceOne, "abcd")
        self.assertEqual([Edge(a, b)], shortest_path(a, b, make_edges((a, b))))
        self.assertEqual([Edge(a, b), Edge(b, d)], shortest_path(a, d, make_edges((a, b), (b, d), (b, c), (c, d))))

    def testWall(self):
        def edge(a, b):
            return Edge(begin=Bat(*a), end=Bat(*b))

        self.assertTrue(Wall((1, 1)).intersects(edge((1, 0), (1, 2))))
        self.assertTrue(Wall((1, 1)).intersects(edge((1, 2), (1, 0))))
        self.assertTrue(Wall((1, 1)).intersects(edge((0, 1), (2, 1))))
        self.assertTrue(Wall((1, 1)).intersects(edge((1, 0), (1, 2))))
        self.assertFalse(Wall((1, 1)).intersects(edge((0, 0), (0, 2))))
        self.assertFalse(Wall((1, 1)).intersects(edge((2, 0), (2, 2))))
        self.assertFalse(Wall((1, 1)).intersects(edge((0, 0), (2, 0))))
        self.assertFalse(Wall((1, 1)).intersects(edge((2, 0), (2, 2))))

    def testGiven(self):
        self.assertAlmostEqual(2.83,
            checkio([
                "B--",
                "---",
                "--A"]), places=2
        )
        self.assertAlmostEqual(4,
            checkio([
                "B-B",
                "BW-",
                "-BA"]), places=2
        )
        self.assertAlmostEqual(12,
            checkio([
                "BWB--B",
                "-W-WW-",
                "B-BWAB"]), places=2
        )
        self.assertAlmostEqual(9.24,
            checkio([
                "B---B-",
                "-WWW-B",
                "-WA--B",
                "-W-B--",
                "-WWW-B",
                "B-BWB-"]), places=2
        )