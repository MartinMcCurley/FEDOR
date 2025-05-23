# PPL Rules - Board Texture Variables

## Board Pairing Variables

Variables describing pairs and higher made hands on the board:

-   **PairOnBoard** - True if there is a pair on board. This will also be true if there are two pair, trips, quads, or a full house on board. Restrictions: Post-flop only.
-   **PairOnFlop** – True if there is/was a pair on board on the flop. Restrictions: Post-flop only.
-   **PairOnTurn** – True if there is/was a pair on board on the turn. Restrictions: Turn and River only.
-   **TwoPairOnBoard** - True if there are two pair on board. This will also be true if there is a full house on board. Restrictions: Post-flop only.
-   **TripsOnBoard** - True if there is a three of a kind on board. This will also be true if there is a full house or quads on board. Restrictions: Post-flop only.
-   **TripsOnBoardOnTurn** – True if three of a kind is/was on board on the Turn. This will also be true if a full house or quads is/was on board on the Turn. Restrictions: Turn and River only.
-   **QuadsOnBoard** - True if there is a four of a kind on board. Restrictions: Post-flop only.
-   **FullHouseOnBoard** - True if there is a made full house on the board. Restrictions: Post-flop only.

## Board Card Changes

Variables tracking how the board changed between streets:

-   **RiverCardisOvercardToBoard** – True if the card that was dealt on the River was higher in rank than all the other board cards. Restrictions: River only.
-   **TurnCardisOvercardToBoard** – True if the card that was dealt on the Turn was higher in rank than all the other board cards. Restrictions: Turn and River only.
-   **TurnCardPaired** – True if the card that was dealt on the Turn was paired on the River. It must be the card that was dealt on the Turn – not true if any other card pairs on the River. Restrictions: River only.
-   **TopFlopCardPairedonTurn** - True if the highest ranking board card on the flop paired on the Turn. Restrictions: Turn and River only.
-   **TopFlopCardPairedonRiver** - True if the highest ranking board card on the flop paired on the River. Restrictions: River only.
-   **SecondTopFlopCardPairedonTurn** - True if the second-highest ranking board card on the flop paired on the Turn. Restrictions: Turn and River only.
-   **SecondTopFlopCardPairedonRiver** - True if the second-highest ranking board card on the flop paired on the River. Restrictions: River only.

## High Card Analysis

Variables analyzing high cards on the board:

-   **AcePresentOnFlop** - True if there is an ace present on board which was dealt on the flop. Restrictions: Post-flop only.
-   **KingPresentOnFlop** - True if there is a king present on board which was dealt on the flop. Restrictions: Post-flop only.
-   **QueenPresentOnFlop** - True if there is a queen present on board which was dealt on the flop. Restrictions: Post-flop only.

## Board Coordination

Variables describing how coordinated the board texture is:

-   **UncoordinatedFlop** – True if the flop contains/contained no pair on board, no possible flush, three different suits, no possible straight, and the ranks are such that no opponent could have 7 or more outs to a straight. Restrictions: Post-flop only.

## Stack and System Variables

Variables related to stack management and system state:

-   **StackSize** - the size of the bots' chip stack counted by number of big blinds. (If the stack size is ever unknown due to temporary obstructions or connection issues then any condition that uses this variable will evaluate to false.)
-   **StartingStackSize** - the size of the bots' chip stack (counted by number of current big blinds) the first time a particular bot window reads it's stack size in the current session. Clicking start and stop on our bots will not reset this variable even if you move to another game, so you should close the bot window and reopen when you change tables. This variable should only be used in cash game profiles as it does not account for the increasing big blind size in tournaments. Also note that when the bot first reads it's stack size it is usually after a blind has been posted so the number associated with this variable will likely always be one big blind short. This variable is primarily meant to be used in the % comparators to compare it to StackSize so you can create stop-loss points if you so desire.
-   **StackUnknown** - True if the bot cannot read its own stack size and therefore returns a "stack unknown" message in the bot window. Potentially useful for making sure the bot does not get involved with anything but strong hands when it is temporarily not reading everything properly.

## User-Defined Variables

Variables for custom logic and conditions:

-   **User[a-z_0-9]** – Set when a situation that is defined by the user is read in the code, with the action being that of setting a user-defined variable instead of taking a normal action. In this case the bot keeps reading code until a matching condition with a normal executable action is found (bet, raise, check, fold, beep, sitout, etc.). True when the condition that the user-variable defined earlier in the code is found true. Only letters, numbers, and underscores can be used in the variable name; however letters are not case-sensitive. Notes: All user defined variables are set to false when cards are dealt for a new hand. Once set to true they retain their value until cards are dealt for a new hand. Therefore variables set to true during early betting rounds can be used on later streets. Situations can be defined to set a user-variable the same way any other situation is defined, using any of the existing PPL variables (both numeric and Boolean). Once the user-variable is set it is used like any other Boolean variable. 