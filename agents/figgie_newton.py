import sys
from util import constants
from util.classes import Player
import random
from agents import cardcounting
import math
sys.path.insert(0, "../")

class FiggieNewton(Player):
    # parameters = pAccept, PList, c
    def __init__(self, id, parameters):
        super(FiggieNewton, self).__init__(id)
        pAccept = parameters[0]
        pList = parameters[1]
        c = parameters[2]
        
        self.hand = {}
        self.pAccept = pAccept
        self.pList = pList
        self.c = c
        self.order_book = None
        self.values = {constants.CLUBS: 3, constants.DIAMONDS: 3, constants.HEARTS: 3, constants.SPADES: 3}

    def get_action(self):
        if(self.order_book != None):   
            a = self.try_accept_bid()
            b = self.try_accept_offer()
            if(a != None):
                #print(a)
                return a
            if(b != None):
                #print(b)
                return b
        return self.try_list()    
    
    def send_update(self, update_data):

        if(update_data["hand"] != None):
            self.hand = update_data["hand"]
        if(update_data["type"] == "round_start"):
            self.assign_prior({self.player_id: update_data["hand"]})
            # print(self.hand)
            # print(self.values)
            return
        if(update_data["order_book"] != None):
            self.order_book = update_data["order_book"] 
        if(update_data["type"] == "accept"):
            self.values[update_data["suit"]] = (self.c * self.values[update_data["suit"]] + 1 * update_data["price"])/(self.c + 1)
            self.c = self.c + 1

    def assign_prior(self, starting_hand):
        deck_dist = cardcounting.deck_distribution(starting_hand)
        for suit in starting_hand[self.player_id].keys():
            self.values[suit] = cardcounting.expected_value_buy(suit, starting_hand[self.player_id][suit], deck_dist)

    def try_accept_bid(self):
        positiveBids = []

        for suit in self.order_book["bids"].keys():
            order = self.order_book["bids"][suit].toDict()
            if order["player_id"] == -1:
                continue
            if order["price"] >= self.values[suit]:
                positiveBids.append(order)
        #     print(order["player_id"], "bids",
        #         order["suit"], "at price", order["price"])
        # print("Positive Bids:")
        # print(positiveBids)
        suit = self.accept_listings(positiveBids, True)
        if(suit != None):
            return {"type": "accept", "action": "accept", "suit": suit, "order_type": "bid"}
        
    def try_accept_offer(self):
         #handle offers
        positiveOffers = []

        for suit in self.order_book["offers"].keys():
            order = self.order_book["offers"][suit].toDict()
            if order["player_id"] == -1:
                continue
            if order["price"] <= self.values[suit]:
                positiveOffers.append(order)
        #     print(order["player_id"], "offers",
        #         order["suit"], "at price", order["price"])
        # print("Positive Offers:")
        # print(positiveOffers)
        suit = self.accept_listings(positiveOffers, False)
        if(suit != None):
            return {"type": "accept", "action": "accept", "suit": suit, "order_type": "offer"}
        return None

    def try_list(self):
        list_bids = []
        list_offers = []
        for suit in self.values:
            #list offer
            cutoffOffer = random.randint(math.ceil(self.values[suit]), math.ceil(self.values[suit] + self.pList))
            cutoffBid = random.randint(math.ceil(self.values[suit] - self.pList), math.ceil(self.values[suit]))
            list_bids.append((suit, cutoffBid))
            list_offers.append((suit, cutoffOffer))
        rand = random.randint(0, 7)
        if(rand > 3):
            return {"type": "place", "action": "place_offer", "suit": list_offers[rand - 4][0], "price": list_offers[rand - 4][1], "order_type": "offer"}
        else:
            return {"type": "place", "action": "place_bid", "suit": list_bids[rand][0], "price": list_bids[rand][1], "order_type": "bid"}

    def pdfAccept(self, order):
        cutoff = random.randint(math.ceil(self.values[order["suit"]]), math.ceil(self.values[order["suit"]] + self.pAccept))
        #print(cutoff, order["price"])
        if(order["price"] >= cutoff):
            #print("Accepting Bid")
            return True
        return False

    def pdfOffer(self, order):
        cutoff = random.randint(math.floor(self.values[order["suit"]] - self.pList), math.floor(self.values[order["suit"]]))
        # print(cutoff, order["price"])
        if(order["price"] <= cutoff):
            #print("Accepting Offer")
            return True
        return False

    def accept_listings(self, orders, isBid):
        best = 0
        suit = None
        for order in orders:
            if(isBid and self.pdfAccept(order)):
                diff = order["price"] - self.values[order["suit"]]
                #print(diff, best)
                if(diff > best):
                    best = diff
                    suit = order["suit"]

            if(not isBid and self.pdfOffer(order)):
                diff = self.values[order["suit"]] - order["price"]
                #print(diff, best)
                if(diff > best):
                    best = diff
                    suit = order["suit"]
        return suit