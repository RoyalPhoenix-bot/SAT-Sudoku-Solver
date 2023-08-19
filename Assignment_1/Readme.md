# Instructions to Run
## Part 1: k-Sudoku Pair Solver
- Required Libraries `csv`, `pysat`, `numpy`, `datetime`.
- Make sure the `.csv` file is in the same directory as the python file.
- Build and Run the code.
- Input size **k** of sudoku in the terminal when prompted.
- Input the file name (with `.csv`) when prompted.
- Eg - If the file name is `sudokuPair`, type `sudokuPair.csv` on the terminal.

**Output:**
- A Solved k-Sudoku Pair is printed on the terminal, or `'None'` if a solution does not exist.

## Part 2: k-Sudoku Pair Generator
- Required Libraries `random`, `pysat`, `numpy`, `datetime`, `os`.
- Preferably, Change the directory on the terminal, (using the `cd` command), so that the output files are made in the same directory as the `.py` file.
- Build and Run the code.
- Input size **k** of sudoku in the terminal when prompted.

**Output:**
- A maximal k-Sudoku Pair (Having the maximum number of holes). The Sudokus are printed on the terminal and put in a `.csv` file as well.
(Outputs of this code are used as inputs in the first code. The output sudokus are put in the test folder included in the Q1 folder).
