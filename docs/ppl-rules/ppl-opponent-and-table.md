# PPL Rules - Opponent and Table Variables

## Position Variables

Variables related to position and table dynamics:

-   **FirstCallerPosition** – The position of the players at the table is counted from a counter-clockwise position relative to the big blind position (not your position). Therefore the small blind = 1, the button = 2, the cutoff (next to the button) = 3, etc. This variable tells you the position of the first preflop caller on the first round of betting when it is your turn to first act. It goes to 0 after the action passes and is therefore useless when the action comes back after a raise behind you. It is most useful when there has only been one caller and you are in the blinds or are in late position and want to know which position the call came from. Restrictions: First action preflop only.
-   **FirstRaiserPosition** – Works the same as FirstCallerPosition above except for identifying the position of a raiser (if any). Especially useful when there has been only one raise and you are in the blinds or are in late position and want to know which position it came from. Restrictions: First action preflop only.
-   **LastCallerPosition** – The position of the players at the table is counted from a counter-clockwise position relative to the big blind position (not your position). Therefore the small blind = 1, the button = 2, the cutoff (next to the button) = 3, etc. This variable tells you the position of the last preflop caller on the first round of betting when it is your turn to first act. It goes to 0 after the action passes and is therefore useless when the action comes back after a raise behind you. It is most useful when there has only been one caller and you are in the blinds or are in late position and want to know which position the call came from. Restrictions: First action preflop only.
-   **LastRaiserPosition** – Works the same as LastCallerPosition above except for identifying the position of a raiser (if any). Especially useful when there has been only one raise and you are in the blinds or are in late position and want to know which position it came from. Restrictions: First action preflop only.
-   **Position** - The bots' position relative to the other players. This variable has its own special values which are: first, middle, or last. The only comparator allowed is '='. Your position is always read in real time whenever it is your turn to act. For example if you are in middle position on the flop and the first opponent bets, you call, the last opponent raises, the original bettor now folds and it is back to you, now opponents = 1 and position = first will be true for the action you are facing. This variable is intended for post-flop use or second orbit situations pre-flop (when there was a raise behind you and the action has come back). For first orbit situations on the pre-flop betting round, use stilltoact = instead.
-   **StillToAct** - only the live players behind you who have not acted yet; does not include calls and raises in front of you. Only valid on the first orbit (that is, the first time the betting goes around) for the betting round. Therefore if somebody raises behind you and the betting comes back to you, stilltoact will always = 0.

## Opponent Count Variables

Variables tracking the number of opponents:

-   **Opponents** – the number of all live opponents, or everyone who has not yet folded (or has gone all-in on a prior betting round). This includes calls and raises in front of you as well. All-in players on a prior betting round are not counted.
-   **OpponentsAtTable** - only the starting number of players currently sitting in, useful for late stages of tournaments.
-   **OpponentsLeft** - same exact variable as 'opponents' above but describes it a little better (use either).
-   **OpponentsOnFlop** – the number of live opponents still in the hand at the beginning of the flop, before there was any betting action on the flop. Restrictions: Turn and River only.

## Stack Size Comparison Variables

Variables for comparing stack sizes with opponents:

-   **MaxCurrentOpponentStackSize** – The number of big blinds that the live opponent (who is still in the hand and not yet folded) with the largest current stack has in his stack at the moment when it is the bot's turn to act. Can be used on the left of the % comparators to compare to your own stack size and is useful for identifying short-stacked opponents or determining that all the live opponents have your stack covered. Can be used preflop or post-flop.
-   **MaxOpponentStackSize** – The number of big blinds that the opponent at your table with the largest stack has in his stack at the beginning of the hand (before blinds are posted). The value is always 0 if you are playing at a poker room or game which does not support this feature. Can be used preflop or post-flop.
-   **MinOpponentStackSize** – The number of big blinds that the opponent at your table with the smallest stack has in his stack at the beginning of the hand (before blinds are posted). The value is always 0 if you are playing at a poker room or game which does not support this feature. Can be used preflop or post-flop.
-   **MaxStillToActStackSize** – The number of big blinds that the opponent with the largest stack who has not acted yet had in their stack at the beginning of the hand (before blinds were posted). Only valid on the first orbit (that is, the first time the betting goes around) for the betting round, otherwise the value is 0. Therefore it only applies to opponents behind you on the first orbit and is really only accurate preflop. Can be used to steal blinds from short-stacked opponents in tournament situations. Can be used on the left of the % comparators.
-   **MinStillToActStackSize** – The number of big blinds that the opponent with the lowest stack who has not acted yet had in their stack at the beginning of the hand (before blinds were posted). Only valid on the first orbit (that is, the first time the betting goes around) for the betting round, otherwise the value is 0. Therefore it only applies to opponents behind you on the first orbit and is really only accurate preflop. Can be used to identify large stacks in the blinds in tournament situations and stop normal steal-raises. Restrictions: Only valid on the first orbit of a betting round.
-   **OpponentsWithHigherStack** – the number of opponents at the table with a larger stack than the bot's at the beginning of the hand (before blinds are posted). Equal stack sizes are not considered higher. The value is always 0 if you are playing at a poker room or game which does not support this feature. Can be used preflop or post-flop.
-   **OpponentsWithLowerStack** – the number of opponents at the table with a smaller stack than the bot's at the beginning of the hand (before blinds are posted). Equal stack sizes are not considered lower. The value is always 0 if you are playing at a poker room or game which does not support this feature. Can be used preflop or post-flop.

## Opponent Identification Variables

Variables for identifying specific opponents:

-   **Opponent** = - opponent screen names who still have cards in front of them on the current hand. This variable accepts user-created custom values which can consist of any combination of upper and lower case letters, numbers, dashes, and underscores. Only the equal sign can follow the word opponent. Use it to identify certain opponents whom you know, or whom you have stats on, and want to adjust your play for. You can group together large lists of opponent names separated by the 'or' operator inside of brackets. You can also set user-defined variables from those lists. This variable can be defined and used on any betting round. Restrictions: WPN Rooms only as of Dec 2016.

## Tournament and Table State Variables

Variables specific to tournament play and table conditions:

-   **BigBlindSize** - the size of the big blind expressed by betting units starting from 1, meant for tournaments.
-   **IsFinalTable** - True if the bot is playing at the Final Table at an MTT, which has a different appearance than the other tables. Our bot software recognizes this and has no problem playing at the final table; however you may want to program different instructions for it by using this variable. Restrictions: Not available at any currently supported poker rooms as of 10-15-2010. 