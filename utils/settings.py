GAME_SCALE = 2
GAME_CAPTION = "Puzzle Bobble"
BG_COLOR = (255, 255, 255)

# used to calculate collisions. this doesn't affect the sprite
BUBBLE_RADIUS = 7 * GAME_SCALE

BUBBLE_FLOATING_DURATION_MINIMUM = 2
BUBBLE_FLOATING_DURATION_MAXIMUM = 4
BUBBLE_FLOATING_ACCELERATION_X = 2
BUBBLE_FLOATING_ACCELERATION_Y = 5

# the minimum and maximum values for a random x direction when starting floating
# value is divided by 10
BUBBLE_FLOATING_DIRECTION_X_MINIMUM = 1
BUBBLE_FLOATING_DIRECTION_X_MAXIMUM = 3
BUBBLE_TOTAL_POP_ANIMATION_FRAMES = 30

SCORE_SCREEN_POSITION = (0,0)
SCORE_TEXT_COLOR = (255,255,255)
SCORE_TEXT_FONT_SIZE = 20
SCORE_TEXT_FONT_NAME = "monospace"
SCORE_TEXT_BG_COLOR = (255,0,0)

BUBBLE_SHOOTER_ROTATION_DEGREES = 1
BUBBLE_SHOOTER_MINIMUM_ROTATION = 15
BUBBLE_SHOOTER_MAXIMUM_ROTATION = 180 - BUBBLE_SHOOTER_MINIMUM_ROTATION

# Menu settings
START_MENU_CAPTION = "Puzzle Bobble - Start Menu"
GAME_OVER_MENU_CAPTION = "Puzzle Bobble - Game Over"
MENU_WINDOW_SIZE = (400, 400)

INFORMATION_COLOR = (0, 0, 0)
INFORMATION_FONT_SIZE = 32
INFORMATION_SPACING = 32

OPTION_COLOR = (0, 0, 0)
OPTION_SELECTED_COLOR = (100, 100, 100)
OPTION_FONT_SIZE = 64
OPTION_SPACING = 64

PLAY_OPTION = "Play"
EXIT_OPTION = "Exit"
PLAY_AGAIN_OPTION = "Play Again"
START_MENU_OPTION = "Start Menu"

SCORE_INFORMATION = "Score: "
LEVEL_INFORMATION = "Level: "
WIN_INFORMATION = "You Won!"
LOSE_INFORMATION = "You Lost!"