import sys
sys.path.insert(0, "../")
from util import constants
from util.classes import Player
import random


class HumanPlayer(Player):
    def __init__(self):
        id = input("Enter your name: ")
        super(HumanPlayer, self).__init__(id)
        self.updates = []

    def get_action(self):
        for update in self.updates:
            for key, value in update.items():
                if (key == "order_book"):
                    for side in value:
                        print(f"\t{side}")
                        for suit in value[side]:
                            print(f"\t\t{suit}: {str(value[side][suit])}")
                else:
                    print(f"{key}: {value}")    
            print()
        self.updates = []

        action = input("Enter your action: ")

        if action == "bid":
            suit = input("Enter suit: ")
            price = float(input("Enter price: "))
            print()
            return {"type": "place", "action": "place_bid", "suit": suit, "price": price, "order_type": "bid"}
        elif action == "offer":
            suit = input("Enter suit: ")
            price = float(input("Enter price: "))
            print()
            return {"type": "place", "action": "place_offer", "suit": suit, "price": price, "order_type": "offer"}
        elif action == "accept":
            suit = input("Enter suit: ")
            order_type = input("Enter order type: ")
            print()
            return {"type": "accept", "action": "accept", "suit": suit, "order_type": order_type}
        else:
            print()
            return {"type": "pass", "action": "pass"}
        

    def place_bid(self):
        suit = random.choice(constants.SUITS)
        price = random.betavariate(1, 5) * 13
        return {"type": "place", "action": "place_bid", "suit": suit, "price": price, "order_type": "bid"}
    
    def place_offer(self):
        suit = random.choice(constants.SUITS)
        price = random.betavariate(5, 2) * 13
        return {"type": "place", "action": "place_offer", "suit": suit, "price": price, "order_type": "offer"}
    
    def accept(self):
        suit = constants.SUITS[random.randint(0, 3)]
        order_type = random.choice(["bid", "offer"])
        return {"type": "accept", "action": "accept", "suit": suit, "order_type": order_type}


    def send_update(self, update_data):
        self.updates.append(update_data)