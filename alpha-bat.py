__author__ = 'xtofl'


from unittest import TestCase

def parse_cave(lines):
    bats = []
    alpha = None
    walls = []
    def addbat(r, c):
        bats.append((r,c))
    def addwall(r, c):
        walls.append((r,c))
    def addalpha(r, c):
        alpha = (r, c)
    for r, line in enumerate(lines):
        for c, cell in line:
            {'-': noop,
             'B': addbat,
             'A': addalpha,
             'W': addwall}[cell](r,c)

    return {'bats': bats, 'alpha': alpha, 'walls': walls}


def checkio(cave_lines):
    cave = parse_cave(cave_lines)
    graph = bat_graph(cave)
    return length(shortest_path(graph))


class AlphaBatTest(TestCase):

    def testGiven(self):
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