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
    "table_sets": (50, 150),      # Middle area for placed sets
    "player_hand": (200, 600),     # Bottom area
    "ui_info": (900, 50),          # Right side for game info
    "instructions": (10, 500),     # Left side, above player hand
    "turn_indicator": (500, 10),   # Saying whose turn it is
    "game_prompts": (900, 500)      # For draw prompts, win messages, etc.
}

MESSAGE_DURATION = 180 
PURPLE = (200, 100, 255)
OTHER_PURPLE = (138, 43, 226)