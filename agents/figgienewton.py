import sys
from util import constants
from util.classes import Player
import random
from agents import cardcounting
import math
import copy
sys.path.insert(0, "../")

class FiggieNewton(Player):
    # parameters = pAccept, PList, c
    def __init__(self, id, parameters):
        super(FiggieNewton, self).__init__(id)
        # pAccept = 1
        pList = 1
        r = 3
        d = 1
        c = parameters[0]
        
        self.hand = {}
        # self.pAccept = pAccept
        self.pList = pList
        self.c = c
        self.player_weights = {}
        self.order_book = None
        self.r = r
        self.d = d
        self.values = {constants.CLUBS: 3, constants.DIAMONDS: 3, constants.HEARTS: 3, constants.SPADES: 3}
        self.count = {}

    def get_action(self):
        if(self.order_book != None):   
            a = self.try_accept_bid()
            b = self.try_accept_offer()
            if(a["player_id"] != -1):
                # print(self.count)
                # print()
                # print("Bid:", a)
                return {"type": "accept", "action": "accept", "suit": a["suit"], "order_type": "bid"}
            if(b["player_id"] != -1):
                # print(self.count)
                # print()
                # print("Offer:", b)
                return {"type": "accept", "action": "accept", "suit": b["suit"], "order_type": "offer"}
        # return {"type": "pass", "action": "pass"}
        return self.try_list()
            
    
    def send_update(self, update_data):
        if(update_data["type"] == "round_start"):
            self.count = {}
            self.hand = update_data["hand"]
            self.count[self.player_id] = copy.deepcopy(self.hand)
            # print(self.hand)
            # print(self.count)
            self.assign_prior()
            self.order_book = update_data["order_book"] 
        # if update_data["hand"] != None:
        #     self.hand = update_data["hand"]
        if "order_book" in update_data.keys():
            self.order_book = update_data["order_book"] 
        
        if(update_data["type"] == "accept"):
            self.count = cardcounting.count_cards(self.count, update_data)
            
            from util.constants import EMPTY_DECK
            total = {constants.HEARTS: 0, constants.DIAMONDS: 0, constants.CLUBS: 0, constants.SPADES: 0}
            player_hands = self.count
            for player_id in player_hands.keys():
                for suit in player_hands[player_id].keys():
                    total[suit] += player_hands[player_id][suit]
            for suit in total:
                if total[suit] > 12:
                    raise ValueError("Too many cards counted")

            # print("action: ", update_data["message"])
            # print("total: ", total)
            # print("hand: ", self.hand)
            # print("values: ", self.values)
            # print("dist: ", cardcounting.deck_distribution(self.count))
            # print()
            trade_weight = 0
            party_id = update_data["party_id"]
            counterparty_id = update_data["counterparty_id"]
            if party_id not in self.player_weights:
                self.player_weights[party_id] = self.c
            if counterparty_id not in self.player_weights:
                self.player_weights[counterparty_id] = self.c
            if party_id != self.player_id and counterparty_id != self.player_id:
                trade_weight = max(self.player_weights[party_id], self.player_weights[counterparty_id])
            suit = update_data["suit"]
            val = cardcounting.expected_value_buy(suit, self.count[self.player_id][suit], cardcounting.deck_distribution(self.count), r=self.r, d=self.d)
            self.values[suit] = (1 * val + trade_weight * update_data["price"])/(1 + trade_weight)

        if (update_data["type"] == "round_end"):
            balances = update_data["balances"]
            current_balance = balances[self.player_id]
            for player_id in balances:
                if player_id != self.player_id:
                    if balances[player_id] > current_balance:
                        self.player_weights[player_id] = self.c
                    elif current_balance > 0 and balances[player_id] > 0:
                        self.player_weights[player_id] = self.c * balances[player_id] / current_balance
                    else:
                        self.player_weights[player_id] = 0


    def assign_prior(self):
        deck_dist = cardcounting.deck_distribution(self.count)
        for suit in self.count[self.player_id].keys():
            self.values[suit] = cardcounting.expected_value_buy(suit, self.count[self.player_id][suit], deck_dist, self.r, self.d)


    
    def try_accept_bid(self):
        bestBid =  copy.deepcopy(constants.EMPTY_BID).toDict()
        bestProfit = 0
        dist = cardcounting.deck_distribution(self.count)
        for suit in self.order_book["bids"].keys():
            order = self.order_book["bids"][suit].toDict()
            if order["player_id"] == -1:
                continue
            profit = order["price"] - cardcounting.expected_value_sell(suit, self.hand[suit], dist, self.r, self.d)
            if profit > 0:
                if(profit > bestProfit):
                    # print("Accept Bid", suit)
                    # print(order["price"], cardcounting.expected_value_sell(suit, self.hand[suit], dist))
                    # print(self.count)
                    # print()
                    bestBid = order
                    bestProfit = profit
        return bestBid
    
        

    
    def try_accept_offer(self):
        #handle offers
        bestOffer = constants.Offer(-1, "", 100000).toDict()
        bestProfit = 0
        dist = cardcounting.deck_distribution(self.count)
        for suit in self.order_book["offers"].keys():
            order = self.order_book["offers"][suit].toDict()
            if order["player_id"] == -1:
                continue
            profit = cardcounting.expected_value_buy(suit, self.hand[suit], dist, self.r, self.d) - order["price"]
            if profit > 0:
                if(profit > bestProfit):
                    # print("Accept Offer", suit)
                    # print(order["price"], cardcounting.expected_value_sell(suit, self.hand[suit], dist))
                    # print(self.count)
                    # print()
                    bestOffer = order
                    bestProfit = profit
        return bestOffer

    def try_list(self):
        list_bids = []
        list_offers = []
        for suit in self.values:
            #list offer
            cutoffOffer = random.randint(math.ceil(self.values[suit]), math.ceil(self.values[suit] + self.pList))
            cutoffBid = random.randint(math.floor(self.values[suit] - self.pList), math.floor(self.values[suit]))
            list_bids.append((suit, cutoffBid))
            list_offers.append((suit, cutoffOffer))
        rand = random.randint(0, 7)
        if(rand > 3):
            return {"type": "place", "action": "place_offer", "suit": list_offers[rand - 4][0], "price": list_offers[rand - 4][1], "order_type": "offer"}
        else:
            return {"type": "place", "action": "place_bid", "suit": list_bids[rand][0], "price": list_bids[rand][1], "order_type": "bid"}

    # def pdfAccept(self, order):
    #     cutoff = random.randint(math.ceil(self.values[order["suit"]]), math.ceil(self.values[order["suit"]] + self.pAccept))
    #     #print(cutoff, order["price"])
    #     if(order["price"] >= cutoff):
    #         #print("Accepting Bid")
    #         return True
    #     return False

    # def pdfOffer(self, order):
    #     cutoff = random.randint(math.floor(self.values[order["suit"]] - self.pList), math.floor(self.values[order["suit"]]))
    #     # print(cutoff, order["price"])
    #     if(order["price"] <= cutoff):
    #         #print("Accepting Offer")
    #         return True
    #     return False

    # def accept_listings(self, orders, isBid):
    #     best = 0
    #     suit = None
    #     for order in orders:
    #         # if(isBid and self.pdfAccept(order)):
    #         if (isBid):
    #             diff = order["price"] - self.values[order["suit"]]
    #             #print(diff, best)
    #             if(diff > best):
    #                 best = diff
    #                 suit = order["suit"]

    #         # if(not isBid and self.pdfOffer(order)):
    #         if (not isBid):
    #             diff = self.values[order["suit"]] - order["price"]
    #             #print(diff, best)
    #             if(diff > best):
    #                 best = diff
    #                 suit = order["suit"]
    #     return suit
    

    # def try_accept_bid(self):
    #     positiveBids = []

    #     for suit in self.order_book["bids"].keys():
    #         order = self.order_book["bids"][suit].toDict()
    #         if order["player_id"] == -1:
    #             continue
    #         if order["price"] >= self.values[suit]:
    #             positiveBids.append(order)
    #     #     print(order["player_id"], "bids",
    #     #         order["suit"], "at price", order["price"])
    #     # print("Positive Bids:")
    #     # print(positiveBids)
    #     suit = self.accept_listings(positiveBids, True)
    #     if(suit != None):
    #         return {"type": "accept", "action": "accept", "suit": suit, "order_type": "bid"}

    # def try_accept_offer(self):
    #         #handle offers
    #     positiveOffers = []

    #     for suit in self.order_book["offers"].keys():
    #         order = self.order_book["offers"][suit].toDict()
    #         if order["player_id"] == -1:
    #             continue
    #         if order["price"] <= self.values[suit]:
    #             positiveOffers.append(order)
    #     #     print(order["player_id"], "offers",
    #     #         order["suit"], "at price", order["price"])
    #     # print("Positive Offers:")
    #     # print(positiveOffers)
    #     suit = self.accept_listings(positiveOffers, False)
    #     if(suit != None):
    #         return {"type": "accept", "action": "accept", "suit": suit, "order_type": "offer"}
    #     return None