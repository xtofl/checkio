__author__ = 'xtofl'


from unittest import TestCase

def parse_cave(lines):
    bats = []
    alpha = []
    walls = []

    def noop(*args):
        pass
    def addbat(r, c):
        bats.append((r,c))
    def addwall(r, c):
        walls.append((r, c))
    def addalpha(r, c):
        alpha.append((r, c))

    actions = {'-': noop,
             'B': addbat,
             'A': addalpha,
             'W': addwall}
    for r, line in enumerate(lines):
        for c, cell in enumerate(line):
            actions[cell](r, c)

    return Cave(bats=bats, alpha=alpha[0], walls=walls)


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


def checkio(cave_lines):
    cave = parse_cave(cave_lines)
    graph = bat_graph(cave)
    return length(shortest_path(graph))


class AlphaBatTest(TestCase):

    def testParsingCave(self):
        small = ["B-", "-A"]
        self.assertEqual(Cave(bats=[(0, 0)], alpha=(1, 1), walls=[]), parse_cave(small))
        medium = ["B--",
                  "-B-",
                  "A-W"]
        self.assertEqual(Cave(bats=[(0, 0), (1, 1)], alpha=(2, 0), walls=[(2, 2)]), parse_cave(medium))

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