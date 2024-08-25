#####################
# Crossword Puzzle Game #
#####################

import random
import json
import sys

# Define a list of words and their clues
words = [
    ("python", "A programming language"),
    ("cursor", "A text editor"),
    ("crossword", "A word puzzle"),
    ("game", "An activity for fun"),
    ("code", "Instructions for a computer"),
    ("algorithm", "A step-by-step procedure for solving a problem"),
    ("database", "A structured collection of data"),
    ("interface", "A point of interaction between components"),
    ("network", "A group of interconnected computers"),
    ("software", "Programs and other operating information used by a computer"),
    ("hardware", "The physical components of a computer system"),
    ("encryption", "The process of encoding information"),
    ("debugging", "The process of identifying and removing errors from software"),
    ("compiler", "A program that translates source code into machine code"),
    ("variable", "A storage location paired with an associated symbolic name"),
    ("function", "A block of organized, reusable code"),
    ("loop", "A sequence of instructions that is continually repeated"),
    ("array", "A data structure consisting of a collection of elements"),
    ("object", "A software bundle of variables and related methods"),
    ("inheritance", "A mechanism of basing an object or class upon another"),
    ("framework", "A platform for developing software applications"),
    ("api", "A set of functions and procedures for building software"),
    ("server", "A computer program or device that provides functionality for other programs or devices"),
    ("client", "A piece of computer hardware or software that accesses a service made available by a server"),
    ("database", "An organized collection of data stored and accessed electronically")
]

def create_grid(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

def print_grid(grid):
    for row in grid:
        print(' '.join(row))
    print()

def check_within_grid(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def check_surrounding_positions_empty(grid, row, col, ignored_positions):
    surrounding_directions = {(-1, 0), (0, -1), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)}
    for position in surrounding_directions:
        srow, scol = row + position[0], col + position[1]
        if check_within_grid(grid, srow, scol) and grid[srow][scol] != ' ' and (srow, scol) not in ignored_positions:
            print(f"[Conflict with surroundings] neighbour position {position_to_string(grid, srow, scol)}, relative {position}")
            return False
    return True

def position_to_string(grid, row, col):
    return f"({row}, {col})[{grid[row][col]}]"

def write_word(grid, word, start_row, start_col, direction):
    if direction == 'across':
        for i, letter in enumerate(word):
            grid[start_row][start_col + i] = letter
    else:
        for i, letter in enumerate(word):
            grid[start_row + i][start_col] = letter

def place_word(grid, word, start_row, start_col, direction, used_word_positions=None):
    if not used_word_positions: # first word
        if direction == 'across':
            if not check_within_grid(grid, start_row, start_col + len(word)):
                print(f"Cannot place '{word}' across at {position_to_string(grid, start_row, start_col)}: Word extends beyond grid")
                return None
        else:
            if not check_within_grid(grid, start_row + len(word), start_col):
                print(f"Cannot place '{word}' down at {position_to_string(grid, start_row, start_col)}: Word extends beyond grid")
                return None
    else:
        if not check_within_grid(grid, start_row, start_col):
            print(f"Cannot place '{word}' at ({start_row}, {start_col}): start position beyond grid")
            return None
        # Find the index of the letter in the word corresponding to the letter on the grid
        intersection_index = word.find(grid[start_row][start_col])
        if intersection_index < 0:
            print(f"Cannot place '{word}' at {position_to_string(grid, start_row, start_col)}: No intersection found")
            return None
        if direction == 'across':
            start_col -= intersection_index
            if not (check_within_grid(grid, start_row, start_col) and check_within_grid(grid, start_row, start_col + len(word))):
                print(f"Cannot place '{word}' across at {position_to_string(grid, start_row, start_col)}: Word extends beyond grid")
                return None
            # Check if the word can be placed without conflicts
            for i, letter in enumerate(word):
                if grid[start_row][start_col + i] != ' ' and grid[start_row][start_col + i] != letter:
                    print(f"Cannot place '{word}' across at {position_to_string(grid, start_row, start_col)}: Conflict at position {position_to_string(grid, start_row, start_col + i)}")
                    return None
                if not check_surrounding_positions_empty(grid, start_row, start_col + i, used_word_positions):
                    print(f"Cannot place '{word}' across at {position_to_string(grid, start_row, start_col)}: Conflict with surroundings at position {position_to_string(grid, start_row, start_col + i)}")
                    return None            
        elif direction == 'down':
            start_row -= intersection_index
            if not (check_within_grid(grid, start_row, start_col) and check_within_grid(grid, start_row + len(word), start_col)):
                print(f"Cannot place '{word}' down at {position_to_string(grid, start_row, start_col)}: Word extends beyond grid")
                return None
            for i, letter in enumerate(word):
                if grid[start_row + i][start_col] != ' ' and grid[start_row + i][start_col] != letter:
                    print(f"Cannot place '{word}' down at {position_to_string(grid, start_row, start_col)}: Conflict at position {position_to_string(grid, start_row + i, start_col)}")
                    return None
                if not check_surrounding_positions_empty(grid, start_row + i, start_col, used_word_positions):
                    print(f"Cannot place '{word}' down at {position_to_string(grid, start_row, start_col)}: Conflict with surroundings at position {position_to_string(grid, start_row + i, start_col)}")
                    return None
            
    # If no conflicts, write the word
    write_word(grid, word, start_row, start_col, direction)
    return (start_row, start_col)

def create_puzzle():
    size = 25
    grid = create_grid(size)
    used_words = []

    for word, clue in random.sample(words, len(words)):
        placed = False
        attempts = 100

        for _ in range(attempts):
                if used_words:
                    used_word, _, row, col, direction = random.choice(used_words)
                    used_word_positions = {(row, col + i) for i in range(len(used_word))} if direction == 'across' else {(row + i, col) for i in range(len(used_word))}
                    # Check if the current word intersects with the used word
                    if not (set(word) & set(used_word)):
                        # todo select start positions from indices of intersections, not randomly
                        continue
                    if direction == 'across':
                        start_row = row
                        start_col = col + random.randint(0, len(used_word) - 1)
                        direction = 'down'
                    else:
                        start_row = row + random.randint(0, len(used_word) - 1)
                        start_col = col
                        direction = 'across'
                else:
                    used_word_positions = set() # first word
                    direction = random.choice(['across', 'down'])
                    if direction == 'across':
                        start_row = random.randint(0, size - 1)
                        start_col = random.randint(0, size - len(word))
                    else:
                        start_row = random.randint(0, size - len(word))
                        start_col = random.randint(0, size - 1)
                
                print(f"Trying to place '{word}' {direction} at ({start_row}, {start_col})")
                result = place_word(grid, word, start_row, start_col, direction, used_word_positions)
                if result:
                    (start_row, start_col) = result
                    print(f"Successfully placed '{word}' at ({start_row}, {start_col})")
                    used_words.append((word, clue, start_row, start_col, direction))
                    placed = True
                    break

        if not placed:
                print(f"Couldn't place word: {word}")

    return grid, used_words

def play_game():
    grid, words = create_puzzle()
    # hide words in the grid to make the game more interesting
    original_grid = grid.copy()
    grid = [[('*' if cell != ' ' else ' ') for cell in row] for row in grid]

    # Add word numbers to the grid
    for i, (_, _, row, col, direction) in enumerate(words):
        write_word(grid, str(i + 1), row, col, direction)

    solved_word_indices = set()

    print("Welcome to the Crossword Puzzle Game!")
    print("Fill in the words based on the clues provided.")
    print("Enter 'quit' to exit the game.\n")

    while len(words) > len(solved_word_indices):
        print_grid(grid)
        for i, (word, clue, _, _, _) in enumerate(words):
            if i not in solved_word_indices:
                print(f"{i + 1}. {clue}")

        guess = input("Enter the word number and your guess (e.g., '1 python'): ").lower()
        if guess == 'quit':
            break
        if guess == '@web':
            print(encode_puzzle_data(original_grid, words))
            sys.exit()

        try:
            num, word_guess = guess.split()
            num = int(num) - 1
            if 0 <= num < len(words) and word_guess == words[num][0]:
                print("Correct!")
                word, _, row, col, direction = words[num]
                solved_word_indices.add(num)
                write_word(grid, word, row, col, direction)
            else:
                print("Incorrect. Try again!")
        except ValueError:
            print("Invalid input. Please try again.")

    if len(solved_word_indices) == len(words):
        print("\nCongratulations! You've completed the crossword puzzle!")
    else:
        print("\nThanks for playing!")

    print("Solved crossword:")
    print_grid(original_grid)

def encode_puzzle_data(grid, words):
    puzzle_data = {
        "grid": grid,
        "words": [
            {
                "word": word,
                "clue": clue,
                "row": row,
                "col": col,
                "direction": direction
            }
            for word, clue, row, col, direction in words
        ]
    }
    return json.dumps(puzzle_data)

if __name__ == "__main__":
    play_game()