"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Bloomaert, Hà Ûyen Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

# Simulation
STEP_TIME = 2

# Grid
GRID_WIDTH = 10
GRID_HEIGHT = 10

# # Climate
SEASON_TEMPERATURE_DIFFERENCE = 20  # Temperature difference between winter and summer
MAX_TEMPERATURE_DIFFERENCE = 10     # in degrees
RANDOM_TEMPERATURE_VARIABILITY = 2  # in degrees
YEAR_DURATION = 100  # year duration in timesteps
AVERAGE_TEMPERATURE = 10

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
