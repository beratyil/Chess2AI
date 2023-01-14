
# Chess AI
Basic Chess AI written in Python 3. 

Uses the Alpha-Beta algorithm to search for the best move. From different than the original repo,
I have implemented new heuristic functions.
The reference of most of these heuristic functions are taken from "Programming A Computer For Playing Chess", Claude E. Shannon, 1949.

I have seen some bugs related with Check-Mate and fix them.

In order to make the game faster, I added new functionality to board class.

<img src="./preview.png" width="200" alt="Python Chess AI Program">

## Getting started

### Example Moves
Moves should have the following format:
```
A2 A4
```
This will move the piece from position A2 to A4.