from collections import deque


def letter_queue(commands):
    q = deque()
    function = {
        "PUSH": lambda tokens: q.append(tokens[1]),
        "POP": lambda _: q.popleft() if q else None
    }

    for cmd in commands:
        tokens = cmd.split()
        function[tokens[0]](tokens)

    return "".join(q)

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert letter_queue(["PUSH A", "POP", "POP", "PUSH Z", "PUSH D", "PUSH O", "POP", "PUSH T"]) == "DOT", "dot example"
    assert letter_queue(["POP", "POP"]) == "", "Pop, Pop, empty"
    assert letter_queue(["PUSH H", "PUSH I"]) == "HI", "Hi!"
    assert letter_queue([]) == "", "Nothing"
