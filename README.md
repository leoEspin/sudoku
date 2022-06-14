# Sudoku solver
The solver is implemented in a class, and uses backtraking to explore the solution space. To use it instanciate the class

```python
test = sudoku(initial_position)
```

where `initial_position` is a 81-characters-long string which holds the initial position, read from the top-left corner to the bottom right one. For example

```python
'5...8..49...5...3..673....115..........2.8..........187....415..3...2...49..5...3'
```

anything that is not a digit will produce an emtpy position at that index. Also, strings shorter than 81 characters can be used, if the initial position does not include the bottom-right corner. For example the string `'5...8..49'` is a valid initial position, and the solver will find a solution.

To search for a solution, run `test.fill_board()`. The solver will show an animation of the progress of the search. The final solution will be stored in `test.board` as a numpy array.

The solver can be initialized with board sizes smaller than the standard 9, however for things to make sense, the board size has be a perfect square, and the digits used in the initial position have to be ajusted accordingly. For example, the following statement is valid

```python
test = sudoku('1  4', N=4)
```

and the solver will find a solution for that 4x4 board and initial position.

Copyright (c) Leonardo Espin. All right reserved.

The code in this repo is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
