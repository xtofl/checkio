__author__ = 'xtofl'

from collections import namedtuple
from itertools import ifilter, imap, starmap, ifilterfalse
from math import sqrt


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
    if len(alpha) != 1: raise ValueError("No unique Alpha Bat in cave")
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
    inter_bat_edges = [Edge(x, y) for x in nodes for y in nodes if not x is y]
    bat_alpha_edges = [Edge(x, cave.alpha) for x in nodes]
    edges = inter_bat_edges + bat_alpha_edges
    arcs_no_walls = ifilterfalse(lambda edge: any(map(lambda wall: wall.intersects(edge), cave.walls)), edges)
    return Graph(nodes, frozenset(arcs_no_walls))


def distance(p0, p1):
    delta = (p1[0] - p0[0], p1[1] - p0[1])
    return sqrt(delta[0] * delta[0] + delta[1] * delta[1])


class Edge(namedtuple("Edge", ("begin", "end"))):
    def connects(self, begin, end):
        return begin == self.begin and end == self.end
    def weight(self):
        return self.begin.distance_to(self.end)

def between(lim1, i, lim2):
    if lim1 < lim2:
        return not (i < lim1 or i > lim2)
    else:
        return not (i < lim2 or i > lim1)

"""thanks - http://stackoverflow.com/a/20679579/6610"""
def line_coefficients(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(segment1, segment2):
    L1, L2 = line_coefficients(*segment1), line_coefficients(*segment2)
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y

def line_intersection(segment1, segment2):

    i = intersection(segment1, segment2)

    if i:
        x, y = i
        def on(segment):
            # since we know i is on the line defined by segment,
            # we can fallback to limit-testing only
            return between(segment[0][0], x, segment[1][0]) and between(segment[0][1], y, segment[1][1])

        if on(segment1) and on(segment2):
            return x, y
        else:
            return None

def add_to_point(point, offset):
    return (point[0] + offset[0], point[1] + offset[1])

class Wall(namedtuple("Wall", ("center"))):

    def intersects(self, arc):
        top_left = add_to_point(self.center, (-0.5, -0.5))
        top_right = add_to_point(self.center, (-0.5, 0.5))
        bot_left = add_to_point(self.center, (0.5, -0.5))
        bot_right = add_to_point(self.center, (0.5, 0.5))

        arc_line = (arc.begin.where, arc.end.where)
        wall_lines = [
            (top_left, top_right),
            (bot_left, bot_right),
            (top_left, bot_left),
            (top_right, bot_right)
        ]

        intersections = list(starmap(line_intersection, [(edge, arc_line) for edge in wall_lines]))
        return any(intersections)

class AStar:
    """adapted from wikipedia http://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode"""

    @staticmethod
    def shortest_path(start, goal, edges, h=lambda vertex, goal: 0):
        def neighbor_edges(node):
            for e in ifilter(lambda edge: edge.begin == node, edges):
                yield e

        closed_set = set()
        open_set = set([start])
        came_from = dict()

        g = dict()
        g[start] = 0
        f = dict()
        f[start] = g[start] + h(start, goal)

        while open_set:
            next = min(open_set, key=lambda x: f[x])
            if next == goal:
                return AStar.reconstruct_path(came_from, goal, begin=begin)

            open_set.remove(next)
            closed_set.add(next)

            for neighbor_edge in neighbor_edges(next):
                if end(neighbor_edge) in closed_set:
                    continue
                tentative_g = g[next] + weight(neighbor_edge)

                neighbor = end(neighbor_edge)
                if not neighbor in open_set or tentative_g < g[end(neighbor_edge)]:
                    came_from[neighbor] = neighbor_edge
                    g[neighbor] = tentative_g
                    f[neighbor] = g[neighbor] + h(neighbor, goal)
                    if not neighbor in open_set:
                        open_set.add(neighbor)

        raise ValueError("no path possible")

    @staticmethod
    def reconstruct_path(came_from, current_node, begin=lambda x: x.begin):
        if current_node in came_from:
            edge_to_current = came_from[current_node]
            p = AStar.reconstruct_path(came_from, begin(edge_to_current), begin=begin)
            return p + [edge_to_current]
        else:
            return []


def length(path):
    return sum(imap(lambda edge: edge.weight(), path))

def checkio(cave_lines):
    cave = parse_cave(cave_lines)
    graph = bat_graph(cave)
    entry_bat = filter(lambda bat: bat.where == (0, 0), cave.bats + [cave.alpha])[0]
    return length(AStar.shortest_path(entry_bat, cave.alpha, graph.edges))


from unittest import TestCase

def make_edges(*args):
    return [Edge(*(arg)) for arg in args]

class AlphaBatTest(TestCase):

    def testParsingCave(self):
        small = ["B-", "-A"]
        self.assertEqual(Cave(bats=[Bat(0, 0)], alpha=Bat(1, 1), walls=[]), parse_cave(small))
        medium = ["B--",
                  "-B-",
                  "A-W"]
        self.assertEqual(Cave(bats=[Bat(0, 0), Bat(1, 1)], alpha=Bat(2, 0), walls=[Wall((2, 2))]), parse_cave(medium))
        self.assertRaises(ValueError, parse_cave, ["B-", "--"])

    def testArcsFromBats(self):
        bats = [Bat(0, 0), Bat(0, 3)]
        alpha = Bat(3, 3)
        cave = Cave(bats=bats, alpha=alpha,
                    walls=[])
        self.assertEqual(frozenset([(bats[0], bats[1]), (bats[1], bats[0]), (bats[0], alpha), (bats[1], alpha)]),
                         bat_graph(cave).edges)

        cave = Cave(bats=bats, alpha=alpha,
                    walls=[Wall((1, 1))])
        self.assertEqual(frozenset([(bats[0], bats[1]), (bats[1], bats[0]), (bats[1], alpha)]),
                         bat_graph(cave).edges)


    def testBatsDistance(self):
        self.assertAlmostEqual(1, distance((0, 0), (1, 0)))
        self.assertAlmostEqual(2, distance((0, 0), (0, 2)))
        self.assertAlmostEqual(1.41, distance((0, 0), (1, 1)), places=2)

    def testShortestPath(self):
        a, b, c, d = Bat(0, 0), Bat(10, 0), Bat(10, 10), Bat(100, 100)
        self.assertEqual([Edge(a, b)], AStar.shortest_path(a, b, make_edges((a, b))))
        self.assertEqual([Edge(a, b), Edge(b, d)], AStar.shortest_path(a, d, make_edges((a, b), (b, d), (c, d))))

        # prefer shorter of two
        class Weighted(namedtuple("Weighted", ["begin", "end", "w"])):
            def weight(self):
                return self.w

        self.assertEqual([Weighted(a, b, 1)], AStar.shortest_path(a, b, [Weighted(a, b, 1), Weighted(a, b, 2)]))
        # prefer hypothenuse
        self.assertEqual([Edge(a, c)], AStar.shortest_path(a, c, make_edges((a, b), (b, c), (a, c))))
        self.assertEqual([Edge(a, c), Edge(c, d)], AStar.shortest_path(a, d, make_edges((a, b), (b, c), (a, c), (c, d))))


    def testIntersection(self):
        self.assertEqual((0, 0), line_intersection(((-1, 0), (1, 0)), ((0, -1), (0, 1))))
        self.assertEqual((0, 0), line_intersection(((0, 0), (1, 0)), ((0, 0), (0, 1))))
        self.assertEqual(None, line_intersection(((.5, 0), (1, 0)), ((0, 0), (0, 1))))
        self.assertEqual((0, 0), line_intersection(((-1, -1), (1, 1)), ((-1, 1), (1, -1))))
        self.assertEqual((1, 0.5), line_intersection(((0.5, 0.5), (1.5, 0.5)), ((1, 0), (1, 2))))

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
        self.assertAlmostEqual(
            2.83,
            checkio([
                "B--",
                "---",
                "--A"]), places=2
        )
        self.assertAlmostEqual(
            4,
            checkio([
                "B-B",
                "BW-",
                "-BA"]), places=2
        )
        self.assertAlmostEqual(
            12,
            checkio([
                "BWB--B",
                "-W-WW-",
                "B-BWAB"]), places=2
        )
        self.assertAlmostEqual(
            9.24,
            checkio([
               "B---B-",
               "-WWW-B",
               "-WA--B",
               "-W-B--",
               "-WWW-B",
               "B-BWB-"]), places=2
        )
        self.assertEqual(0, checkio(["A"]))