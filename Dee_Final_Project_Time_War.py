from graphics import Canvas
import time
import random

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SQUARE_SIZE = 20
INITIAL_VELOCITY = 10
START_X = 0
START_Y = 0

DELAY = 0.1

def main():
    """
    Main function to run the game.
    Inspired by 'This Is How You Lose the Time War'.
    Your goal is to collect green energy and don't cross the boundaries!
    """
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # --- OUTER LOOP: Keeps the game running forever so we can restart ---
    while True:
        # Draw a white rectangle to give us a fresh blank screen for the new round
        canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 'white')

        # Set up a fresh game
        square_x = START_X
        square_y = START_Y

        hurdles = []
        square = create_red_oval(canvas, square_x, square_y)
        goal = create_green_oval(canvas, hurdles)

        x_velocity = 0
        y_velocity = INITIAL_VELOCITY

        score = 0
        score_text = create_text(canvas, CANVAS_WIDTH // 2 - 30, 20, "Energy: 0", "blue")

        # --- INNER LOOP: The Animation Loop ---
        while True:
            key = canvas.get_last_key_press()
            if key:
                x_velocity, y_velocity = handle_key_press(key, x_velocity, y_velocity)

            canvas.move(square, x_velocity, y_velocity)

            if is_out_of_bounds(square, canvas):
                show_game_over(canvas, score, "You fell over the edge...")
                break

            if check_collision(square, goal, canvas):
                update_goal_position(goal, canvas, hurdles)  
                score += 1
                score_text = update_text(canvas, score_text, "Energy: " + str(score)) 
                create_hurdle(canvas, hurdles, goal)  

            if check_hurdle_collision(square, hurdles, canvas):
                show_game_over(canvas, score, "Blue blocked your mission...")
                break

            time.sleep(DELAY)

        # --- RESTART WAITER ---
        # After a Game Over, wait for the player to press 'R' to play again
        while True:
            key = canvas.get_last_key_press()

            # Check for both lowercase and uppercase 'space'
            if key == 'SPACE' or key == 'space' or key == ' ':
                break  # Break out of the waiter loop to restart the Outer Loop!
            time.sleep(DELAY)

#-------------------------------------------------------------------------------------------------#

def show_game_over(canvas, score, message):
    """ Clears the screen and shows the game over text properly centered. """
    # Red background
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 'red')
    
    # Push each line left by a different amount based on how long the sentence is
    # Using 'black' text for a stark, classic look
    create_text(canvas, CANVAS_WIDTH // 2 - 45, CANVAS_HEIGHT // 2 - 28, "Game over, Red!", 'black')
    create_text(canvas, CANVAS_WIDTH // 2 - 60, CANVAS_HEIGHT // 2 - 10, message, 'black')
    create_text(canvas, CANVAS_WIDTH // 2 - 90, CANVAS_HEIGHT // 2 + 10, "This is how you lose the time war!", 'black')
    create_text(canvas, CANVAS_WIDTH // 2 - 45, CANVAS_HEIGHT // 2 + 38, "Final Energy: " + str(score), 'black')

    # Give the player the restart instructions
    create_text(canvas, CANVAS_WIDTH // 2 - 55, CANVAS_HEIGHT // 2 + 70, "Press 'Space' to Restart", 'black')

def create_red_oval(canvas, x, y):
    return canvas.create_oval(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, 'red')

def create_green_oval(canvas, hurdles):
    # Define the top-middle scoreboard area to avoid
    score_min_x = (CANVAS_WIDTH // 2) - 60
    score_max_x = (CANVAS_WIDTH // 2) + 60
    score_min_y = 0
    score_max_y = 40

    while True:
        x = random.randrange(0, CANVAS_WIDTH, SQUARE_SIZE)
        y = random.randrange(0, CANVAS_HEIGHT, SQUARE_SIZE)

        # 1. Avoid Scoreboard
        if score_min_x <= x <= score_max_x and score_min_y <= y <= score_max_y:
            continue

        # 2. Avoid Hurdles
        overlapping = False
        for hurdle in hurdles:
            if x == canvas.get_left_x(hurdle) and y == canvas.get_top_y(hurdle):
                overlapping = True
                break

        if not overlapping:
            break

    return canvas.create_oval(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, 'green')

def update_goal_position(goal, canvas, hurdles):
    # Define the top-middle scoreboard area to avoid
    score_min_x = (CANVAS_WIDTH // 2) - 60
    score_max_x = (CANVAS_WIDTH // 2) + 60
    score_min_y = 0
    score_max_y = 40

    while True:
        x = random.randrange(0, CANVAS_WIDTH, SQUARE_SIZE)
        y = random.randrange(0, CANVAS_HEIGHT, SQUARE_SIZE)

        # 1. Avoid Scoreboard
        if score_min_x <= x <= score_max_x and score_min_y <= y <= score_max_y:
            continue

        # 2. Avoid Hurdles
        overlapping = False
        for hurdle in hurdles:
            if x == canvas.get_left_x(hurdle) and y == canvas.get_top_y(hurdle):
                overlapping = True
                break

        if not overlapping:
            break

    canvas.move(goal, x - canvas.get_left_x(goal), y - canvas.get_top_y(goal))

def create_hurdle(canvas, hurdles, goal):
    # Define the top-middle scoreboard area to avoid
    score_min_x = (CANVAS_WIDTH // 2) - 60
    score_max_x = (CANVAS_WIDTH // 2) + 60
    score_min_y = 0
    score_max_y = 40

    goal_x = canvas.get_left_x(goal)
    goal_y = canvas.get_top_y(goal)

    while True:
        x = random.randrange(0, CANVAS_WIDTH, SQUARE_SIZE)
        y = random.randrange(0, CANVAS_HEIGHT, SQUARE_SIZE)

        # 1. Avoid Scoreboard
        if score_min_x <= x <= score_max_x and score_min_y <= y <= score_max_y:
            continue

        # 2. Avoid Goal
        if x == goal_x and y == goal_y:
            continue

        # 3. Avoid other Hurdles
        overlapping = False
        for hurdle in hurdles:
            if x == canvas.get_left_x(hurdle) and y == canvas.get_top_y(hurdle):
                overlapping = True
                break

        if not overlapping:
            break

    hurdle = canvas.create_oval(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, 'blue')
    hurdles.append(hurdle)

def check_hurdle_collision(square, hurdles, canvas):
    """ Checks if Red overlaps with a Blue hurdle at all. """
    square_x = canvas.get_left_x(square)
    square_y = canvas.get_top_y(square)

    for hurdle in hurdles:
        hurdle_x = canvas.get_left_x(hurdle)
        hurdle_y = canvas.get_top_y(hurdle)

        # This logic checks if the boundaries of the two squares overlap at all
        # edited part -- dee
        if (square_x < (hurdle_x + SQUARE_SIZE) and 
            (square_x + SQUARE_SIZE) > hurdle_x and 
            square_y < (hurdle_y + SQUARE_SIZE) and 
            (square_y + SQUARE_SIZE) > hurdle_y):
            return True
    
    return False

def handle_key_press(key, x_velocity, y_velocity):
    """ Updates the velocity based on the exact arrow key names from the library. """
    speed = INITIAL_VELOCITY

    if key == 'LEFT_ARROW' or key == 'ArrowLeft':
        return -speed, 0
    if key == 'RIGHT_ARROW' or key == 'ArrowRight':
        return speed, 0
    if key == 'UP_ARROW' or key == 'ArrowUp':
        return 0, -speed
    if key == 'DOWN_ARROW' or key == 'ArrowDown':
        return 0, speed

    return x_velocity, y_velocity

def is_out_of_bounds(obj, canvas):
    x = canvas.get_left_x(obj)
    y = canvas.get_top_y(obj)
    
    if (x < 0) or (x + SQUARE_SIZE > CANVAS_WIDTH):
        return True
    if (y < 0) or (y + SQUARE_SIZE > CANVAS_HEIGHT):
        return True
    
    return False

def check_collision(square, goal, canvas):
    """ Checks if Red overlaps with a Green energy. """
    square_x = canvas.get_left_x(square)
    square_y = canvas.get_top_y(square)
    
    goal_x = canvas.get_left_x(goal)
    goal_y = canvas.get_top_y(goal)
    
    # This logic checks if the boundaries of the two squares overlap at all
    if (square_x < goal_x + SQUARE_SIZE and 
        square_x + SQUARE_SIZE > goal_x and 
        square_y < goal_y + SQUARE_SIZE and 
        square_y + SQUARE_SIZE > goal_y):
        return True
    
    return False

def create_text(canvas, x, y, text, color):
    """ Back to the original working wrapper without the conflicting font argument! """
    return canvas.create_text(x, y, text, color)

def update_text(canvas, text_id, new_text):
    """
    Deletes the old text and draws the new text with a transparent background.
    """
    canvas.delete(text_id)
    # Subtract 30 to match the initial score placement
    return create_text(canvas, CANVAS_WIDTH // 2 - 30, 20, new_text, "blue")

if __name__ == '__main__':
    main()