import sys
from util import constants
from util.classes import Player
import random
from agents import cardcounting
import math
import copy
sys.path.insert(0, "../")

class CardCounter(Player):
    # parameters = pAccept, PList, c
    def __init__(self, id):
        super(CardCounter, self).__init__(id)
        
        self.hand = {}
        self.order_book = None
        self.count = {}

    def get_action(self):
        if(self.order_book != None):   
            a = self.try_accept_bid()
            b = self.try_accept_offer()
            if(a["player_id"] != -1):
                return {"type": "accept", "action": "accept", "suit": a["suit"], "order_type": "bid"}
            if(b["player_id"] != -1):
                return {"type": "accept", "action": "accept", "suit": b["suit"], "order_type": "offer"}
        return {"type": "pass", "action": "pass"}
    
    def send_update(self, update_data):

        if(update_data["hand"] != None):
            self.hand = update_data["hand"]
            self.count[self.player_id] = self.hand
        if(update_data["order_book"] != None):
            self.order_book = update_data["order_book"] 
        if(update_data["type"] == "round_start"):
            self.count = {}
        if(update_data["type"] == "accept"):
            print(update_data["message"])
            self.count = cardcounting.count_cards(self.count, update_data)

    def try_accept_bid(self):
        bestBid =  copy.deepcopy(constants.EMPTY_BID).toDict()
        dist = cardcounting.deck_distribution(self.count)
        for suit in self.order_book["bids"].keys():
            order = self.order_book["bids"][suit].toDict()
            if order["player_id"] == -1:
                continue
            if order["price"] >= cardcounting.expected_value_sell(suit, self.hand[suit], dist):
                if(order["price"] > bestBid["price"]):
                    bestBid = order
        
        return bestBid

    def try_accept_offer(self):
         #handle offers
        bestOffer =  copy.deepcopy(constants.EMPTY_OFFER).toDict()
        dist = cardcounting.deck_distribution(self.count)
        for suit in self.order_book["offers"].keys():
            order = self.order_book["offers"][suit].toDict()
            if order["player_id"] == -1:
                continue
            if order["price"] <= cardcounting.expected_value_buy(suit, self.hand[suit], dist):
                if(order["price"] < bestOffer["price"]):
                    bestOffer = order
        
        return bestOffer

   