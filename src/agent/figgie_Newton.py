# fmt: off
import asyncio
import websockets
import controller
import random
import pretty_printer as pp
import sys
sys.path.insert(0, "../")
from util.constants import SUITS, EMPTY_ORDER_BOOK, HEARTS, SPADES, CLUBS, DIAMONDS, EMPTY_BID, EMPTY_OFFER, BROADCAST_PERIOD
# fmt: on

'''
A bot that works
'''

uri = "ws://127.0.0.1:8000/ws"


class FiggieNewton:
    def __init__(self, pAccept, pList, c, start_round):
        self.player_id = "Figgie Newton"
        self.pAccept = pAccept
        self.pList = pList
        self.c = c
        self.start_round = start_round
        self.values = {CLUBS: 0, DIAMONDS: 0, HEARTS: 0, SPADES: 0} #valuation of a card of suit

    def assign_prior(self, starting_hand):
        for suit in starting_hand:
            self.values[suit] = 3
    
    def pdfAccept(self, order):
        cutoff = random.randint(self.values[order["suit"]], self.values[order["suit"]] + self.pAccept)
        print(cutoff, order["price"])
        if(order["price"] >= cutoff):
            print("Accepting Bid")
            return True
        return False

    def pdfOffer(self, order):
        cutoff = random.randint(self.values[order["suit"]] - self.pList, self.values[order["suit"]])
        print(cutoff, order["price"])
        if(order["price"] <= cutoff):
            print("Accepting Offer")
            return True
        return False

    def accept_listings(self, orders, isBid):
        best = 0
        suit = None
        for order in orders:
            if(isBid and self.pdfAccept(order)):
                diff = order["price"] - self.values[order["suit"]]
                print(diff, best)
                if(diff > best):
                    best = diff
                    suit = order["suit"]

            if(not isBid and self.pdfOffer(order)):
                diff = self.values[order["suit"]] - order["price"]
                print(diff, best)
                if(diff > best):
                    best = diff
                    suit = order["suit"]
        return suit
            

    async def run(self):
        async with websockets.connect(uri) as websocket:
            await controller.add_player(websocket, self.player_id)
            if (self.start_round):
                await controller.start_round(websocket)
            
            request = await controller.get_game_update(websocket)
            # request should either be add_player
            # or an error saying that player already exists


            pp.print_state(request)
            playerInfo = await controller.round_started(websocket)
            while (playerInfo == None):
                # Wait until round starts
                playerInfo = await controller.round_started(websocket)
                pass
            
            hand = playerInfo["hand"]
            self.assign_prior(hand)
            print(hand)
            print(self.values)

            while True:
                try:
                    game_state = await controller.get_game_update(websocket)                
                
                    order_book = None

                    if ("order_book" in game_state["data"].keys()):
                        order_book = game_state["data"]["order_book"]
                

                    if(order_book != None):   
                        #handle bids
                        #Find positive ev bids and decide whether or not to accept them

                        positiveBids = []

                        for suit in order_book["bids"].keys():
                            order = order_book["bids"][suit]
                            if order["order_id"] == -1:
                                continue
                            if order["price"] >= self.values[suit]:
                                positiveBids.append(order)
                            print(order["player_id"], "bids",
                                order["suit"], "at price", order["price"])
                        print("Positive Bids:")
                        print(positiveBids)
                        suit = self.accept_listings(positiveBids, True)
                        if(suit != None):
                            await controller.accept_bid(websocket, self.player_id, suit)
                    
                        #handle offers
                        positiveOffers = []

                        for suit in order_book["offers"].keys():
                            order = order_book["offers"][suit]
                            if order["order_id"] == -1:
                                continue
                            if order["price"] <= self.values[suit]:
                                positiveOffers.append(order)
                            print(order["player_id"], "bids",
                                order["suit"], "at price", order["price"])
                        print("Positive Offers:")
                        print(positiveOffers)
                        suit = self.accept_listings(positiveOffers, False)
                        if(suit != None):
                            await controller.accept_offer(websocket, self.player_id, suit)

                    accepted_order = None
                    if (game_state["type"] == "accept_order"):
                        accepted_order = game_state["data"]["accepted_order"]
                        accepted_suit = accepted_order["suit"]
                        accepted_price = accepted_order["price"]

                        self.values[accepted_suit] = (self.c * self.values[accepted_suit] + 1 * accepted_price)/(self.c + 1)
                        self.c = self.c + 1
                        

                    pp.print_state(game_state)
                    print("Hand:")
                    print(hand)
                    print("Current Values:")
                    print(self.values)
                    #handle listings
                    await asyncio.sleep(1)

                except websockets.ConnectionClosed as e:
                    websocket = await websocket.connect(uri)


figgieBot = FiggieNewton(
    1, 1, 10, start_round=True)
asyncio.get_event_loop().run_until_complete(figgieBot.run())
