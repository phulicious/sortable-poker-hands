'''
Sortable Poker Hands

A famous casino is suddenly faced with a sharp decline of their revenues. They decide to offer Texas hold'em also online. Can you help them by writing an algorithm that can rank poker hands?

Task:

Create a poker hand that has a constructor that accepts a string containing 5 cards:
hand = PokerHand("KS 2H 5C JD TD")
The characteristics of the string of cards are:
A space is used as card seperator
Each card consists of two characters
The first character is the value of the card, valid characters are:
`2, 3, 4, 5, 6, 7, 8, 9, T(en), J(ack), Q(ueen), K(ing), A(ce)`
The second character represents the suit, valid characters are:
`S(pades), H(earts), D(iamonds), C(lubs)`

The poker hands must be sortable by rank, the highest rank first:
hands = []
hands.append(PokerHand("KS 2H 5C JD TD"))
hands.append(PokerHand("2C 3C AC 4C 5C"))
hands.sort() (or sorted(hands))
Apply the Texas Hold'em rules for ranking the cards.
There is no ranking for the suits.
An ace can either rank high or rank low in a straight or straight flush. Example of a straight with a low ace:
`"5C 4D 3C 2S AS"`

Note: there are around 25000 random tests, so keep an eye on performances.
'''

from collections import defaultdict
from typing import List


class PokerHand(object):
    '''Representation of a poker hand and its basic characteristics.

    The PokerHands Weight are:
        Straight Flush  : 1
        Four of a Kind  : 2
        Full House      : 3
        Flush           : 4
        Straight        : 5
        Three of a Kind : 6
        Two Pairs       : 7
        Pair            : 8
        High Card       : 9
    
    In the sample test, the sorted poker hands are displayed with the highest ranking hand in the top.
    The sort method, sorts in ascending order, this means the highest weight would have to be considered the lowest number.

    If there are ties between the hands weight, the tiebreaker shall be resolved as follow:
        Straight Flush or Straight:
            The hand with the highest card in the Straight.
            There's no need to account for the Royal Straight Flush because of this.
        Four of a Kind:
            The highest Four of a Kind, then the Kicker.
        Full House:
            The highest Three of a Kind, then the highest Pair.
        Flush:
            The hand with the highest card in the Flush wins.
        Three of a Kind:
            The highest Three of a Kind, then the highest Kicker.
        Two Pairs or Pair:
            The highest Pair, then the highest Kicker.
        High Card:
            The highest card in the hand.

    If still there is a tie, then it is a tie because all the Suits have the same weight.

    Attributes:
        hand (str): String representation of the poker hand.
        cards (List[PokerCard]): The list of poker cards in this hand.
    '''
    def __repr__(self):
        return self.hand

    def __init__(self, hand: str):
        self.hand = hand
        self.cards = [PokerCard(card) for card in hand.split(' ')]
        self.cards.sort()
        
    def __eq__(self, other: PokerHand):
        self_hand_weight = self.get_hand_weight()
        other_hand_weight = other.get_hand_weight()

        if self_hand_weight[0] != other_hand_weight[0]:
            return False
        
        for i in range(1, len(self_hand_weight)):
            if self_hand_weight[i] != other_hand_weight[i]:
                return False
        return True
    
    def __lt__(self, other: PokerHand):
        self_hand_weight = self.get_hand_weight()
        other_hand_weight = other.get_hand_weight()

        if self_hand_weight[0] < other_hand_weight[0]:
            return True
        
        # if both hands have teh same weight, the tie must be broken by highest ranking cards.
        if self_hand_weight[0] == other_hand_weight[0]:
            for i in range(1, len(self_hand_weight)):
                # if the rank is also equal, you want to check the next cards, if any are left
                if self_hand_weight[i] == other_hand_weight[i]:
                    continue
                if self_hand_weight[i] < other_hand_weight[i]:
                    return True
                return False
        # if it is a tie
        return False

    def get_hand_weight(self):
        '''Analize hand strenght.

        Returns:
            A Tuple containing the hand weight as its firs argument,
            then the cards ranks to break a tie in case the hand weight is the same.
        '''
        hand = defaultdict(int)
        for card in self.cards:
            hand[card.rank] += 1

        length = len(hand)
        # values holds the count for how many times each rank appears in the hand
        values = list(hand.values())

        # five different cards
        if length == 5:
            suited = self.is_suited()
            straight_high_card = self.is_a_straight()

            # if it is a straight flush:
            if suited and straight_high_card:
                return (1, straight_high_card)
            # if it is a flush:
            if suited:
                return (4, *self.cards)
            # if it is a straight:
            if straight_high_card:
                return (5, straight_high_card)
            # high card:
            return (9, *self.cards)

        if length == 2:
            # four of a kind:
            if 4 in values:
                i_four = values.index(4)
                i_kicker = values.index(1)
                return (2, self.cards[i_four], self.cards[i_kicker])

            # full house:
            i_triple = values.index(3)
            i_pair = values.index(2)
            return (3, self.cards[i_triple], self.cards[i_pair])

        if length == 3:
            # triple:
            if 3 in values:
                i_triple = values.index(3)
                return (6, self.cards[i_triple], *self.cards[:i_triple], *self.cards[i_triple+1:])

            # two pairs:
            i_pair = values.index(2)
            j_pair = values.index(2, i_pair+1)
            i_kicker = values.index(1)
            return (7, self.cards[i_pair], self.cards[j_pair], self.cards[i_kicker])

        if length == 4:
            # this is a pair:
            i_pair = values.index(2)
            return (8, self.cards[i_pair], *self.cards[:i_pair], *self.cards[i_pair+1:])

    def is_suited(self):
        '''Check if hand is Suited.'''
        for i in range(len(self.cards)-1):
            if self.cards[i].suit != self.cards[i+1].suit:
                return False

        return True
    
    def is_a_straight(self):
        '''Check if hand is a Straight
        
        Returns:
            The highest card in the Straight.
        '''
        starter = 0
        # if True, skips the first element to check for the Low Straight
        if self.cards[0].rank == 'A' and self.cards[1].rank == '5':
            starter = 1

        for i in range(starter, len(self.cards)-1):
            if self.cards[i+1] - self.cards[i] != 1:
                return False

        # in case it was a Low Straight, you want to return the 5 instead of the Ace
        if starter == 1:
            return self.cards[1]

        return self.cards[0]


class PokerCard(object):
    '''Representation of a poker card and its basic characteristics.

    The PokerCards Weight are:
        Ace:    1       |   7:      8
        King:   2       |   6:      9
        Queen:  3       |   5:      10
        Jack:   4       |   4:      11
        Ten:    5       |   3:      12
        9:      6       |   2:      13
        8:      7       |   Ace*:   When comparing it in a low Straight

    Attributes:
        card (str): String representation of the poker card.
        rank (str): The rank of the card.
        suit (str): The suit of the card.
    '''
    def __repr__(self):
        return self.get_card_weight()
    
    def __init__(self, card: str):
        self.card = card
        self.rank = card[0]
        self.suit = card[1]
    
    def __eq__(self, other: PokerCard):
        return True if self.get_card_weight() == other.get_card_weight() else False
    
    def __lt__(self, other: PokerCard):
        return True if self.get_card_weight() < other.get_card_weight() else False
    
    def __sub__(self, other: PokerCard):
        return self.get_card_weight() - other.get_card_weight()
    
    def get_card_weight(self):
        '''Return the card weight based on its rank.'''
        if self.rank == 'T':
            return 5
        if self.rank == 'J':
            return 4
        if self.rank == 'Q':
            return 3
        if self.rank == 'K':
            return 2
        if self.rank == 'A':
            return 1
        return (63 - ord(self.rank))
