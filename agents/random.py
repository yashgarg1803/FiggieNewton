import sys
sys.path.insert(0, "../")
from util import constants
from util.classes import Player
import random


class RandomPlayer(Player):
    def __init__(self, id):
        super(RandomPlayer, self).__init__(id)
    
    def get_action(self):
        r = random.random()
        if r > 0.75:
            return self.place_bid()
        elif r > 0.5:
            return self.place_offer()
        elif r > 0.25:
            return self.accept()
        else:
            return {"type": "pass", "action": "pass"}
        

    def place_bid(self):
        suit = random.choice(constants.SUITS)
        price = random.randint(0, 100)
        return {"type": "place", "action": "place_bid", "suit": suit, "price": price, "order_type": "bid"}
    
    def place_offer(self):
        suit = random.choice(constants.SUITS)
        price = random.randint(0, 100)
        return {"type": "place", "action": "place_offer", "suit": suit, "price": price, "order_type": "offer"}
    
    def accept(self):
        suit = constants.SUITS[random.randint(0, 3)]
        order_type = random.choice(["bid", "offer"])
        return {"type": "accept", "action": "accept", "suit": suit, "order_type": order_type}


    def send_update(self, update_data):
        pass