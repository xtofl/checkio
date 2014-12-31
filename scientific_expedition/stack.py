def push(stack, v, total):
    return stack + [v], total


def pop(stack, total):
    if not stack: return [], total
    return stack[:-1], total + stack[-1]


def peek(stack, total):
    if not stack: return [], total
    return stack, total + stack[-1]


def digit_stack(series):
    stack, total = [], 0
    for command in series:
        tokens = command.split()
        stack, total = \
            {
                "PUSH": lambda: push(stack, int(tokens[1]), total),
                "POP": lambda: pop(stack, total),
                "PEEK": lambda: peek(stack, total)
            }[tokens[0]]()
    return total


from unittest import TestCase


class TestStack(TestCase):
    def test_Given(self):
        self.assertEqual(digit_stack(["PUSH 3", "POP", "POP", "PUSH 4", "PEEK", "PUSH 9", "PUSH 0", "PEEK", "POP", "PUSH 1", "PEEK"]), 8)
        self.assertEqual(digit_stack(["POP", "POP"]), 0)
        self.assertEqual(digit_stack(["PUSH 9", "PUSH 9", "POP"]), 9)
        self.assertEqual(digit_stack([]), 0)