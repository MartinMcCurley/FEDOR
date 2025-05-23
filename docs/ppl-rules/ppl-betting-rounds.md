# PPL Rules - Betting Round Specific Variables

## Pre-flop Specific Variables

Variables that can only be used or are specifically designed for pre-flop play:

-   **FirstCallerPosition** – The position of the first preflop caller on the first round of betting when it is your turn to first act. Restrictions: First action preflop only.
-   **FirstRaiserPosition** – Identifies the position of a raiser on the first preflop round. Restrictions: First action preflop only.
-   **LastCallerPosition** – The position of the last preflop caller on the first round of betting when it is your turn to first act. Restrictions: First action preflop only.
-   **LastRaiserPosition** – Identifies the position of the last raiser on the first preflop round. Restrictions: First action preflop only.

## Post-flop Only Variables

Variables that can only be used after the flop has been dealt:

-   **BotsLastPreflopAction** - whatever the bot's last action on the preflop betting round was. Restrictions: Post-flop only.
-   **NumberOfRaisesBeforeFlop** – The number of preflop raises made by opponents. The bot's own raises are not counted. Restrictions: Post-flop only.
-   **BotsActionsPreflop** – the number of actions taken on the preflop betting round which involve putting chips in the pot (calling or raising). Checks are not counted as an action. Restrictions: Post-flop only.
-   **RaisesBeforeFlop** – This is true if any opponent raised before the flop. Restrictions: Post-flop only.

## Flop Specific Variables

Variables related to flop betting and analysis:

-   **BotsActionsOnFlop** – the number of actions taken on the flop betting round which involve putting chips in the pot (calling or raising). Checks are not counted as an action. Restrictions: Turn and River only.
-   **CalledOnFlop** – True if the bot called on the flop. Restrictions: Post-flop only.
-   **BotRaisedOnFlop** – True if the bot raised on the flop. Restrictions: Post-flop only.
-   **NumberOfRaisesOnFlop** – The number of raises on the flop betting round made by opponents. Restrictions: Turn and River only.
-   **OpponentCalledOnFlop** – True if at least one opponent called on the flop and no opponent bet or raised. Restrictions: Turn and River only.
-   **RaisesOnFlop** - True if any opponent raised on the flop. Restrictions: Turn and River only.
-   **NoBettingOnFlop** – True if there was no betting on the flop. Restrictions: Turn and River only.

## Turn Specific Variables

Variables related to turn betting and analysis:

-   **CalledOnTurn** – True if the bot called on the turn. Restrictions: River only.
-   **BotRaisedOnTurn** – True if the bot raised on the turn. Restrictions: Turn and River only.
-   **NumberOfRaisesOnTurn** – The number of raises on the Turn betting round made by opponents. Restrictions: River only.
-   **OpponentCalledOnTurn** – True if at least one opponent called on the turn and no opponent bet or raised. Restrictions: River only.
-   **RaisesOnTurn** - True if any opponent raised on the turn. Restrictions: River only.
-   **NoBettingOnTurn** – True if there was no betting on the turn. Restrictions: River only.

## Historical Hand Strength by Street

Variables tracking hand strength on specific previous streets:

### Flop History (Turn and River only)

-   **HadPairOnFlop** - True if the bot had any pair on the Flop, including a pocket pair. Restrictions: Turn and River only.
-   **HadTopPairOnFlop** - True if the bot had top pair on the flop. Restrictions: Turn and River only.
-   **HadTwoPairOnFlop** - True if the bot had two pair on the flop. Restrictions: Turn and River only.
-   **HadOverpairOnFlop** - True if the bot had any overpair on the flop. Restrictions: Turn and River only.
-   **FlushPossibleOnFlop** – True if a flush is/was possible on the flop. Restrictions: Post-flop only.
-   **StraightPossibleOnFlop** – True if straight is/was possible on the flop. Restrictions: Post-flop only.
-   **LowPossibleOnFlop** – True if a low is/was possible on the flop. Restrictions: Post-flop only. Can only be true in Omaha/8 games.
-   **PairOnFlop** – True if there is/was a pair on board on the flop. Restrictions: Post-flop only.
-   **MoreThanOneStraightPossibleOnFlop** - True if there is/was more than one way to make a straight on the flop. Restrictions: Post-flop only.
-   **AcePresentOnFlop** - True if there is an ace present on board which was dealt on the flop. Restrictions: Post-flop only.
-   **KingPresentOnFlop** - True if there is a king present on board which was dealt on the flop. Restrictions: Post-flop only.
-   **QueenPresentOnFlop** - True if there is a queen present on board which was dealt on the flop. Restrictions: Post-flop only.

### Turn History (River only)

-   **HadPairOnTurn** - True if the bot had any pair on the Turn, including a pocket pair. Restrictions: River only.
-   **HadTopPairOnTurn** - True if the bot had top pair on the Turn. Restrictions: River only.
-   **FlushPossibleOnTurn** – True if a flush is/was possible on the turn. Restrictions: Turn and River only.
-   **StraightPossibleOnTurn** – True if straight is/was possible on the turn. Restrictions: Turn and River only.
-   **LowPossibleOnTurn** – True if a low is/was possible on the turn. Restrictions: Turn and River only. Can only be true in Omaha/8 games.
-   **PairOnTurn** – True if there is/was a pair on board on the turn. Restrictions: Turn and River only.
-   **MoreThanOneStraightPossibleOnTurn** – True if there is/was more than one way to make a straight on the turn. Restrictions: Turn and River only.
-   **OneCardStraightPossibleOnTurn** – True if a one card straight is/was possible on the turn. Restrictions: Turn and River only.
-   **TripsOnBoardOnTurn** – True if three of a kind is/was on board on the Turn. Restrictions: Turn and River only.
-   **FourOf1SuitOnTurn** – True if only 1 suite is/was present on the board on the turn. Restrictions: Turn and River only.

## Board Card Pairing Between Streets

Variables tracking specific board card pairing events:

-   **TopFlopCardPairedonTurn** - True if the highest ranking board card on the flop paired on the Turn. Restrictions: Turn and River only.
-   **TopFlopCardPairedonRiver** - True if the highest ranking board card on the flop paired on the River. Restrictions: River only.
-   **SecondTopFlopCardPairedonTurn** - True if the second-highest ranking board card on the flop paired on the Turn. Restrictions: Turn and River only.
-   **SecondTopFlopCardPairedonRiver** - True if the second-highest ranking board card on the flop paired on the River. Restrictions: River only.
-   **TurnCardPaired** – True if the card that was dealt on the Turn was paired on the River. Restrictions: River only.

## River Specific Variables

Variables that can only be used on the river:

-   **RiverCardisOvercardToBoard** – True if the card that was dealt on the River was higher in rank than all the other board cards. Restrictions: River only.
-   **FlushOnBoard** - True if all the board cards on the River are the same suit. Restrictions: River only.

## Opponent Count by Street

Variables tracking opponent counts on specific streets:

-   **OpponentsOnFlop** – the number of live opponents still in the hand at the beginning of the flop, before there was any betting action on the flop. Restrictions: Turn and River only.

## Backdoor Variables (Flop Only)

Variables for backdoor draws that can only be evaluated on the flop:

-   **HaveBackdoorFlushDraw** - True if the bot has a made flush or a flush draw or a backdoor flush draw. Restrictions: Flop only.
-   **HaveBackdoorNutFlushDraw** - True if the bot has a made nut flush or a nut flush draw or a backdoor nut flush draw. Restrictions: Flop only.
-   **HaveBackdoor2ndNutFlushDraw** - True if the bot has a made 2nd nut flush or a 2nd nut flush draw or a backdoor 2nd nut flush draw. Restrictions: Flop only.
-   **HaveBackdoor3rdNutFlushDraw** - True if the bot has a made 3rd nut flush or a 3rd nut flush draw or a backdoor 3rd nut flush draw. Restrictions: Flop only.
-   **HaveNutLowBackdoorDraw** - True if the bot has the nut low backdoor draw. Restrictions: Flop only. Can only be true in Omaha/8 games.

## Specific Hand Strength by Street

Variables for specific hand strength evaluations that depend on which street:

-   **Have4thTopSet** - True if the bot has a hole pair that has the same value as the 4th highest board card. Restrictions: Turn and River only.

## Suits by Street

Variables tracking suit information by specific streets:

-   **SuitsOnFlop** – The number of unique suits that were on board on the flop only. Restrictions: Post-flop only. 