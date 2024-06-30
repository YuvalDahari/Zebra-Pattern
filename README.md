# ZEBRA PATTERN Simulation
This Python script simulates a cellular automaton to create a zebra-like stripe pattern on a grid using Tkinter for the GUI and Matplotlib for plotting measurement data over generations.

## Requirements
- Python 3.x
- Tkinter
- Matplotlib
## Installation
Clone the repository:
```bash
git clone <repository_url>
```
## Install dependencies:
```bash
pip install tkinter matplotlib
```

Run the script zebra_pattern.py to start the simulation. The script initializes a grid where cells change color based on specific rules, aiming to achieve a zebra-like pattern.

## Cellular Automaton Details
*Objective*: Create a preference for a pattern of alternating stripes, i.e., a "white" column, a "black" column, a "white" column, etc.

### Board Configuration:

**Board size**: 80x80 cells
**Square size**: 8x8 pixels
**Initial state**: 50% of cells are "white" and 50% are "black"
### Rules:

- Each cell updates its color based on the colors of its neighbors.
- The rules promote the creation of alternating stripes.
## Algorithm:

- The simulation runs for a fixed number of generations (default: 300).
- The board updates continuously when the play button is pressed.
## Measure of Pattern Consistency
A measure is proposed to calculate how close the automaton is to the perfect state of full and alternating stripes. The logic behind the measure is as follows:

### Horizontal Consistency:
Counts the number of cells that do not match the colors of their horizontal neighbors.
### Vertical Consistency:
Counts the number of cells that match the colors of their vertical neighbors.
The final measure is the average of the horizontal and vertical consistency counts.
## Controls
**Update Board**: Manually update the board once.
**Play**: Start continuous updates.
**Stop**: Pause the simulation.
**Restart**: Reset the board to its initial state.
## Graphical Output
Measure Over Generation: Plots measurement data using Matplotlib to visualize the pattern evolution over generations.
The simulation runs for at least 250 generations and is repeated 10 times with different random starting positions to observe the pattern formation.
