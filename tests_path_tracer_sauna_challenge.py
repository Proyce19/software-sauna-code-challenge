import unittest

from path_tracer_sauna_challenge import trace_path, is_valid_next_character, get_adjacent_positions


class TestPathTracer(unittest.TestCase):

    def test_is_valid_next_character(self):
        self.assertTrue(is_valid_next_character('@', '-'))
        self.assertTrue(is_valid_next_character('-', 'A'))
        self.assertFalse(is_valid_next_character('x', '-'))

    def test_get_adjacent_positions(self):
        pos = (1, 1)
        expected = [(0, 1), (2, 1), (1, 0), (1, 2)]
        self.assertEqual(get_adjacent_positions(3, 3, pos), expected)

    def test_simple_path(self):
        input_map = [
            ['@', '-', 'A', '-', 'x']
        ]
        result = trace_path(input_map)
        self.assertEqual(result, ('A', '@-A-x'))

    def test_trace_loop_path(self):
        input_map = [
            [' ', '+', '-', 'L', '-', '+', ' ', ' '],
            [' ', '|', ' ', ' ', '+', 'A', '-', '+'],
            ['@', 'B', '+', ' ', '+', '+', ' ', 'H'],
            [' ', '+', '+', ' ', ' ', ' ', ' ', 'x']
        ]
        result = trace_path(input_map)
        self.assertEqual(result, ('BLAH', '@B|+-L-+++A-+Hx'))

    def test_error_multiple_starts(self):
        input_map = [
            ['@', '-', '-', 'x'],
            [' ', ' ', ' ', '@']
        ]
        result = trace_path(input_map)
        self.assertEqual(result, 'Error')

    def test_error_multiple_ends(self):
        input_map = [
            ['@', '-', '-', 'x'],
            [' ', ' ', ' ', 'x']
        ]
        result = trace_path(input_map)
        self.assertEqual(result, 'Error')

    def test_error_disconnected_path(self):
        input_map = [
            ['@', '-', '-', 'A'],
            [' ', ' ', ' ', ' '],
            ['x', '-', '-', 'B']
        ]
        result = trace_path(input_map)
        self.assertEqual(result, 'Error')

    def test_with_letter_on_turn(self):
        input_map = [
            ['@', '-', '+'],
            [' ', ' ', 'A'],
            [' ', ' ', '|'],
            [' ', ' ', 'x']
        ]
        result = trace_path(input_map)
        self.assertEqual(result, ('A', '@-+A|x'))

    def test_large_input(self):
        input_map = [
            [' ', ' ', ' ', ' ', '+', '-', 'O', '-', 'N', '-', '+', ' ', ' '],
            [' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' '],
            [' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '+', '-', 'I', '-', '+'],
            ['@', '-', 'G', '-', 'O', '-', '+', ' ', '|', ' ', '|', ' ', '|'],
            [' ', ' ', ' ', ' ', '|', ' ', '|', ' ', '+', '-', '+', ' ', 'E'],
            [' ', ' ', ' ', ' ', '+', '-', '+', ' ', ' ', ' ', ' ', ' ', 'S'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x']
        ]
        result = trace_path(input_map)
        self.assertNotEqual(result, 'Error')
        self.assertTrue('x' in result[1])

    def test_horizontal_only(self):
        input_map = [['@', '-', 'A', '-', 'B', '-', 'x']]
        result = trace_path(input_map)
        self.assertEqual(result, ('AB', '@-A-B-x'))

    def test_vertical_only(self):
        input_map = [['@'], ['|'], ['A'], ['|'], ['B'], ['|'], ['x']]
        result = trace_path(input_map)
        self.assertEqual(result, ('AB', '@|A|B|x'))

    def test_no_letter_on_path(self):
        input_map = [
            ['@', '-', '+', ' ', ' '],
            [' ', ' ', '|', ' ', ' '],
            [' ', ' ', '+', '-', 'x'],
            [' ', ' ', 'A', ' ', ' '],
        ]
        result = trace_path(input_map)
        self.assertEqual(result, ('', '@-+|+-x'))

    def test_letter_in_path_no_x(self):
        input_map = [['@', '-', 'A', '-', 'B']]
        result = trace_path(input_map)
        self.assertEqual(result, 'Error')

    def test_end_before_any_letter(self):
        input_map = [['@', '-', 'x', '-', 'A']]
        result = trace_path(input_map)
        self.assertEqual(result, ('', '@-x'))

    def test_with_repeating_letters(self):
        input_map = [['@', '-', 'A', '-', '+'],
                     [' ', ' ', ' ', ' ', '|'],
                     ['x', '-', 'A', '-', '+']]
        result = trace_path(input_map)
        self.assertEqual(result, ('AA', '@-A-+|+-A-x'))

    def test_entire_sub_path_is_not_visited(self):
        input_map = [
            ['@', '-', 'A', '-', '+'],
            [' ', ' ', ' ', ' ', '|'],
            ['B', '-', '+', ' ', 'C'],
            [' ', ' ', '|', ' ', '|'],
            [' ', ' ', '+', '-', 'x']
        ]
        result = trace_path(input_map)
        self.assertEqual(result, ('AC', '@-A-+|C|x'))


if __name__ == '__main__':
    unittest.main()
