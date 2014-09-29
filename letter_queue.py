from collections import deque


def letter_queue(commands):
    q = ""
    function = {
        "PUSH": lambda q, tokens: q + tokens[1],
        "POP": lambda q, _: q[1:] if q else ""
    }

    for cmd in commands:
        tokens = cmd.split()
        q = function[tokens[0]](q, tokens)

    return q

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert letter_queue(["PUSH A", "POP", "POP", "PUSH Z", "PUSH D", "PUSH O", "POP", "PUSH T"]) == "DOT", "dot example"
    assert letter_queue(["POP", "POP"]) == "", "Pop, Pop, empty"
    assert letter_queue(["PUSH H", "PUSH I"]) == "HI", "Hi!"
    assert letter_queue([]) == "", "Nothing"
