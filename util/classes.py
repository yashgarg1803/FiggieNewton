import json
import datetime
from . import constants


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.balance = constants.STARTING_BALANCE

    def privateToDict(self):
        dict = self.__dict__.copy()
        return dict

    def publicToDict(self):
        dict = {
            "player_id": self.player_id,
            "balance": self.balance
        }
        return dict
    
    def get_action(self):
        raise NotImplementedError("get_action() method must be implemented by subclass")
    
    def send_update(self, update_data):
        raise NotImplementedError("send_update() method must be implemented by subclass") 


class Bid:
    def __init__(self, player_id, suit, price):
        self.player_id = player_id
        self.suit = suit
        self.price = price

    def toDict(self):
        return self.__dict__
    
    def __str__(self):
        return f"{self.player_id}, {self.price}"


class Offer:
    def __init__(self, player_id, suit, price):
        self.player_id = player_id
        self.suit = suit
        self.price = price

    def toDict(self):
        return self.__dict__
    
    def __str__(self):
        return f"{self.player_id}, {self.price}"
