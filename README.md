# Tower of Hanoi Visual Simulator

A complete Python desktop project that visualizes the Tower of Hanoi puzzle using Tkinter.

## Features
- Select from 1 to 10 disks.
- Animated solution with Start and Pause/Resume.
- Step-by-step controls: Next Move and Previous Move.
- Reset puzzle at any time.
- Shows current move, step progress, and the minimum number of moves.
- Move history panel.
- Enforces the Tower of Hanoi rules.
- Uses the recursive algorithm to generate the optimal solution.

## Requirements
- Python 3.8 or later
- Tkinter (normally included with Python)

No third-party Python packages are required.

## How to run
1. Extract `tower_of_hanoi_visual_simulator.zip`.
2. Open a terminal or command prompt in the extracted folder.
3. Run:

   ```bash
   python main.py
   ```

   On some systems, use `python3 main.py`.

## How it works
The minimum number of moves required for `n` disks is:

`M = 2^n - 1`

The recursive algorithm follows these steps:
1. Move `n - 1` disks from the source rod to the auxiliary rod.
2. Move the largest disk from the source rod to the destination rod.
3. Move `n - 1` disks from the auxiliary rod to the destination rod.

## Project structure
```
tower_of_hanoi_visual_simulator/
├── main.py
├── README.md
└── requirements.txt
```

## Suggested project report points
- **Title:** Tower of Hanoi Visual Simulator
- **Objective:** To demonstrate the optimal Tower of Hanoi solution visually and sequentially.
- **Language:** Python
- **GUI library:** Tkinter
- **Algorithm:** Recursion
- **Time complexity:** O(2^n)
- **Auxiliary space:** O(n) recursion depth, excluding the stored move list
- **Formula:** Minimum moves = 2^n - 1
