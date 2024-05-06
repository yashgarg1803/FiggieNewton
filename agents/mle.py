import sys
sys.path.insert(0, "../")
from util import constants
from util.classes import Player
import random
import copy

class MLEPlayer(Player):
    def __init__(self, id):
        super(MLEPlayer, self).__init__(id)
        self.last_trades = copy.deepcopy(constants.EMPTY_DECK)
        self.goal_suit_value = 5

    def get_action(self):
        r = random.random()
        if r > 0.5:
            return self.place_bid()
        elif r > 0:
            return self.place_offer()
        elif r > 0:
            return self.accept()
        else:
            return {"type": "pass", "action": "pass"}
        

    def place_bid(self):
        suit = random.choice(constants.SUITS + [self.goal_suit] * 2)
        
        if suit == self.goal_suit:
            price = min(self.last_trades[suit] + 1, 14)
        else:
            price = random.choice([1, 1, 1, 2, 2, 3])
        return {"type": "place", "action": "place_bid", "suit": suit, "price": price, "order_type": "bid"}
    
    def place_offer(self):
        suit = random.choice(constants.SUITS)
        if suit == self.goal_suit:
            price = random.randrange(20, 40)
        else:
            price = max(random.choice([self.last_trades[suit] - 1, self.last_trades[suit], self.last_trades[suit] + 1]), 1)

        return {"type": "place", "action": "place_offer", "suit": suit, "price": price, "order_type": "offer"}
    
    def accept(self):
        suit = constants.SUITS[random.randint(0, 3)]
        order_type = random.choice(["bid", "offer"])
        return {"type": "accept", "action": "accept", "suit": suit, "order_type": order_type}


    def send_update(self, update_data):
        if(update_data["type"] == "round_start"):
            self.hand = update_data["hand"]
            max_suit = constants.SUITS[0]
            for suit in constants.SUITS:
                if self.hand[suit] > self.hand[max_suit]:
                    max_suit = suit
            self.goal_suit = constants.SUITS[(constants.SUITS.index(max_suit) // 2) + ((constants.SUITS.index(max_suit) + 1) % 2)]
        
        if(update_data["type"] == "accept"):
            suit = update_data["suit"]
            price = update_data["price"]
            self.last_trades[suit] = price

                

