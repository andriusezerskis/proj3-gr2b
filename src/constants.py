"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Bloomaert, Hà Ûyen Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

# Simulation
STEP_TIME = 2

# Grid
GRID_WIDTH = 5
GRID_HEIGHT = 5

# # Climate
SEASON_TEMPERATURE_DIFFERENCE = 20  # Temperature difference between winter and summer
MAX_TEMPERATURE_DIFFERENCE = 10  # in degrees
MAX_RANDOM_TEMPERATURE_DIFFERENCE = 5  # in degrees
YEAR_DURATION = 1000  # year duration in timesteps
AVERAGE_TEMPERATURE = 10  # in degrees
MAX_TIMESTEP = 10000  # speed of the variable temperature change is 1/MAX_TIMESTEP, periodic noise after that
# but the noise does not tile :(
NB_STEP_BEFORE_UPDATE = 10  # number of timesteps before an update (for performance)

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
