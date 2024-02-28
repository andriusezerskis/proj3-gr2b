"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
from enum import Enum
import json

# STYLESHEET
CLICKED_BUTTON_STYLESHEET = "background-color: blue; color: white;"
NOT_CLICKED_BUTTON_STYLESHEET = "background-color: green; color: white;"


ENTITY_DEAD_MESSAGE = "L'entité est morte"
ENTITY_NOT_SELECTED = "Pas d'entité sélectionnée"

# Entities
ENTITY_HUNGRY_THRESHOLD = 10
ENTITY_MAX_AGE = 24 * 5
ENTITY_MAX_HUNGER = 24
# Reproduction
# number of timesteps before an entity can reproduce again
# ENTITY_MAX_HUNGER_REPRODUCTION > ENTITY_MIN_AGE_REPRODUCTION or else we could have a self-sufficient
# species that does not eat
ENTITY_REPRODUCTION_COOLDOWN = 24
ENTITY_MAX_HUNGER_REPRODUCTION = 10
ENTITY_MIN_AGE_REPRODUCTION = 12
PLANT_REPRODUCTION_PROBABILITY = 0.07
PLANT_ADJACENT_PEERS_AUTO_DEATH_THRESHOLD = 6
PLANT_PROBABILITY_DEATH_IF_TOO_MUCH_PEERS = 0.75


# Rendering size
RENDERING_WIDTH = 100
RENDERING_HEIGHT = 100

# Simulation
STEP_TIME = 2000

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

# the water level will oscillate between WATER_LEVEL and MAX_WATER_LEVEL in a sinusoidal manner
# WATER_LEVEL < MAX_WATER_LEVEL < SAND_LEVEL
MAX_WATER_LEVEL = 0.05
DAY_DURATION = 24

# # Entity generation
# the probability that a tile does not contain any entity at generation
EMPTY_TILE_PROBABILITY_GENERATION = 0.75

# NIGHT MODE
NIGHT_MODE_START = 18
MIDDLE_OF_THE_NIGHT = 1
NIGHT_MODE_FINISH = 8
SUNSET_MODE_START = 16

MAX_TILE_FILTER_OPACITY = 0.7

# Types of disasters
DISASTERS = {}

# WINDOWS
# MAIN_WINDOW
MAIN_WINDOW_TITLE = "Simulation 2D"

# COMMANDS_WINDOW
COMMANDS_WINDOW_TITLE = "Commands"
MOVE_CAMERA_UP = "Move Camera UP : UP ARROW"


# # Textures
TEXTURE_SIZE = 2048
TEXTURE_FOLDER_PATH = "../../assets/textures"
ENTITIES_TEXTURE_FOLDER_PATH = TEXTURE_FOLDER_PATH + "/entities"
TILES_TEXTURE_FOLDER_PATH = TEXTURE_FOLDER_PATH + "/tiles"
ITEMS_TEXTURE_FOLDER_PATH = TEXTURE_FOLDER_PATH + "/items"
EFFECTS_TEXTURE_FOLDER_PATH = TEXTURE_FOLDER_PATH + "/effects"

# Special
NIGHT_MODE = "#090957"
SUNSET_MODE = "#fc995b"
HIGHLIGHTED_TILE = f"{EFFECTS_TEXTURE_FOLDER_PATH}/yellow.png"
FIRE = f"{EFFECTS_TEXTURE_FOLDER_PATH}/fire.png"
ICE = f"{EFFECTS_TEXTURE_FOLDER_PATH}/ice.png"

# jsons
ENTITY_PARAMETERS_FILE_PATH = "../config/entities.json"
TILE_PARAMETERS_FILE_PATH = "../config/tiles.json"
LOOT_PARAMETERS_FILE_PATH = "../config/loots.json"
CRAFT_PARAMETERS_FILE_PATH = "../config/crafts.json"

with open(ENTITY_PARAMETERS_FILE_PATH, "r") as f:
    ENTITY_PARAMETERS: dict = json.load(f)

with open(TILE_PARAMETERS_FILE_PATH, "r") as f:
    TILE_PARAMETERS: dict = json.load(f)

with open(LOOT_PARAMETERS_FILE_PATH, "r") as f:
    LOOT_PARAMETERS: dict = json.load(f)

with open(CRAFT_PARAMETERS_FILE_PATH, "r") as f:
    CRAFT_PARAMETERS: dict = json.load(f)

# Entity info text
HEALTH_BAR_TEXT = "Santé : "
NAME_TEXT = "Prénom : "
AGE_TEXT = "Âge : "
HUNGER_TEXT = "Faim"


class Disaster(str, Enum):
    FIRE_TEXT = "Explosion",
    ICE_TEXT = "Froid glacial"
    INVASION_TEXT = "Invasion de:"


CONTROL_PLAYER = "Contrôler"
RELEASE_PLAYER = "Relâcher"

TIME_FORMAT = "%e %A: %H hours"


GRID_STYLESHEET = """
            QScrollBar:horizontal {
                background-color: #808080; /* Couleur de fond */
                height: 15px; /* Hauteur */
            }

            QScrollBar::handle:horizontal {
                background-color: #C0C0C0; /* Couleur du curseur */
                min-width: 50px; /* Largeur minimale */
            }

            QScrollBar::add-line:horizontal {
                background: none;
            }

            QScrollBar::sub-line:horizontal {
                background: none;
            }

            QScrollBar:vertical {
                background-color: #808080; /* Couleur de fond */
                width: 15px; /* Largeur */
            }

            QScrollBar::handle:vertical {
                background-color: #C0C0C0; /* Couleur du curseur */
                min-height: 50px; /* Hauteur minimale */
            }

            QScrollBar::add-line:vertical {
                background: none;
            }

            QScrollBar::sub-line:vertical {
                background: none;
            }
        """
