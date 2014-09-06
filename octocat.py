from math import sqrt
from itertools import ifilter, starmap
from operator import mul


def freeze(x):
    if type(x) is list:
        return tuple(map(freeze, x))
    return x

def thaw(x):
    if type(x) is tuple:
        return list(map(thaw, x))
    return x

class AStar:
    """adapted from wikipedia http://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode"""

    @staticmethod
    def shortest_path(start, goal, edges, neighbors=None, weight=lambda x: x.weight, h=lambda vertex, goal: 0, begin=lambda x: x.begin, end=lambda x: x.end):
        start = freeze(start)
        goal = freeze(goal)
        def dump(x):
            return None
            print x
        if neighbors:
            neighbor_edges = lambda x: dump(x) or freeze(neighbors(x))
        else:
            def neighbor_edges(node):
                for e in ifilter(lambda edge: begin(edge) == node, edges):
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

def find_zero(lines):
    for row, line in enumerate(lines):
        for col, v in enumerate(line):
            if v == 0:
                return row, col
    raise ValueError("no zero in puzzle "+str(lines))

def swap(first, second, puzzle):
    row0, col0 = first
    row1, col1 = second
    puzzle = thaw(puzzle)
    puzzle[row0][col0], puzzle[row1][col1] = puzzle[row1][col1], puzzle[row0][col0]
    return puzzle


def move_coords(puzzle):
    row, col = find_zero(puzzle)
    dirs = {'L': (0, -1),
            'R': (0, +1),
            'U': (-1, 0),
            'D': (+1, 0)}
    positive = lambda c: len(puzzle) > c[1][0] >= 0 and len(puzzle[0]) > c[1][1] >= 0
    coords = filter(positive, [(k, (row + dirs[k][0], col + dirs[k][1])) for k in dirs.keys()])
    return set(coords)


def moves(puzzle):
    """returns the possible moves in a format
    (name, source, dest)
    """
    return map(lambda c: (c[0], (puzzle, swap(find_zero(puzzle), c[1], puzzle))), move_coords(puzzle))



def checkio(puzzle):
    solved = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    def lin(a):
        return reduce(lambda x, y: x+y, freeze(a), ())
    def distance(a, b):
        a, b = lin(a), lin(b)
        return sqrt(sum(starmap(lambda a, b: (a-b)*(a-b), zip(a, b))))

    path = AStar.shortest_path(start=puzzle, goal=solved, edges=None, neighbors=moves,
                               begin=lambda x: freeze(x[1][0]),
                               end=lambda x: freeze(x[1][1]),
                               weight=lambda x: 1,
                               h=distance)
    return "".join(map(lambda x: x[0], path))

from unittest import TestCase
class TestOctoCat(TestCase):

    def testShift(self):
        self.assertEqual((0, 1), find_zero([[4, 0, 5]]))
        self.assertEqual((1, 1), find_zero([[1, 2, 3], [4, 0, 5]]))
        self.assertEqual((2, 2), find_zero(
            [[1, 2, 3],
             [4, 6, 8],
             [7, 5, 0]]))

    def testSwap(self):
        puzzle = [[1, 2, 3],
                  [4, 0, 5],
                  [6, 7, 8]]
        self.assertEqual([[4, 2, 3],
                          [1, 0, 5],
                          [6, 7, 8]], swap((0, 0), (1, 0), puzzle))

    def testMoves(self):
        puzzle = [[1, 2, 3],
                  [4, 0, 5],
                  [6, 7, 8]]

        these_moves = move_coords(puzzle)
        self.assertTrue(('L', (1, 0)) in these_moves)
        self.assertTrue(('R', (1, 2)) in these_moves)
        self.assertTrue(('U', (0, 1)) in these_moves)
        self.assertTrue(('D', (2, 1)) in these_moves)

        puzzle = [[1, 2, 3],
                  [0, 4, 5],
                  [6, 7, 8]]

        self.assertEqual({('R', (1, 1)), ('U', (0, 0)), ('D', (2, 0))}, move_coords(puzzle))

    def testGiven(self):
        self.assertEqual("", checkio(
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 0]]
        ))
        self.assertEqual("ULDR", checkio(
            [[1, 2, 3],
             [4, 6, 8],
             [7, 5, 0]]))
        self.assertTrue(checkio([[4, 3, 1], [2, 5, 0], [7, 8, 6]]))
