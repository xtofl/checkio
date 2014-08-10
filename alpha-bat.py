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
        walls.append((r, c))
    def addalpha(r, c):
        alpha.append(Bat(r, c))

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

    def __eq__(self, other):
        return self.where == other.where

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return self.where.__hash__()

    def __repr__(self):
        return "Bat{}".format(self.where)


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
    arcs = frozenset([(x, y) for x in nodes for y in nodes if not x is y])
    return Graph(nodes, arcs)

def checkio(cave_lines):
    cave = parse_cave(cave_lines)
    graph = bat_graph(cave)
    return length(shortest_path(graph))


def distance(p0, p1):
    delta = (p1[0] - p0[0], p1[1] - p0[1])
    return sqrt(delta[0] * delta[0] + delta[1] * delta[1])


class Edge(namedtuple("Edge", ("begin", "end", "weight"))):
    def connects(self, begin, end):
        return begin == self.begin and end == self.end


def paths(begin, end, edges):
    direct_edges = ifilter(lambda e: e.connects(begin, end), edges)
    for e in direct_edges:
        yield [e]

    indirect_edges = ifilter(lambda e: e.begin == begin, edges)
    for e in indirect_edges:
        rest_edges = ifilter(lambda edge: edge != e, edges)
        for p in paths(e.end, end, rest_edges):
            yield [e] + p


def shortest_path(begin, end, edges):
    return 1


def length(path):
    return sum(map(lambda edge: edge.weight, path))

class AlphaBatTest(TestCase):

    def testPaths(self):
        def make_edges(*args):
            return [Edge(*(arg+(1,))) for arg in args]
        self.assertTrue([Edge(1, 2, 1)] in paths(1, 2, make_edges((1, 2))))
        self.assertTrue([Edge(1, 2, 1), Edge(2, 3, 1)] in paths(1, 3, make_edges((1, 2), (2, 3))))
        self.assertTrue([Edge(1, 2, 1), Edge(2, 3, 1)] in paths(1, 3, make_edges((8, 10), (1, 2), (2, 3))))

    def testParsingCave(self):
        small = ["B-", "-A"]
        self.assertEqual(Cave(bats=[Bat(0, 0)], alpha=Bat(1, 1), walls=[]), parse_cave(small))
        medium = ["B--",
                  "-B-",
                  "A-W"]
        self.assertEqual(Cave(bats=[Bat(0, 0), Bat(1, 1)], alpha=Bat(2, 0), walls=[(2, 2)]), parse_cave(medium))
        self.assertRaises(ValueError, parse_cave, ["B-", "--"])

    def testArcsFromBats(self):
        cave = Cave(bats=[Bat(0, 0), Bat(1, 1)], alpha=Bat(1, 2), walls=[])
        self.assertEqual({(Bat(0, 0), Bat(1, 1)), (Bat(1, 1), Bat(0, 0))}, bat_graph(cave).edges)


    def testBatsDistance(self):
        self.assertAlmostEqual(1, distance((0, 0), (1, 0)))
        self.assertAlmostEqual(2, distance((0, 0), (0, 2)))
        self.assertAlmostEqual(1.41, distance((0, 0), (1, 1)), places=2)

    def testShortestPath(self):
        a, b, c, d = 'a', 'b', 'c', 'd'
        self.assertEqual(1, shortest_path(begin=a, end=b, edges={(a, b): 1}))

    def _testGiven(self):
        self.assertAlmostEqual(2.83,
            checkio([
                "B--",
                "---",
                "--A"])
        )
        self.assertAlmostEqual(4,
            checkio([
                "B-B",
                "BW-",
                "-BA"])
        )
        self.assertAlmostEqual(12,
            checkio([
                "BWB--B",
                "-W-WW-",
                "B-BWAB"])
        )
        self.assertAlmostEqual(9.24,
            checkio([
                "B---B-",
                "-WWW-B",
                "-WA--B",
                "-W-B--",
                "-WWW-B",
                "B-BWB-"])
        )