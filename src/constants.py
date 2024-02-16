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
RENDERING_WIDTH = 100
RENDERING_HEIGHT = 100

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
SAND_LEVEL = 0.1
LAND_LEVEL = 0.75
MOUNTAIN_LEVEL = 1
# the water level will oscillate between WATER_LEVEL and MAX_WATER_LEVEL in a sinusoidal manner
# WATER_LEVEL < MAX_WATER_LEVEL < SAND_LEVEL
MAX_WATER_LEVEL = 0.015
DAY_DURATION = 24

# # Entity generation
# the probability that a tile does not contain any entity at generation
EMPTY_TILE_PROBABILITY_GENERATION = 0.75
ENTITY_WEIGHTS = {"Human": 0.5,
                  "Fish": 0.5,
                  "Algae": 1,
                  "Tree": 1,
                  "Crab": 0.2}

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
ENTITIES_FOLDER_PATH = TEXTURE_FOLDER_PATH + "/entities"
TILES_FOLDER_PATH = TEXTURE_FOLDER_PATH + "/tiles"

# Entities
HUMAN_TEXTURE_PATH = f"{ENTITIES_FOLDER_PATH}/human.png"
FISH_TEXTURE_PATH = f"{ENTITIES_FOLDER_PATH}/fish.png"
ALGAE_TEXTURE_PATH = f"{ENTITIES_FOLDER_PATH}/algae.png"
TREE_TEXTURE_PATH = f"{ENTITIES_FOLDER_PATH}/tree.png"
CRAB_TEXTURE_PATH = f"{ENTITIES_FOLDER_PATH}/crab.png"

# Tiles
LAND_TEXTURE_PATH = f"{TILES_FOLDER_PATH}/land.png"
WATER_TEXTURE_PATH = f"{TILES_FOLDER_PATH}/water.png"
SAND_TEXTURE_PATH = f"{TILES_FOLDER_PATH}/sand.png"
MOUNTAIN_TEXTURE_PATH = f"{TILES_FOLDER_PATH}/mountain.png"

# Special
NIGHT_MODE = f"{TEXTURE_FOLDER_PATH}/nightFilter.png"
SUNSET_MODE = f"{TEXTURE_FOLDER_PATH}/sunset.png"
HIGHLIGHTED_TILE = f"{TEXTURE_FOLDER_PATH}/yellow.png"


# Music
MUSIC_PATH = "../assets/music/Popcorn.mp3"


# Translation of entities' names
ENTITIES_NAMES_TRANSLATION = {"Algae": "Algue", "Fish": "Poisson", "Human": "Humain", "Tree": "Arbre", "Crab": "Crabe"}