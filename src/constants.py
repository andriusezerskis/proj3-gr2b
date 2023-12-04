"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

# Simulation
STEP_TIME = 2000

# Grid
GRID_WIDTH = 10
GRID_HEIGHT = 10

# # Climate
# Temperature difference between winter and summer
SEASON_TEMPERATURE_DIFFERENCE = 20
MAX_TEMPERATURE_DIFFERENCE = 10  # in degrees
MAX_RANDOM_TEMPERATURE_DIFFERENCE = 5  # in degrees
YEAR_DURATION = 1000  # year duration in timesteps
AVERAGE_TEMPERATURE = 10  # in degrees
# speed of the variable temperature change is 1/MAX_TIMESTEP, periodic noise after that
MAX_TIMESTEP = 10000
# but the noise does not tile :(
# number of timesteps before an update (for performance)
NB_STEP_BEFORE_UPDATE = 10

# # Textures
TEXTURE_FOLDER_PATH = "../assets/textures"

# Entities
HUMAN_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/human.png"
FISH_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/fish.png"
ALGAE_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/algae.png"
TREE_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/tree.png"

# Tiles
LAND_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/land.png"
WATER_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/water.png"
SAND_TEXTURE_PATH = f"{TEXTURE_FOLDER_PATH}/sand.png"
