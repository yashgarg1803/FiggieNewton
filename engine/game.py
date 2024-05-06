import random
import sys
sys.path.insert(0, "../")
from util.constants import SUITS, EMPTY_ORDER_BOOK, HEARTS, SPADES, CLUBS, DIAMONDS, EMPTY_BID, EMPTY_OFFER, POT_SIZE, EMPTY_DECK, TICKS_PER_ROUND, STARTING_BALANCE
from util.classes import Player, Bid, Offer
import copy

class Game:
    game_number = 0
    
    def __init__(self, players={}, show_messages=True):
        self.players = players # map of (player_id, Player)
        self.game_id = Game.game_number
        Game.game_number += 1
        self.round_number = 0
        self.show_messages = show_messages
        self.balances = {player_id: STARTING_BALANCE for player_id in self.players}

    def add_player(self, player):
        self.players[player.player_id] = player

    def print_message(self, message):
        if "invalid" in message:
            return
        if self.show_messages:
            print(message)

    def init_round(self):
        self.next_order_id = 0
        self.round_number += 1
        self.order_book = copy.deepcopy(EMPTY_ORDER_BOOK)
        

        self.player_hands = {} # map of (player_id, deck of cards (dict of suit: count))
        for player_id in self.players:
            self.player_hands[player_id] = copy.deepcopy(EMPTY_DECK)

        for player_id in self.players:
            self.players[player_id].balance -= POT_SIZE / len(self.players)
        self.pot = POT_SIZE

        self.deal_cards()

    def deal_cards(self):
        """
        Generate a random deck of 40 cards with 8 or 10 of the goal suit, 12 of the
        opposite suit, and 10 or 12 of the remaining two suits.

        Requires: 4 players already added to game
        shuffles deck and then distribute cards to each player
        """
        deck = []
        self.goal_suit = SUITS[random.randint(0, 3)]
        # same color but not goal suit gets 12
        if self.goal_suit == HEARTS:
            deck.extend([DIAMONDS] * 12)
        elif self.goal_suit == DIAMONDS:
            deck.extend([HEARTS] * 12)
        elif self.goal_suit == SPADES:
            deck.extend([CLUBS] * 12)
        elif self.goal_suit == CLUBS:
            deck.extend([SPADES] * 12)

        # goal suit gets 8 or 10 or 10
        self.num_of_goal_suit = random.choice([8, 10, 10])
        deck.extend([self.goal_suit] * self.num_of_goal_suit)

        # one of opposite color gets 10 and other gets rest of cards (8 or 10)
        if self.goal_suit == HEARTS or self.goal_suit == DIAMONDS:
            suit_with_10 = random.choice([SPADES, CLUBS])
            deck.extend([suit_with_10] * 10)
            if suit_with_10 == SPADES:
                deck.extend([CLUBS] * (40 - len(deck)))
            else:
                deck.extend([SPADES] * (40 - len(deck)))
        else:
            suit_with_10 = random.choice([HEARTS, DIAMONDS])
            deck.extend([suit_with_10] * 10)
            if suit_with_10 == HEARTS:
                deck.extend([DIAMONDS] * (40 - len(deck)))
            else:
                deck.extend([HEARTS] * (40 - len(deck)))

        # nth player gets card at Mi + n where n is 0 through 40/M, M = number of players
        random.shuffle(deck)
        counter = 0
        for player_id in self.players:
            for i in range(40 // len(self.players)):
                self.player_hands[player_id][deck[counter + i*(len(self.players))]] += 1
            counter += 1
  
    def start_game(self, num_rounds=1):
        if len(self.players) < 4:
            self.print_message("not enough players")
            return
        
        for player_id in self.players:
            self.players[player_id].balance = 0
        while self.round_number < num_rounds:
            self.do_round()

        self.print_message("game over")
        self.print_message(f"final balances: {self.balances}")
    
    def do_round(self):
        self.init_round()
        self.print_message(f"round {self.round_number} start")
        self.play_round()
        self.end_round()
        self.print_message(f"round {self.round_number} end")
        self.balances = {player_id: self.players[player_id].balance for player_id in self.players}
        self.print_message(f"balances: {self.balances}")

    def play_round(self):
        for player_id in self.players:
            self.players[player_id].send_update({
                "type": "round_start",
                "round_number": self.round_number,
                "hand": self.player_hands[player_id],
                "order_book": self.order_book,
            })
        
        for tick in range(TICKS_PER_ROUND):
            tick_place_orders = []
            tick_accepts = []
            tick_cancels = []
            for player_id in self.players:
                player = self.players[player_id]
                message = player.get_action()


                if message["type"] == "place":
                    price = int(round(message["price"]))
                    suit = message["suit"]
                    order_type = message["order_type"]
                    order_side = order_type + "s" # bc orderbook is a dict of 'bids' and 'offers'
                    counterorder_type = "bid" if order_type == "offer" else "offer"
                    counterorder_side = counterorder_type + "s"
                    sign = 1 if order_type == "bid" else -1

                    # need card to sell it
                    if order_type == "offer" and self.player_hands[player_id][suit] == 0:
                        self.print_message(f"player {player_id} made an invalid action")
                        continue
                    # an order at least as good as counterorder becomes an accepted order if different player
                    # if same player it should be a cancel if greater (same is a valid order)
                    # if better than current order, it should be placed
                    counterorder_id = self.order_book[counterorder_side][suit].player_id
                    counterorder_price = self.order_book[counterorder_side][suit].price
                    if counterorder_id != -1 and player_id != counterorder_id and sign * price >= sign * counterorder_price:
                        tick_accepts.append((player_id, suit, counterorder_type))
                    elif counterorder_id != -1 and player_id == counterorder_id and sign * price >= sign * counterorder_price:
                        tick_cancels.append((player_id, suit, counterorder_type))
                    elif self.order_book[order_side][suit].player_id == -1 \
                            or (order_type == "bid" and price > self.order_book[order_side][suit].price) \
                            or (order_type == "offer" and price < self.order_book[order_side][suit].price): 
                        tick_place_orders.append((player_id, suit, price, order_type))
                    else:
                        self.print_message(f"player {player_id} made an invalid action")

                elif message["type"] == "accept":
                    suit = message["suit"]
                    order_type = message["order_type"]
                    # need card to sell it
                    if order_type == "bid" and self.player_hands[player_id][suit] == 0:
                        self.print_message(f"player {player_id} made an invalid action")
                        continue

                    if self.order_book[order_type + "s"][suit].player_id != player_id \
                            and self.order_book[order_type + "s"][suit].player_id != -1:
                        tick_accepts.append((player_id, suit, order_type))
                    else:
                        self.print_message(f"player {player_id} made an invalid action")

                elif message["type"] == "cancel":
                    suit = message["suit"]
                    order_type = message["order_type"]
                    tick_cancels.append((player_id, suit, order_type))

                elif message["type"] == "pass":
                    pass
                
                else:
                    self.print_message(f"player {player_id} made an invalid action")

                
            update = self.process_tick(tick_place_orders, tick_accepts, tick_cancels)
            update["order_book"] = self.order_book
            for player_id in self.players:
                #player_update = copy.deepcopy(update)
                update["hand"] = self.player_hands[player_id]
                self.players[player_id].send_update(update)
    
    def process_tick(self, tick_place_orders, tick_accepts, tick_cancels):
        if tick_accepts:
            action = random.choice(tick_accepts)
            party_id, suit, order_type = action
            counterorder = self.order_book[order_type + "s"][suit]
            counterparty_id = counterorder.player_id
            price = counterorder.price

            if order_type == "bid":
                if self.player_hands[party_id][suit] == 0:
                    raise Exception("invalid action")
                # party is accepting the bid of the counterparty => party is selling
                self.players[counterparty_id].balance -= price
                self.player_hands[party_id][suit] -= 1

                self.players[party_id].balance += price
                self.player_hands[counterparty_id][suit] += 1
            else:
                if self.player_hands[counterparty_id][suit] == 0:
                    raise Exception("invalid action")
                # party is accepting the offer of the counterparty => party is buying
                self.players[party_id].balance -= price
                self.player_hands[counterparty_id][suit] -= 1

                self.player_hands[party_id][suit] += 1
                self.players[counterparty_id].balance += price

            self.order_book = copy.deepcopy(EMPTY_ORDER_BOOK)
            party_action = f"sells {suit} to" if order_type == "bid" else f"buys {suit} from"
            self.print_message(f"'{party_id}' {party_action} '{counterparty_id}' at {price}")
            return {
                "type": "accept",
                "party_id": party_id,
                "counterparty_id": counterparty_id,
                "order_type": order_type,
                "suit": suit,
                "price": price,
                "message": f"'{party_id}' {party_action} '{counterparty_id}' at {price}",
            }

        for cancel in tick_cancels:
            party_id, suit, order_type = cancel
            price = self.order_book[order_type + "s"][suit].price
            self.order_book[order_type + "s"][suit] = copy.deepcopy(EMPTY_BID) if order_type == "bid" else copy.deepcopy(EMPTY_OFFER)
            self.print_message(f"'{party_id}' cancels {order_type} of {suit} at {price}")
        
        if tick_place_orders:
            order = random.choice(tick_place_orders)
            party_id, suit, price, order_type = order
            self.order_book[order_type + "s"][suit] = Bid(party_id, suit, price) if order_type == "bid" else Offer(party_id, suit, price)
            
            party_action = "bids" if order_type == "bid" else "offers"
            self.print_message(f"'{party_id}' {party_action} {suit} at {price}")
            return {
                "type": "place",
                "party_id": party_id,
                "order_type": order_type,
                "suit": suit,
                "price": price,
                "message": f"'{party_id}' {party_action} {suit} at {price}",
            }
        
        return {
            "type": "update",
        }
    
    def end_round(self):
        max_count = 0
        for player_id in self.players:
            goal_count = self.player_hands[player_id][self.goal_suit]
            self.players[player_id].balance += goal_count * 10
            max_count = max(max_count, goal_count)
        
        max_winners = [player_id for player_id in self.players if self.player_hands[player_id][self.goal_suit] == max_count]
        num_winners = len(max_winners)
        for player_id in max_winners:
            self.players[player_id].balance += (self.pot - self.num_of_goal_suit * 10) / num_winners
        self.balances = {player_id: self.players[player_id].balance for player_id in self.players}
        for player_id in self.players:
            self.players[player_id].send_update({
                "type": "round_end",
                "balances": self.balances,
                "player_hands": self.player_hands,
                "goal_suit": self.goal_suit,
                "num_of_goal_suit": self.num_of_goal_suit,
                "order_book": None
            })

        self.order_book = copy.deepcopy(EMPTY_ORDER_BOOK)
        self.goal_suit = None
        self.pot = 0
        self.player_hands = {}
        self.num_of_goal_suit = None
