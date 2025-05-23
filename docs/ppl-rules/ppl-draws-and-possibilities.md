# PPL Rules - Draws and Possibility Variables

## Straight Draw Variables

Variables for evaluating straight draws:

-   **HaveStraightDraw** - True if the bot has a made straight or a straight draw. A straight draw is defined as a hand with at least 7 'outs' to a straight. Cards that could complete a flush are counted as outs. Restrictions: Post-flop only.
-   **HaveInsideStraightDraw** - True if the bot has a made straight or an inside straight draw. An inside straight draw is defined as a hand with at least 4 'outs' to a straight. Note that this condition is also true when HaveStraightDraw is true Restrictions: Post-flop only.
-   **HaveNutStraightDraw** - True if the bot has a made nut straight or has a nut straight draw. A nut straight draw is defined as a hand with at least 7 'outs' to a nut straight. If a flush is not already possible then a card that will complete a nut straight but also make a flush possible is not counted as an 'out' to a nut straight. Restrictions: Post-flop only.
-   **HaveInsideNutStraightDraw** - True if the bot has an inside nut straight draw. An inside nut straight draw is defined as a hand with at least 4 'outs' to a nut straight. Unlike NutStraightDraw, outs that make a flush possible are not excluded. Note that this condition is also true when HaveNutStraightDraw is true. Restrictions: Post-flop only.

## Omaha Straight Draw Variables

Variables specific to Omaha straight draws:

-   **Have10OutStraightDraw** - True if the bot has a straight draw which has at least 10 outs to a straight. Can also be possible when the bot has a made straight already. Restrictions: Post-flop only. Can only be true in Omaha games.
-   **Have12OutStraightDraw** - True if the bot has a straight draw which has at least 12 outs to a straight. Can also be possible when the bot has a made straight already. Restrictions: Post-flop only. Can only be true in Omaha games.
-   **Have16OutStraightDraw** - True if the bot has a straight draw which has at least 16 outs to a straight. Can also be possible when the bot has a made straight already. Restrictions: Post-flop only. Can only be true in Omaha games.
-   **FourCardStraightInHand** - True if the bot has 4 cards in sequence in the hole. For example this variable is true if the hand is 5678. Restrictions: Can only be true in Omaha games.
-   **FourCardsWith1GapInHand** - True if the bot has 4 cards in sequence with 1 gap in the hole. For example this variable is true if the hand is 5689. Restrictions: Can only be true in Omaha games.
-   **ThreeCardStraightInHand** - True if the bot has three consecutive ranks in it's hole cards. Restrictions: Can only be true in Omaha games.
-   **ThreeCardsWith1gapInHand** - True if the bot has three cards in sequence with 1 gap in the hole. For example this variable is true if the hand is 568A. Restrictions: Can only be true in Omaha games.

## Flush Draw Variables

Variables for evaluating flush draws:

-   **HaveFlushDraw** - True if the bot has a made flush or a flush draw. Restrictions: Post-flop only.
-   **HaveNutFlushDraw** - True if the bot has a made nut flush or a nut flush draw. Restrictions: Post-flop only.
-   **Have2ndNutFlushDraw** - True if the bot has a made 2nd nut flush or a 2nd nut flush draw. Restrictions: Post-flop only.
-   **Have3rdNutFlushDraw** - True if the bot has a made 3rd nut flush or a 3rd nut flush draw. Restrictions: Post-flop only.
-   **Have4thNutFlushDraw** - True if the bot has a made 4th nut flush or a 4th nut flush draw. Restrictions: Post-flop only.
-   **Have5thNutFlushDraw** - True if the bot has a made 5th nut flush or a 5th nut flush draw. Restrictions: Post-flop only.

## Backdoor Draw Variables

Variables for backdoor draws (requiring two cards):

-   **HaveBackdoorFlushDraw** - True if the bot has a made flush or a flush draw or a backdoor flush draw. A backdoor flush draw is defined as a hand that has three cards of a particular suit so that getting two more cards of the same suit can complete the flush. Restrictions: Flop only.
-   **HaveBackdoorNutFlushDraw** - True if the bot has a made nut flush or a nut flush draw or a backdoor nut flush draw. A backdoor flush draw is defined as a hand that has three cards of a particular suit so that getting two more cards of the same suite can complete the flush. Restrictions: Flop only.
-   **HaveBackdoor2ndNutFlushDraw** - True if the bot has a made 2nd nut flush or a 2nd nut flush draw or a backdoor 2nd nut flush draw. A backdoor flush draw is defined as a hand that has three playable cards of a particular suit so that getting two more cards of the same suit can complete the flush. Restrictions: Flop only.
-   **HaveBackdoor3rdNutFlushDraw** - True if the bot has a made 3rd nut flush or a 3rd nut flush draw or a backdoor 3rd nut flush draw. A backdoor flush draw is defined as a hand that has three cards of a particular suit including the so that getting two more cards of the same suite can complete the flush. Restrictions: Flop only.

## Board Texture - Flush Possibilities

Variables describing flush possibilities on the board:

-   **FlushPossible** - True if a flush can be made with the current board cards. Restrictions: Post-flop only.
-   **FlushPossibleOnFlop** – True if a flush is/was possible on the flop. Restrictions: Post-flop only.
-   **FlushPossibleOnTurn** – True if a flush is/was possible on the turn. Restrictions: Turn and River only.
-   **FlushOnBoard** - True if all the board cards on the River are the same suit. Restrictions: River only.
-   **OneCardFlushPossible** - True if a flush can be made by using one hole card with the current board cards. Restrictions: Post-flop only.
-   **SuitsOnBoard** – The number of unique suits on board. For example if the board cards are Ac 8c 7c on the flop then this evaluates to 1 as there is only 1 suite (clubs) on board. Restrictions: Post-flop only.
-   **SuitsOnFlop** – The number of unique suits that were on board on the flop only. For example if the flop came Ac 8c 7c on the flop then this evaluates to 1 as there was only 1 suite (clubs) on board. Restrictions: Post-flop only.
-   **FourOf1SuitOnTurn** – True if only 1 suite is/was present on the board on the turn. Restrictions: Turn and River only.

## Board Texture - Straight Possibilities

Variables describing straight possibilities on the board:

-   **StraightPossible** - True if a straight can be made with the current board cards. Restrictions: Post-flop only.
-   **StraightPossibleOnFlop** – True if straight is/was possible on the flop. Restrictions: Post-flop only.
-   **StraightPossibleOnTurn** – True if straight is/was possible on the turn. Restrictions: Turn and River only.
-   **StraightOnBoard** - True if there is a straight on board. Restrictions: Post-flop only.
-   **OneCardStraightPossible** - True if a straight can be made by using one hole card with the current board cards. Restrictions: Post-flop only.
-   **OneCardStraightPossibleOnTurn** – True if a one card straight is/was possible on the turn. Restrictions: Turn and River only.
-   **OnlyOneStraightPossible** - True if one and only one straight can be made with the current board cards. For example if the board is AKQ then the only possible way to make a straight is with JT and so this variable will be true in this situation. However if the board is KQJ then the two ways to make a straight are with an AT or with a T9 so this variable will be false in this situation. Restrictions: Post-flop only.
-   **Only1OneCardStraightPossible** - True if one and only one straight can be made using only one hole card with the current board cards. For example if the board is 4578 then the only one-card straight possible is with a 6 so this variable will be true in this situation. However if the board is 4567 then there are two one-card straights possible and this variable will be false in this situation. Restrictions: Post-flop only.
-   **MoreThanOneStraightPossibleOnFlop** - True if there is/was more than one way to make a straight on the flop. Restrictions: Post-flop only.
-   **MoreThanOneStraightPossibleOnTurn** – True if there is/was more than one way to make a straight on the turn. Restrictions: Turn and River only.
-   **ThreeCardStraightOnBoard** - True if there are three consecutive ranks on the board. Restrictions: Post-flop only.

## Board Texture - Straight Flush Possibilities

Variables describing straight flush possibilities:

-   **StraightFlushPossible** - True if a straight-flush can be made with the current board cards. Restrictions: Post-flop only.
-   **StraightFlushPossibleByOthers** - True if a straight-flush can be made by an opponent with the current board cards given the bots hole cards. The bot may or may not have a straight flush and a straight flush may be possible with the current board cards but the bots' hole cards may rule out a straight flush for anybody else. For example if the board is Ac Kc Qc and the bot is holding Tc and 4c then the bot does not have a straight flush but nobody else can have a straight flush either because the bot holds Tc which is required to make a straight flush with the current board cards. This variable will evaluate to false while StraightFlushPossible will evaluate to true. Therefore the bots' nut flush hand cannot be beaten by a straight flush in this situation. Restrictions: Post-flop only.
-   **OneCardStraightFlushPossible** - True if a straight flush can be made by using one hole card with the current board cards. Restrictions: Post-flop only.

## Low Hand Variables (Omaha Hi-Lo)

Variables for low hand evaluation in split-pot games:

-   **LowPossible** - True if a low can be made with the current board cards. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **LowPossibleOnFlop** – True if a low is/was possible on the flop. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **LowPossibleOnTurn** – True if a low is/was possible on the turn. Restrictions: Omaha only, Turn and River only. Can only be true in Omaha/8 games.
-   **LowCardsInHand** – The number of unique low cards in your hand. An ace is counted as a low card and duplicates are not counted. For example in Omaha if our hand cards are AA39 this will evaluate to 2. For us to be able to make a low in Omaha Hi-Lo LowCardsInHand must be >= 2.
-   **LowCardsOnBoard** – The number of unique low cards on board. An ace is counted as a low card and duplicates are not counted. For example in Omaha/8 if the board on the turn is AA39 this will evaluate to 2. For a low to be possible in Omaha Hi-Lo LowCardsOnBoard must be >= 3. Restrictions: Post-flop only.

## Low Hand Strength Variables (Omaha Hi-Lo)

Variables for evaluating low hand strength:

-   **HaveLow** - True if the bot has a made low using the current board cards. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **HaveNutLow** - True if the bot has the best possible low using the current board cards. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **HaveNutLowWithBackup** - True if the bot has the best possible low using the current board cards with backup. A backup implies that the nut low cannot be counterfeited by a new board card. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **Have2ndNutLow** - True if the bot has the 2nd best possible low using the current board cards. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **Have3rdNutLow** - True if the bot has the 3rd best possible low using the current board cards. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **Have4thNutLow** - True if the bot has the 4th best possible low using the current board cards. Restrictions: Post-flop only. Can only be true in Omaha/8 games.

## Low Draw Variables (Omaha Hi-Lo)

Variables for low draws:

-   **HaveNutLowDraw** - True if the bot has the nut low draw. If a low is possible then this variable will be false. This variable is also false for made lows. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **HaveNutLowDrawWithBackup** - True if the bot has the nut low draw with backup. This variable will be false if a low is already possible. A backup implies that any non duplicate low card being dealt will cause the bot to have the nut low. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **HaveNutLowBackdoorDraw** - True if the bot has the nut low backdoor draw. This variable is true only if there is only 1 low card on board such that if two new low cards are dealt out (without counterfeiting the bots' low cards) then the bot will have the nut low on the river. Restrictions: Flop only. Can only be true in Omaha/8 games.
-   **Have2ndNutLowDraw** - True if the bot has the 2nd nut low draw. If a low is possible then this variable will be false. This variable is also false for made lows. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **Have3rdNutLowDraw** - True if the bot has the 3rd nut low draw. If a low is possible then this variable will be false. This variable is also false for made lows. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **Have4thNutLowDraw** - True if the bot has the 4th nut low draw. If a low is possible then this variable will be false. This variable is also false for made lows. Restrictions: Post-flop only. Can only be true in Omaha/8 games.

## Wheel Variables

Variables related to wheel (A2345) possibilities:

-   **WheelPossible** - True if a wheel can be made with the current board cards. A wheel is A2345. Restrictions: Post-flop only.
-   **FourCardsToWheelOnBoard** - True if a wheel can be made by using only one hole card. A wheel is A2345. Restrictions: Post-flop only. 