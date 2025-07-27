SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720




REG_SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
REG_RANKS = [
    "Ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
]
ALT_SUITS = ["Hearts", "Stars", "Clubs", "Spades"]
ALT_RANKS = [
    "Ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
    "10",
    "Squire",
    "Knight",
    "Jack",
    "Queen",
    "King",
]

JOKER_RANKS = [
    "Ace",
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
    "player_hand": (200, 600),     # Bottom area
    "ui_info": (900, 50),          # Right side for game info
    "turn_indicator": (500, 10),   # Saying whose turn it is
    "toast_area": (10, 500)        # Messages in bottom left out of the way
}
