# PPL Rules - Game State and Betting Variables

## Numeric Betting Variables

The following variables relate to betting actions, pot size, and amounts in the current hand:

-   **AmountToCall** – this is always expressed by number of big blinds, regardless of game type (Limit, NL, etc). It is the amount that the bot needs to put into the pot in order to call. It is 0 if the bot can check.
-   **Bets** – number of bets by opponents in this betting round. The bot's own bets are not counted. This variable is reset to 0 when flop, turn or river cards are dealt so that it represents the number of bets for the particular betting round only. The value can be either 0 or 1 since not more than 1 bet can be made in a particular betting round.
-   **BetSize** - this is always expressed by the number of big blinds, regardless of game type (Limit, NL, etc).
-   **BotsActionsOnThisRound** – the number of actions taken on the current betting round which involve putting chips in the pot (calling or raising). Checks are not counted as an action.
-   **Calls** – number of calls by opponents on this betting round. The bots' own calls are not counted. This variable is reset to 0 when flop, turn or river cards are dealt so that it represents the number of calls for the particular betting round only.
-   **CallsSinceLastRaise** – number of calls by all opponents since the last raise by an opponent on the current betting round. If there has not yet been a raise on the current betting round the value is 0. (The bot's own raise cannot be counted since it could never be the last raise.)
-   **Checks** – number of checks by opponents in this betting round. The bots' own checks are not counted. This variable is reset to 0 when flop, turn or river cards are dealt so that it represents the number of checks for the particular betting round only.
-   **Folds** – number of folds since the current betting round card(s) were dealt.
-   **PotSize** - this is always expressed by number of big blinds, regardless of game type (Limit, NL, etc).
-   **Raises** – number of raises by opponents on this betting round. The bots' own raises are not counted. This variable is reset to 0 when the flop, turn or river cards are dealt so that it represents the number of raises for the particular betting round only.
-   **RaisesSinceLastPlay** – The number of raises since bots' last action. Reset to 0 every time the bot beeps, checks, calls, bets, or raises and also when pre-flop, flop, turn, or river cards are dealt. This does not include the bots' own raises.
-   **TotalInvested** - the total amount of chips invested so far in the hand, counted by number of big blinds.

## Bot Action Variables

Variables tracking the bot's own actions:

-   **BotsLastAction** - whatever action the bot took last, good for handling raises after you act. This variable has its own special values which are: none, beep, raise, bet, call, or check. The only comparator allowed is '='.
-   **BotsLastPreflopAction** - whatever the bot's last action on the preflop betting round was. This variable uses the special BotsLastAction values which are: none, beep, raise, bet, call, or check. The only comparator allowed is '='. Restrictions: Post-flop only.

## Boolean Betting Variables

These variables evaluate to either true or false and relate to betting actions:

-   **BotCalledBeforeFlop** – True if the bot called before the flop. This can be used pre-flop also and will be true if the bot has already called.
-   **BotIsLastRaiser** – True if the bot has raised and there have been no raises after that.
-   **BotRaisedBeforeFlop** – True if the bot raised before the flop. This can be used pre-flop also and will be true if the bot has already raised.
-   **BotRaisedOnFlop** – True if the bot raised on the flop. Restrictions: Post-flop only.
-   **BotRaisedOnTurn** – True if the bot raised on the turn. Restrictions: Turn and River only.
-   **CalledOnFlop** – True if the bot called on the flop. Not true if the bot only checked, bet or raised on the flop. However this is true even if the bot bet or raised, was raised or re-raised and then called on the flop. Restrictions: Post-flop only.
-   **CalledOnTurn** – True if the bot called on the turn. Not true if the bot only checked, bet or raised on the turn. However this is true even if the bot bet or raised, was raised or re-raised and then called on the turn. Restrictions: River only.
-   **NoBettingOnFlop** – True if there was no betting on the flop. I.e. everybody checked on the flop. However note that as a special case only for Omaha Hi-Lo this is also true if the bot was in the last position on the flop, it was checked around to the bot, the bot bet and after that there were no raises. Restrictions: Turn and River only.
-   **NoBettingOnTurn** – True if there was no betting on the turn. I.e. everybody checked on the turn. However note that as a special case only for Omaha Hi-Lo this is also true if the bot was in the last position on the turn, it was checked around to the bot, the bot bet and after that there were no raises. Restrictions: River only.
-   **OpponentCalledOnFlop** – True if at least one opponent called on the flop and no opponent bet or raised. Restrictions: Turn and River only.
-   **OpponentCalledOnTurn** – True if at least one opponent called on the turn and no opponent bet or raised. Restrictions: River only.
-   **OpponentIsAllin** – True if any opponent has gone all-in at any point in the current hand, including the current betting round.
-   **RaisesBeforeFlop** – This is true if any opponent raised before the flop. Raises by the bot are not counted. If you want to check whether the bot raised before the flop use the variable BotRaisedBeforeFlop instead. Restrictions: Post-flop only.
-   **RaisesOnFlop** - True if any opponent raised on the flop. The bots' raises are not counted. Restrictions: Turn and River only.
-   **RaisesOnTurn** - True if any opponent raised on the turn. The bots' raises are not counted. Restrictions: River only.

## General Variables

-   **Random** – returns a random number between 1 and 100, inclusive. Used to easily code randomized actions. For example: when random <= 50 would be true 50% of the time on average.
-   **Others** – Always True 