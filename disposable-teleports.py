from cookielib import reach
from itertools import imap, ifilter


def dest(port, src):
    return port.replace(src, "")


def connects_to(port, station):
    return station in port


def ports(csv):
    return csv.split(",")


def removed_i(i, lst):
    return lst[:i] + lst[i+1:]


def removed_v(v, lst):
    return filter(lambda x: x != v, lst)


def port(src, dst):
    return src + dst


def ifind_paths(station, ports):
    direct_ports = filter(lambda x: connects_to(x[1], station), enumerate(ports))
    for i, port in direct_ports:
        new_ports = removed_i(i, ports)
        new_station = dest(port, station)
        yield new_station
        for rest_path in ifind_paths(new_station, new_ports):
            yield new_station + rest_path


def contains_all_and_ends_in(stations, station):
    def f(path):
        return set(stations) == set(path) and path[-1] == station
    return f

def checkio(portcsv):
    all_paths = ifind_paths(station="1", ports=ports(portcsv))
    paths = ifilter(contains_all_and_ends_in("12345678", "1"), all_paths)
    first_path = "1" + paths.next()
    print("{} => {}".format(portcsv, first_path))
    return first_path

from unittest import TestCase


class Test(TestCase):

    def testPortsFromCsv(self):
        self.assertEqual(ports("12"), ["12"])
        self.assertEqual(ports("12,32,53"), ["12","32","53"])

    def testReachable(self):
        self.assertTrue(connects_to("12", "1"))
        self.assertTrue(connects_to("21", "1"))

    def testRemove(self):
        self.assertEqual([], removed_i(0, [1]))
        self.assertEqual([1, 2], removed_i(0, [3, 1, 2]))
        self.assertEqual([3, 2], removed_i(1, [3, 1, 2]))
        self.assertEqual([], removed_v(0, [0]))
        self.assertEqual([1], removed_v(0, [1]))

    def _testCheckIo(self):
        self.assertEqual(checkio("12,23,34,45,56,67,78,81"), "123456781")
        self.assertEqual(checkio("12,28,87,71,13,14,34,35,45,46,63,65"), "1365417821")
        self.assertEqual(checkio("12,15,16,23,24,28,83,85,86,87,71,74,56"), "12382478561")
        self.assertEqual(checkio("13,14,23,25,34,35,47,56,58,76,68"), "132586741")



def main():
    checkio("12,23,34,45,56,67,78,81") == "123456781"
    checkio("12,28,87,71,13,14,34,35,45,46,63,65") == "1365417821"
    checkio("12,15,16,23,24,28,83,85,86,87,71,74,56") == "12382478561"
    checkio("13,14,23,25,34,35,47,56,58,76,68") == "132586741"


if __name__ == "__main__":
    main()

"""
The island has eight stations which are connected by a network of teleports; however, the teleports take a very long time to recharge. This means you can only use each one once. After you use a teleport, it will shut down and no longer function. But you can visit any station more than once. For this task, you should begin at number 1 and try to travel around to all the stations before returning to the starting point. The map of the teleports is presented as a string in which the comma-separated list represents teleports. Each teleport is given the name of the station it connects to. This name consists of two digits, such as '12' or '32.' Each test requires you to provide a route which passes through every station. A route is presented as a string of the station numbers in the sequence in which they must be visited (ex. 123456781).
"""
