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
    def __init__(self, nodes, arcs):
        self.nodes = nodes
        self.arcs = arcs

def bat_graph(cave):
    nodes = cave.bats
    arcs = frozenset([(x, y) for x in nodes for y in nodes if not x is y])
    return Graph(nodes, arcs)

def checkio(cave_lines):
    cave = parse_cave(cave_lines)
    graph = bat_graph(cave)
    return length(shortest_path(graph))


class AlphaBatTest(TestCase):

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
        self.assertEqual({(Bat(0, 0), Bat(1, 1)), (Bat(1, 1), Bat(0, 0))}, bat_graph(cave).arcs)

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