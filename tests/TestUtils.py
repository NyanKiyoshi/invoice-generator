import unittest


class TestUtils(unittest.TestCase):
    def assertStrippedEqual(self, first: str, second: str, msg=None):
        return self.assertEqual(first, second.strip(), msg)

    @staticmethod
    def assertStrippedMultiIn(first: tuple, second: str):
        line = ''
        line_no = 0
        char_pos = 0

        while line_no < len(first) and char_pos < len(second):
            c = second[char_pos]

            if c == '\n':
                if first[line_no] == line.strip():
                    line_no += 1
                else:
                    line_no = 0

                line = ''
            else:
                line += c

            char_pos += 1

        if line_no != len(first):
            raise AssertionError("{} not in {}".format(first, second))
