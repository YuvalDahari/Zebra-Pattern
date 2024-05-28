import tkinter as tk
import random
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
SQUARE_SIZE = 8
BOARD_ROWS = 80
BOARD_COLUMNS = 80
COLORS = ['white', 'black']
CURRENT_SPIN = 0
MATRIX_COLORS = [[[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)],
                 [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]]
PLAY_BUTTON = False
UPDATE_INTERVAL = 50
rectangles = {}
GENERATION = 300
CURRENT_GENERATION = 0
CURRENT_MEASUREMENT = 0
NUM_RUN = 10
CURRENT_RUN = 0
GRAPH_INFO = []


# Function to initialize the board
def init_board(canvas):
    """Initialize the board with random colors."""
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS):
            x0 = j * SQUARE_SIZE
            y0 = i * SQUARE_SIZE
            x1 = x0 + SQUARE_SIZE
            y1 = y0 + SQUARE_SIZE
            color = random.choice(COLORS)
            MATRIX_COLORS[CURRENT_SPIN][i][j] = color
            rect_id = canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')
            rectangles[(i, j)] = rect_id


# Function to get neighboring' colors
def neighboring_colors(row, col):
    """Extracts the colors of given cell's neighbors."""
    # Calculate the indices of neighboring cells, handling wrapping around the board
    upper_neighbor = (row + 1 + BOARD_ROWS) % BOARD_ROWS
    lower_neighbor = (row - 1 + BOARD_ROWS) % BOARD_ROWS
    right_neighbor = (col - 1 + BOARD_COLUMNS) % BOARD_COLUMNS
    left_neighbor = (col + 1 + BOARD_COLUMNS) % BOARD_COLUMNS

    # Retrieve colors of neighboring cells
    color_upper_neighbor = MATRIX_COLORS[CURRENT_SPIN][upper_neighbor][col]
    color_lower_neighbor = MATRIX_COLORS[CURRENT_SPIN][lower_neighbor][col]
    color_right_neighbor = MATRIX_COLORS[CURRENT_SPIN][row][right_neighbor]
    color_left_neighbor = MATRIX_COLORS[CURRENT_SPIN][row][left_neighbor]
    color_upper_right_neighbor = MATRIX_COLORS[CURRENT_SPIN][upper_neighbor][right_neighbor]
    color_upper_left_neighbor = MATRIX_COLORS[CURRENT_SPIN][upper_neighbor][left_neighbor]
    color_lower_right_neighbor = MATRIX_COLORS[CURRENT_SPIN][lower_neighbor][right_neighbor]
    color_lower_left_neighbor = MATRIX_COLORS[CURRENT_SPIN][lower_neighbor][left_neighbor]

    return (color_upper_neighbor, color_lower_neighbor, color_right_neighbor, color_left_neighbor,
            color_upper_right_neighbor, color_upper_left_neighbor, color_lower_right_neighbor,
            color_lower_left_neighbor)


# Function implementing the logic to determine the color of a cell
def machine(row, col):
    """Apply the machine logic to determine the color of a cell."""
    # Extract colors of neighboring cells
    (color_upper_neighbor, color_lower_neighbor, color_right_neighbor, color_left_neighbor,
     color_upper_right_neighbor, color_upper_left_neighbor, color_lower_right_neighbor,
     color_lower_left_neighbor) = neighboring_colors(row, col)

    # Apply logic to determine the color of the current cell based on its neighbors
    # Checking the column neighbors and matching them if they are the same color
    if color_upper_neighbor == color_lower_neighbor:
        return color_upper_neighbor
    else:
        # List of all neighbors in the right and left column
        neighbors = [
            color_right_neighbor, color_upper_right_neighbor, color_lower_left_neighbor,
            color_left_neighbor, color_upper_left_neighbor, color_lower_right_neighbor
        ]

        # Check all permutations of 3 neighbors from the sides and return the opposite color if they are all the same
        for comb in combinations(neighbors, 3):
            if len(set(comb)) == 1:
                return COLORS[1] if comb[0] == COLORS[0] else COLORS[0]


# Function to reset the board
def reset_board(canvas):
    """Reset the board to its initial state."""
    global CURRENT_GENERATION
    global CURRENT_SPIN
    global GRAPH_INFO
    global CURRENT_MEASUREMENT
    CURRENT_SPIN = 0
    GRAPH_INFO = []
    plot_measurements()
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS):
            color = random.choice(COLORS)
            MATRIX_COLORS[CURRENT_SPIN][i][j] = color
            rect_id = rectangles[(i, j)]
            canvas.itemconfig(rect_id, fill=color)
    CURRENT_GENERATION = 0
    update_label.config(text=f"Generation Count: {CURRENT_GENERATION}")
    CURRENT_MEASUREMENT = get_measure()
    measure_label.config(text=f"Current Measurement: {CURRENT_MEASUREMENT}")


# Function to update the measure Over Generation graph
def plot_measurements():
    """Create the plot with the generation as x-axis and the measurement as y-axis."""
    ax.clear()
    x_values = [point[0] for point in GRAPH_INFO]
    y_values = [point[1] for point in GRAPH_INFO]
    ax.plot(x_values, y_values)
    ax.set_title('measure Over Generation')
    ax.set_xlabel('Generation')
    ax.set_ylabel('measure')
    canvas_graph.draw()


# Function to update the board
def update_board(canvas):
    """Update the board based on the machine logic."""
    global CURRENT_SPIN
    global PLAY_BUTTON
    global CURRENT_GENERATION
    global CURRENT_MEASUREMENT
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS):
            color = machine(i, j)
            MATRIX_COLORS[(CURRENT_SPIN + 1) % 2][i][j] = color
            rect_id = rectangles[(i, j)]
            canvas.itemconfig(rect_id, fill=color)
    CURRENT_MEASUREMENT = get_measure()
    GRAPH_INFO.append((CURRENT_GENERATION, CURRENT_MEASUREMENT))
    CURRENT_SPIN = (CURRENT_SPIN + 1) % 2
    plot_measurements()
    update_label.config(text=f"Generation Count: {CURRENT_GENERATION}")
    measure_label.config(text=f"Current Measurement: {CURRENT_MEASUREMENT}")
    CURRENT_GENERATION += 1
    if CURRENT_GENERATION == GENERATION + 1:
        PLAY_BUTTON = False
        play_button.config(state=tk.NORMAL)
        update_button.config(state=tk.NORMAL)
        return


# Function to calculate the measure of the board
def get_measure():
    """Calculate how close the matrix to 'zebra' form."""
    horizontal_consistency_count = 0
    vertical_consistency_count = 0

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            current_color = MATRIX_COLORS[CURRENT_SPIN][row][col]

            # Extract colors of neighboring cells
            (color_upper_neighbor, color_lower_neighbor, color_right_neighbor, color_left_neighbor, _, _, _, _) =\
                neighboring_colors(row, col)

            # Check horizontal neighbors
            if current_color != color_left_neighbor and current_color != color_right_neighbor:
                horizontal_consistency_count += 1

            # Check vertical neighbors
            if current_color == color_upper_neighbor and current_color == color_lower_neighbor:
                vertical_consistency_count += 1

    # Calculate the consistency measures
    total_cells = BOARD_ROWS * BOARD_COLUMNS
    m_horizontal = horizontal_consistency_count / total_cells
    m_vertical = vertical_consistency_count / total_cells

    # Return the average between the measures
    return (m_horizontal + m_vertical) / 2


# Function to continuously update the board
def loop(canvas):
    """Continuously update the board."""
    if PLAY_BUTTON:
        update_board(canvas)
        canvas.after(UPDATE_INTERVAL, lambda: loop(canvas))


# Function to start playing
def play(canvas):
    """Start playing the simulation."""
    global PLAY_BUTTON
    PLAY_BUTTON = True
    loop(canvas)
    play_button.config(state=tk.DISABLED)
    update_button.config(state=tk.DISABLED)


# Function to stop playing
def stop():
    """Stop the simulation."""
    global PLAY_BUTTON
    PLAY_BUTTON = False
    play_button.config(state=tk.NORMAL)
    update_button.config(state=tk.NORMAL)


# Main function
if __name__ == '__main__':
    # Set up the Tkinter root window
    root = tk.Tk()
    root.title("ZEBRA PATTERN")

    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
    fig, ax = plt.subplots()
    canvas_graph = FigureCanvasTkAgg(fig, master=control_frame)
    canvas_graph.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    # Create the Tkinter canvas
    c = tk.Canvas(root, width=BOARD_COLUMNS * SQUARE_SIZE, height=BOARD_ROWS * SQUARE_SIZE)
    c.pack()

    # Initialize the board
    init_board(c)

    # Add buttons and labels
    update_button = tk.Button(root, text="Update Board", command=lambda: update_board(c))
    update_button.pack(side=tk.LEFT)

    play_button = tk.Button(root, text="Play", command=lambda: play(c))
    play_button.pack(side=tk.LEFT)

    stop_button = tk.Button(root, text="Stop", command=stop)
    stop_button.pack(side=tk.LEFT)

    restart_button = tk.Button(root, text="Restart", command=lambda: reset_board(c))
    restart_button.pack(side=tk.LEFT)

    update_label = tk.Label(root, text=f"Generation Count: {CURRENT_GENERATION}")
    CURRENT_MEASUREMENT = get_measure()
    measure_label = tk.Label(root, text=f"Current Measurement: {CURRENT_MEASUREMENT}")
    update_label.pack(side=tk.LEFT)
    measure_label.pack(side=tk.LEFT)

    # Run the Tkinter main loop
    tk.mainloop()
