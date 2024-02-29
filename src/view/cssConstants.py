"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

FONT = 'Small Fonts'

# COLOR START WINDOWS
BUTTON_COLOR = '#7cac04'
SPIN_COLOR ="background-color: #feb07c;"
HLAYOUT_COLOR = "background-color: white;"
START_BUTTON_STYLE_SHEET = f"background-color: {BUTTON_COLOR}; color: white; border-radius:0.001px; font-size: 30px; width: 5px;"

# COLOR MONITOR
CLICKED_COLOR = '#96a9f9'
NCLICKED_COLOR = '#d0f996'
SPIN_COLOR2 ="background-color: white;"


# STYLESHEET
CLICKED_BUTTON_STYLESHEET = f"background-color: {CLICKED_COLOR}; color: white; border-radius:0.001px"
NOT_CLICKED_BUTTON_STYLESHEET = f"background-color: {NCLICKED_COLOR}; color: black; border-radius:0.001px"


VLAYOUT_COLOR = "background-color: #ddd5fd"

PLOT_COLOR = "magenta"
PLOT_BCKGROUND = "lavender"
FIG_BCKGROUND = "#d8dfe6"

PROGRESS_BAR = """QProgressBar {
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #CD96CD;
    width: 10px;
    margin: 0.5px;
}"""