# Unbeatable Tic-Tac-Toe AI

A desktop Tic-Tac-Toe game built in Python using Pygame for the graphical interface and an unbeatable AI backend powered by the Minimax decision-tree algorithm.

## Features
* **Interactive GUI:** Built with Pygame, featuring dynamic color shifting for game-over states (Green for Win, Red for Loss, Grey for Tie).
* **Unbeatable AI Engine:** Implements a full recursive Minimax search tree that evaluates all future board states to guarantee the AI never loses.
* **Matrix State Management:** Utilizes NumPy to manage the 3x3 game board data structure for fast state evaluation.

## Tech Stack
* **Language:** Python 3
* **Graphics & Event Handling:** Pygame
* **Data Structures:** NumPy

## Core Concepts Implemented
* **Minimax Algorithm:** A recursive backtracking algorithm used in game theory. The AI maximizes its own score ($+\infty$ for a win) while assuming the human player will minimize the AI's score ($-\infty$ for a loss).
* **Backtracking:** The AI simulates a move, recursively scores the future outcomes, and then clears the square (backtracks) to restore the actual board state before making its final decision.
* **Matrix Grid Mapping:** Translating raw pixel click coordinates dynamically into discrete 2D matrix indices `(row, col)`.

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/abhiswrld/Tic-Tac-Toe-AI.git](https://github.com/abhiswrld/Tic-Tac-Toe-AI.git)