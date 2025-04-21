from typing import List, Tuple, Union, Dict


def is_valid_next_character(current_character: str, check_character: str) -> bool:
    """
      Check if the next character is valid.

      Parameters:
          current_character (str): The character we want to check for.
          check_character (str): The character we want to check.

      Returns:
          bool: If the character is valid based on the logic.
    """
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
    """
      Get adjacent positions for a given position.

      Parameters:
          rows (int): Number of rows of the 2D Array.
          cols (str): Number of cols of the 2D Array.
          position (Tuple[int, int]): The position for which we want to get adjacent positions.

      Returns:
          List[Tuple[int, int]]: The list of positions.
    """
    row, col = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [
        (row + dr, col + dc)
        for dr, dc in directions
        if 0 <= row + dr < rows and 0 <= col + dc < cols
    ]


def walk_all_paths(matrix: List[List[str]], dict_map: Dict[Tuple[int, int], str], key: Tuple[int, int], visited: List[Tuple[int, int]],
                   letters: List[str], full_path: List[str]) -> Union[str, Tuple[str, str]]:
    """
      The main function that implements the solution for the challenge. It walks the path for the provided 2D Array.

      Parameters:
          matrix (List[List[str]]): The 2D Array.
          dict_map Dict[Tuple[int, int], str]: The 2D Array in ordered dict form with only valid positions.
          key (Tuple[int, int]): The current position.
          visited (List[Tuple[int, int]]): All visited positions so far.
          letters (List[str]): All letters collected on the way to the end of the path.
          full_path (List[str]): All characters collected on the way to the end of the path.

      Returns:
          Union[str, Tuple[str, str]]: Tuple with two elements, the letters and the path
           or the word 'Error' if we encounter an error scenario.
    """
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


def reorder_dict(initial_dict: Dict[Tuple[int, int], str]) -> Dict[Tuple[int, int], str]:
    """
       Reorders a dictionary in such way where the first element is always
        the one with value '@' and the last is one with value 'x'.

       Parameters:
           initial_dict (Dict[Tuple[int, int], str]): The 2D Array.

       Returns:
           Dict[Tuple[int, int], str]: Ordered dict.

    """
    first = {k: v for k, v in initial_dict.items() if v == '@'}
    middle = {k: v for k, v in initial_dict.items() if v not in ('@', 'x')}
    last = {k: v for k, v in initial_dict.items() if v == 'x'}
    return {**first, **middle, **last}


def is_valid_character(character: str) -> bool:
    """
      Checks if the character is valid such it can be taken into consideration.

      Parameters:
          character (str): The character that needs to be checked.

      Returns:
          bool: If the character is valid.

       """
    return character in ['-', '+', '@', '|', 'x'] or 'A' <= character <= 'Z'


def create_dict_map(matrix: List[List[str]]) -> Union[str, Dict[Tuple[int, int], str]]:
    """
     Creates a dict from a given 2D Array. It takes only the characters needed to create a valid path.
     Checks for error scenarios.

     Parameters:
         matrix (List[List[str]]): The starting 2D array.

     Returns:
         Union[str, Dict[Tuple[int, int], str]]: The dict map where the key is a tuple of the position of the
         character in the 2D Array and the value is the character. Or the word 'Error' if we encounter an error scenario.

    """
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


def find_start(dict_map: Dict[Tuple[int, int], str]) -> Union[None, Tuple[int, int]]:
    """
        Checks if the start element (with value '@') is in the dict_map.

        Parameters:
            dict_map (Dict[Tuple[int, int], str]): The dict.

        Returns:
            Union[None, Tuple[int, int]]: The position of the start element or None.
       """
    for k, v in dict_map.items():
        if v == '@':
            return k
    return None


def trace_path(matrix: List[List[str]]) -> Union[str, Tuple[str, str]]:
    """
       Wraps the functions needed to solve the challenge into one, so we can just have one line call in the main part.

       Parameters:
           matrix (List[List[str]]): The 2D Array.

       Returns:
           Union[str, Tuple[str, str]]: Tuple with two elements, the letters and the path
           or the word 'Error' if we encounter an error scenario.
    """

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
