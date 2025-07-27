SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720




REG_SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
REG_RANKS = [
    "ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "jack",
    "queen",
    "king",
]
ALT_SUITS = ["Hearts", "Stars", "Clubs", "Spades"]
ALT_RANKS = [
    "ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
    "10",
    "squire",
    "knight",
    "jack",
    "queen",
    "king",
]

JOKER_RANKS = [
    "ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
    "10",
]

ZONES = {
    "deck": (50, 350),             # Left side, middle
    "discard": (150, 350),         # Next to deck
    "computer_hand": (300, 50),    # Top area
    "table_sets": (50, 150),       # Middle area for placed sets
    "player_hand": (250, 600),     # Bottom area
    "ui_info": (980, 20),          # Right side for game info
    "turn_indicator": (500, 10),   # Saying whose turn it is
    "toast_area": (50, 460)        # Messages in bottom left out of the way
}
