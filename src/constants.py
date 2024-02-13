"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

# Simulation
STEP_TIME = 2000

# Entities
ENTITY_HUNGRY_THRESHOLD = 10
ENTITY_MAX_AGE = 24 * 5
ENTITY_MAX_HUNGER = 24
# Reproduction
# number of timesteps before an entity can reproduce again
ENTITY_REPRODUCTION_COOLDOWN = 10
ENTITY_MAX_HUNGER_REPRODUCTION = 10
ENTITY_MIN_AGE_REPRODUCTION = 10

# Grid
GRID_WIDTH = 100
GRID_HEIGHT = 100

# Rendering size
RENDERING_WIDTH = 50
RENDERING_HEIGHT = 50

# # Climate
# Temperature difference between winter and summer
SEASON_TEMPERATURE_DIFFERENCE = 20
MAX_TEMPERATURE_DIFFERENCE = 10  # in degrees
MAX_RANDOM_TEMPERATURE_DIFFERENCE = 5  # in degrees
YEAR_DURATION = 1000  # year duration in timesteps
AVERAGE_TEMPERATURE = 10  # in degrees
# number of timesteps before an update (for performance)
NB_STEP_BEFORE_UPDATE = 10

# # Generation & Tides
# the level is the maximum height of a tile of a certain type
# the height is in [-1, 1]
# for instance, Water tiles are found from height -1 to WATER_LEVEL
# Sand tiles are found from height WATER_LEVEL to SAND_LEVEL
WATER_LEVEL = 0
SAND_LEVEL = 0.03
LAND_LEVEL = 1
# the water level will oscillate between WATER_LEVEL and MAX_WATER_LEVEL in a sinusoidal manner
# WATER_LEVEL < MAX_WATER_LEVEL < SAND_LEVEL
MAX_WATER_LEVEL = 0.015
DAY_DURATION = 24

# NIGHT MODE
NIGHT_MODE_START = 20
MIDDLE_OF_THE_NIGHT = 1
NIGHT_MODE_FINISH = 6
SUNSET_MODE_START = 18


# WINDOWS
# MAIN_WINDOW
MAIN_WINDOW_TITLE = "Simulation 2D"

# COMMANDS_WINDOW
COMMANDS_WINDOW_TITLE = "Commands"
MOVE_CAMERA_UP = "Move Camera UP : UP ARROW"


# # Textures
TEXTURE_FOLDER_PATH = "../assets/textures"

# Entities
HUMAN_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/human.png"
FISH_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/fish.png"
ALGAE_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/algae.png"
TREE_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/tree.png"
CRAB_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/crab.png"

# Tiles
LAND_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/land.png"
WATER_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/water.png"
SAND_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/sand.png"
BOAT_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/boat.png"

# Special
NIGHT_MODE = f"{TEXTURE_FOLDER_PATH}/nightFilter.png"
SUNSET_MODE = f"{TEXTURE_FOLDER_PATH}/sunset.png"
HIGHLIGHTED_TILE = f"{TEXTURE_FOLDER_PATH}/yellow.png"
