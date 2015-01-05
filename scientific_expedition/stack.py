def push(stack, v, total):
    return stack + [v], total


def pop(stack, total):
    if not stack: return [], total
    return stack[:-1], total + stack[-1]


def peek(stack, total):
    if not stack: return [], total
    return stack, total + stack[-1]


digit_stack=d=lambda queue, stack='0', total=0:\
        total if len(queue) == 0\
        else \
        (
            {
                "PUSH": lambda: d(queue[1:], queue[0][5]+stack, total),
                "POP": lambda: d(queue[1:], stack[1:] or '0', total+int(stack[0])),
                "PEEK": lambda: d(queue[1:], stack, total+int(stack[0]))
            }[queue[0].split()[0]]()
        )

from unittest import TestCase


class TestStack(TestCase):
    def test_Given(self):
        self.assertEqual(digit_stack(["PUSH 3", "POP", "POP", "PUSH 4", "PEEK", "PUSH 9", "PUSH 0", "PEEK", "POP", "PUSH 1", "PEEK"]), 8)
        self.assertEqual(digit_stack(["POP", "POP"]), 0)
        self.assertEqual(digit_stack(["PUSH 9", "PUSH 9", "POP"]), 9)
        self.assertEqual(digit_stack([]), 0)