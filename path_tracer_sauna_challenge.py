from typing import List, Tuple, Union, Dict


def is_valid_next_character(current_character: str, check_character: str):
    if current_character == '@':
        return check_character in ('-', '|', '+', 'x') or 'A' <= check_character <= 'Z'
    elif current_character == '-':
        return check_character in ('-', '+', 'x', '|') or 'A' <= check_character <= 'Z'
    elif current_character == '|':
        return check_character in ('|', '+', 'x', '-') or 'A' <= check_character <= 'Z'
    elif current_character == '+':
        return check_character in ('-', '|', '+', 'x') or 'A' <= check_character <= 'Z'
    elif 'A' <= current_character <= 'Z':
        return check_character in ('-', '|', '+', 'x') or 'A' <= check_character <= 'Z'
    elif current_character == 'x':
        return False


def get_adjacent_positions(rows: int, cols: int, position: Tuple[int, int]) -> List[Tuple[int, int]]:
    row, col = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [
        (row + dr, col + dc)
        for dr, dc in directions
        if 0 <= row + dr < rows and 0 <= col + dc < cols
    ]


def contains_ordered_subsequence(full: List[str], sub: List[str]) -> bool:
    for i in range(len(full) - len(sub) + 1):
        if full[i:i+len(sub)] == sub:
            return True
    return False


def walk_all_paths(matrix: List[List[str]], dict_map: Dict, key: Tuple[int, int], visited: List[Tuple[int, int]],
                   letters: List[str], full_path: List[str]) -> Union[str, Tuple[str, str]]:


    current_char = dict_map[key]
    full_path.append(current_char)
    visited.append(key)

    if 'A' <= current_char <= 'Z':
        letters.append(current_char)
    if current_char == 'x':
        return ''.join(letters), ''.join(full_path)

    adjacent_positions = get_adjacent_positions(len(matrix), len(matrix[0]), key)
    next_positions = [
        pos for pos in adjacent_positions
        if pos in dict_map and is_valid_next_character(current_char, dict_map[pos]) and pos not in visited
    ]

    for pos in next_positions:
        result = walk_all_paths(matrix, dict_map, pos, visited.copy(), letters[:], full_path[:])
        if result != "Error":
            return result

    return "Error"


def reorder_dict(d: Dict) -> Dict:
    first = {k: v for k, v in d.items() if v == '@'}
    middle = {k: v for k, v in d.items() if v not in ('@', 'x')}
    last = {k: v for k, v in d.items() if v == 'x'}
    return {**first, **middle, **last}


def is_valid_character(character: str) -> bool:
    return character in ['-', '+', '@', '|', 'x'] or 'A' <= character <= 'Z'


def create_dict_map(matrix: List[List[str]]) -> Union[str, Dict[Tuple[int, int], str]]:
    dict_map = {}
    counter_start = 0
    counter_end = 0
    for i, row in enumerate(matrix):
        for j, item in enumerate(row):
            if item == ' ':
                continue
            if is_valid_character(item):
                if item == '@':
                    counter_start += 1
                elif item == 'x':
                    counter_end += 1
                dict_map[(i, j)] = item
            else:
                return "Error"
    if counter_start != 1 or counter_end != 1:
        return "Error"
    return reorder_dict(dict_map)


def find_start(dict_map):
    for k, v in dict_map.items():
        if v == '@':
            return k
    return None


def trace_path(matrix: List[List[str]]) -> Union[str, Tuple[str, str]]:
    dict_map = create_dict_map(matrix)
    if isinstance(dict_map, str):
        return "Error"

    start = find_start(dict_map)
    if not start:
        return "Error"

    return walk_all_paths(matrix, dict_map, start, [], [], [])


if __name__ == '__main__':
    input_map = [
        ['@', '-', '-', '-', 'A', '-', '-', '-', '+'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['x', '-', 'B', '-', '+', ' ', ' ', ' ', 'C'],
        [' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],
        [' ', ' ', ' ', ' ', '+', '-', '-', '-', '+']
    ]

    result = trace_path(input_map)

    if result == "Error":
        print("Error")
    else:
        letters, path = result
        print(letters)
        print(path)
