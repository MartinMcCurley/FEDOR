# PPL Rules - Hand Strength and Evaluation Variables

## Made Hand Variables

Variables for evaluating made hands:

-   **HaveFlush** - True if the bot has a made flush. For Holdem a flush on board does count as a made flush. Restrictions: Post-flop only.
-   **HaveFullHouse** - True if the bot has a made full house. Any playable full house, can consist of only one card in the case of two pair on board or play the board on the river if a full house in on board. Restrictions: Post-flop only.
-   **HavePair** - True if the bot has a pair. This could be a pair in hand or one of the hand cards paired with at least one of the cards on board. A pair on board does not count. Restrictions: Post-flop only.
-   **HaveQuads** - True if the bot has a made four of a kind. Four of a kind on board does not count. Restrictions: Post-flop only.
-   **HaveSet** - True if the bot has a hole pair that has the same value as one of the board cards. Restrictions: Post-flop only.
-   **HaveStraight** - True if the bot has any made straight. Restrictions: Post-flop only.
-   **HaveStraightFlush** - True if the bot has a made straight flush. For Holdem a straight flush on board does count as a made straight flush. Restrictions: Post-flop only.
-   **HaveTrips** - True if there is a pair on board and the bot has a hole card of the same value as the board pair. Three of a kind on board does not count as having trips. Restrictions: Post-flop only.
-   **HaveTwoPair** - True if the bot has two pair. A pair on board does not count as one of the pairs. Restrictions: Post-flop only.

## Pair Type Variables

Variables for specific pair types:

-   **HaveBottomPair** - True if the bot has a hole card that is the same value as the lowest card on board. Ace is highest. Restrictions: Post-flop only.
-   **HaveBottomSet** - True if the bot has a hole pair that has the same value as the lowest board card. Ace is highest. Restrictions: Post-flop only.
-   **HaveBottomTwoPair** - True if the two lowest valued board cards are present in the hole for the bot. A pair on board does not count as one of the pairs. Ace is highest. Restrictions: Post-flop only.
-   **HaveOverPair** - True if the bot has a hole pair that is higher in value than any card on board. Ace is highest. Restrictions: Post-flop only.
-   **HaveTopNonBoardPairedPair** - True if the bot has a hole card that is the same value as the highest non-paired card on board. Ace is highest. This was designed to identify the strength of two-pair hands when a pair is on board. (Please note that HaveTwoPair in PPL cannot include a board pair however). Restrictions: Post-flop only.
-   **HaveTopPair** - True if the bot has a hole card that is the same value as the highest card on board. Ace is highest. This could include a paired board card and would therefore be true if you have top trips as well. Restrictions: Post-flop only.
-   **HaveTopSet** - True if the bot has a hole pair that has the same value as the highest board card. Ace is highest. Restrictions: Post-flop only.
-   **HaveTopTwoPair** - True if the two highest valued board cards are present in the hole for the bot. A pair on board does not count as one of the pairs. Ace is highest. Restrictions: Post-flop only.
-   **HaveUnderPair** - True if the bot has a hole pair (and the highest hole pair) is lower in value than the lowest card on board. Ace is highest. Restrictions: Post-flop only.
-   **HaveUnderStraight** - True if the bot has a straight such that all hand cards used to make the straight are lower in value than any board cards used to make the straight. Restrictions: Post-flop only.

## Numbered Pair Variables

Variables for ranking pairs:

-   **Have2ndOverPair** - True if the bot has a hole pair which is between the highest board card and the 2nd highest card rank on board and therefore is not technically an overpair to the board. Ace is highest. Pairs on board are only counted as one rank. Restrictions: Post-flop only.
-   **Have2ndTopPair** - True if the bot has a hole card that is the same value as the 2nd highest card on board. Ace is highest. Restrictions: Post-flop only.
-   **Have2ndTopSet** - True if the bot has a hole pair that has the same value as the 2nd highest board card. Ace is highest. Restrictions: Post-flop only.
-   **Have3rdOverPair** - True if the bot has a hole pair which is between the 2nd highest and 3rd highest card rank on board and therefore is not technically an overpair to the board. Ace is highest. Pairs on board are only counted as one rank. Restrictions: Post-flop only.
-   **Have3rdTopPair** - True if the bot has a hole card that is the same value as the 3rd highest card on board. Ace is highest. Restrictions: Post-flop only.
-   **Have3rdTopSet** - True if the bot has a hole pair that has the same value as the 3rd highest board card. Ace is highest. Restrictions: Post-flop only.
-   **Have4thOverPair** - True if the bot has a hole pair which is between the 3rd highest and 4th highest card rank on board and therefore is not technically an overpair to the board. Ace is highest. Pairs on board are only counted as one rank. Restrictions: Post-flop only.
-   **Have4thTopPair** - True if the bot has a hole card that is the same value as the 4th highest card on board. Ace is highest. Restrictions: Post-flop only.
-   **Have4thTopSet** - True if the bot has a hole pair that has the same value as the 4th highest board card. Ace is highest. Restrictions: Turn and River only.
-   **Have5thOverPair** - True if the bot has a hole pair which is between the 4th highest and 5th highest card rank on board, so is not technically an overpair to the board. Ace is highest. Pairs on board are only counted as one rank. Restrictions: Postflop only.

## Nut Hand Variables

Variables for evaluating nut hands:

-   **HaveNuts** - True if the bot has the best possible hand at the moment. This variable does not apply to low hands in Omaha Hi-Lo, only the best possible high hand. Restrictions: Post-flop only.
-   **HaveNutStraight** - True if the bot has the best possible straight using the current board cards. Note that this may not be the nut hand if a flush or a full house is possible. Restrictions: Post-flop only.
-   **HaveNutStraightFlush** - True if the bot has a made straight flush and it is not possible for an opponent to have a higher straight flush. For Holdem a royal straight flush on board does count as a made nut straight flush. Restrictions: Post-flop only.
-   **NutFullHouseOrFourOfAKind** – This is 0 if we don't have a full house or four of a kind. Otherwise it returns a number indicating whether our hand is the 1st nut, 2nd nut and so on. If we have the 1st nut full house or four of a kind this returns 1. If we have the 2nd nut full house or 4 of a kind it returns 2 and so on. It does not take straight flushes into account. So it could return 1 even if our hand can be beaten by a straight flush. Restrictions: Post-flop only.

## Flush Variables

Variables for flush evaluation:

-   **HaveNutFlush** - True if the bot has the highest possible flush with the current board cards. For Holdem a royal straight flush on board does count as a made nut flush. Note that nut flushes could be beaten by full houses, four of a kind and straight flushes. Restrictions: Post-flop only.
-   **HaveNutFlushCard** - True if a flush is possible based on the current board cards and one of the bot's hole cards is the card required for a nut flush. The bot may not have a made flush but since it is holding the nut flush card nobody else can have the nut flush either. Restrictions: Post-flop only.
-   **Have2ndNutFlush** - True if the bot has the 2nd highest possible flush with the current board cards. Note that 2nd nut flushes could be beaten by a higher flush, full houses, four of a kind and straight flushes. Restrictions: Post-flop only.
-   **Have3rdNutFlush** - True if the bot has the 3rd highest possible flush with the current board cards. Note that 3rd nut flushes could be beaten by a higher flush, full houses, four of a kind and straight flushes. Restrictions: Post-flop only.
-   **Have4thNutFlush** - True if the bot has the 4th highest possible flush with the current board cards. Note that 4th nut flushes could be beaten by a higher flush, full houses, four of a kind and straight flushes. Restrictions: Post-flop only.
-   **Have5thNutFlush** - True if the bot has the 5th highest possible flush with the current board cards. Note that 5th nut flushes could be beaten by a higher flush, full houses, four of a kind and straight flushes. Restrictions: Post-flop only.

## Kicker Variables

Variables for kicker evaluation:

-   **HaveBestKicker** - True if the bot has the best kicker with the current board cards. Best kicker is defined as the highest valued card not currently present on the board. Ace is highest. Restrictions: Post-flop only.
-   **HaveBestKickerOrBetter** - True if the bot has a made hand which is best kicker or better given the current board cards. Note that the "or better" part of this variable refers to any higher hand rank, including a pair, set, straight, full house, etc. Restrictions: Post-flop only.
-   **Have2ndBestKicker** - True if the bot has the 2nd best kicker or the best kicker with the current board cards (to clarify, this variable is also true when havebestkicker is true). The 2nd best kicker is defined as the 2nd highest valued card not currently present on the board. Restrictions: Post-flop only.
-   **Have2ndBestKickerOrBetter** - True if the bot has a made hand which is 2nd best kicker or better given the current board cards. The "or better" part refers to any better hand values such as a pair, two pair, etc and not just a better kicker. Restrictions: Post-flop only.
-   **Have3rdBestKicker** - True if the bot has the 3rd best kicker, the 2nd best kicker, or the best kicker with the current board cards. The 3rd best kicker is defined as the 3rd highest valued card not currently present on the board. Restrictions: Post-flop only.
-   **Have3rdBestKickerOrBetter** - True if the bot has a made hand which is 3rd best kicker or better given the current board cards. The "or better" part refers to any better hand values such as a pair, two pair, etc and not just a better kicker. Restrictions: Post-flop only.

## Overpair Ranking Variables

Variables for ranking overpairs:

-   **HaveBestOverpairOrBetter** - True if the bot has a made hand which is best overpair or better given the current board cards. Best overpair is AA with no A on board. Note that the "or better" part of this variable refers to any higher hand rank. Restrictions: Post-flop only.
-   **Have2ndBestOverpairOrBetter** - True if the bot has a made hand which is 2nd best overpair or better given the current board cards. 2nd best overpair is KK with no A or K on board. Restrictions: Post-flop only.
-   **Have3rdBestOverpairOrBetter** - True if the bot has a made hand which is 3rd best overpair or better given the current board cards. 3rd best overpair is QQ with no A, K or Q on board. Restrictions: Post-flop only.

## Historical Hand Strength Variables

Variables tracking hand strength on previous streets:

-   **HadPairOnFlop** - True if the bot had any pair on the Flop, including a pocket pair. Restrictions: Turn and River only.
-   **HadPairOnTurn** - True if the bot had any pair on the Turn, including a pocket pair. Restrictions: River only.
-   **HadTopPairOnFlop** - True if the bot had top pair on the flop. Restrictions: Turn and River only.
-   **HadTopPairOnTurn** - True if the bot had top pair on the Turn. Restrictions: River only.
-   **HadTwoPairOnFlop** - True if the bot had two pair on the flop. Restrictions: Turn and River only.
-   **HadOverpairOnFlop** - True if the bot had any overpair on the flop. An overpair is defined as a pocket pair higher than all the board cards. Restrictions: Turn and River only.

## Special Hand Evaluation Variables

-   **HaveNothing** - True if the bot has no pair, no trips, no straight, no straight draw, no inside straight draw, no flush, no flush draw, no backdoor flush draw; and if overcards = 2 is also false. This variable only applies to high hands in Omaha Hi-Lo and disregards made low hands or low draws, so should not be used in Omaha Hi-Lo. Restrictions: Post-flop only.
-   **Overcards** – The number of hole cards that are Overcards to the board (not vice-versa). Restrictions: Post-flop only.
-   **OvercardsOnBoard** – The number of Board cards that are Overcards to the hole cards. Please note that this includes paired board cards so is not necessarily just the number of higher ranks. Restrictions: Post-flop only.

## Omaha-Specific Variables

Variables specific to Omaha games:

-   **PairInHand** - True if the bot has a hole pair. Also true if the bot has two pair, trips, or quads in the hole.
-   **TripsInHand** - True if the bot has trips in the hole. Restrictions: Can only be true in Omaha games.
-   **TwoPairInHand** - True if the bot has two pair in the hole. Restrictions: Can only be true in Omaha games.
-   **SuitsInHand** – The number of unique suits in your hole cards. This variable was primarily designed for our Omaha bot profiles. For example if your hole cards are Ad 3d 8d Js then this evaluates to 2 as you have only two suits in your hand (diamonds and spades).
-   **DoubleSuited** – This variable is no longer working. Instead, to state that a pocket pair is double-suited use hand = K suited K suited, hand = Q suited Q suited, etc., which we have verified is working as desired. Please note that suitsinhand = 2 is also true when you have three of 1 suit and 2 of another. Restrictions: Omaha Bots only. 