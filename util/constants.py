from .classes import Bid, Offer

# Suits
HEARTS = "hearts"
DIAMONDS = "diamonds"
CLUBS = "clubs"
SPADES = "spades"
SUITS = [HEARTS, DIAMONDS, CLUBS, SPADES]
EMPTY_DECK = {HEARTS: 0, DIAMONDS: 0, CLUBS: 0, SPADES: 0}

# Orders
EMPTY_BID = Bid(-1, "", -1)
EMPTY_OFFER = Offer(-1, "", -1)
EMPTY_BIDS = {HEARTS: EMPTY_BID, DIAMONDS: EMPTY_BID,
              CLUBS: EMPTY_BID, SPADES: EMPTY_BID}
EMPTY_OFFERS = {HEARTS: EMPTY_OFFER, DIAMONDS: EMPTY_OFFER,
                CLUBS: EMPTY_OFFER, SPADES: EMPTY_OFFER}
EMPTY_ORDER_BOOK = {"bids": EMPTY_BIDS, "offers": EMPTY_OFFERS}

# General settings
POT_SIZE = 200  
TOTAL_CARD_COUNT = 40
TICKS_PER_ROUND = 100
STARTING_BALANCE = 0
