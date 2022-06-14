# Sudoku solver
The solver is implemented in a class, and uses backtraking to explore the solution space. To use it instanciate the class

```python
test = sudoku(initial_position)
```

where `initial_position` is a 81-characters-long string which holds the initial position, read from the top-left corner to the bottom right one. For example

```python
'5...8..49...5...3..673....115..........2.8..........187....415..3...2...49..5...3'
```

anything that is not a digit will produce an emtpy position at that index. Also, strings shorter than 81 characters can be used, if the initial position does not include the bottom-right corner.

To search for a solution, run `test.fill_board()`. The solver will show an animation of the progress of the search. The final solution will be stored in `test.board` as a numpy array.

