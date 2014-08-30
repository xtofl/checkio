from itertools import ifilter

class AStar:
    """adapted from wikipedia http://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode"""

    @staticmethod
    def shortest_path(start, goal, edges, neighbors=None, h=lambda vertex, goal: 0):
        if neighbors:
            neighbor_edges = neighbors
        else:
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
                return AStar.reconstruct_path(came_from, goal)

            open_set.remove(next)
            closed_set.add(next)

            for neighbor_edge in neighbor_edges(next):
                if neighbor_edge.end in closed_set:
                    continue
                tentative_g = g[next] + neighbor_edge.weight()

                neighbor = neighbor_edge.end
                if not neighbor in open_set or tentative_g < g[neighbor_edge.end]:
                    came_from[neighbor] = neighbor_edge
                    g[neighbor] = tentative_g
                    f[neighbor] = g[neighbor] + h(neighbor, goal)
                    if not neighbor in open_set:
                        open_set.add(neighbor)

        raise ValueError("no path possible")

    @staticmethod
    def reconstruct_path(came_from, current_node):
        if current_node in came_from:
            edge_to_current = came_from[current_node]
            p = AStar.reconstruct_path(came_from, edge_to_current.begin)
            return p + [edge_to_current]
        else:
            return []



def checkio(cat):
    return "ULDR"

from unittest import TestCase
class TestOctoCat(TestCase):
    def testGiven(self):
        self.assertEqual("ULDR", checkio(
            [[1, 2, 3],
             [4, 6, 8],
             [7, 5, 0]]))
