# PPL Rules Documentation Index

This documentation has been organized into focused modules for easier navigation and reference. Each module covers a specific aspect of the Poker Programming Language (PPL) variables.

## Overview

The PPL variables are used in conditions of the form `<variable> <comparator> <value>` for numeric variables, or simply `<variable>` for boolean variables. These variables provide comprehensive information about the game state, opponents, hand strength, and board texture.

## Documentation Modules

### Core Game Mechanics

1. **[Game State and Betting](ppl-gamestate-and-betting.md)**
   - Betting amounts and pot information
   - Bot action tracking
   - Betting round statistics
   - Random and utility variables

2. **[Opponent and Table Variables](ppl-opponent-and-table.md)**
   - Position variables and table dynamics
   - Opponent counting and identification
   - Stack size comparisons
   - Tournament-specific variables

### Hand and Board Analysis

3. **[Hand Strength and Evaluation](ppl-hand-strength.md)**
   - Made hand detection (pairs, trips, straights, etc.)
   - Nut hand evaluation
   - Kicker analysis
   - Historical hand strength tracking
   - Omaha-specific variables

4. **[Draws and Possibilities](ppl-draws-and-possibilities.md)**
   - Straight and flush draws
   - Backdoor possibilities
   - Board texture analysis
   - Low hand variables (Omaha Hi-Lo)
   - Wheel possibilities

5. **[Board Texture](ppl-board-texture.md)**
   - Board pairing and coordination
   - Card changes between streets
   - High card analysis
   - Stack and system variables
   - User-defined variables

### Street-Specific Analysis

6. **[Betting Round Specific Variables](ppl-betting-rounds.md)**
   - Pre-flop only variables
   - Post-flop restrictions
   - Street-specific betting patterns
   - Historical analysis by street
   - Backdoor variables (flop only)

## Usage Guidelines

### Variable Types

- **Numeric Variables**: Used with comparators (<, >, =, etc.)
  - Example: `Raises < 2`, `AmountToCall > 5`

- **Boolean Variables**: Evaluate to true/false
  - Example: `FlushPossible`, `HaveTopPair`

### Restrictions

Many variables have specific restrictions on when they can be used:
- **Pre-flop only**: Can only be used before the flop
- **Post-flop only**: Can only be used after the flop has been dealt
- **Turn and River only**: Can only be used on turn and river streets
- **Omaha only**: Specific to Omaha game variants
- **Tournament specific**: Related to tournament play mechanics

### Game Type Compatibility

- **Hold'em**: Most variables work in Hold'em games
- **Omaha**: Additional variables for 4-card hands and complex draws
- **Omaha Hi-Lo**: Special low hand and split-pot variables
- **Tournament vs Cash**: Some variables are tournament-specific

## Quick Reference

### Most Common Variables

**Betting & Game State:**
- `AmountToCall` - Amount needed to call
- `PotSize` - Current pot size in big blinds
- `Opponents` - Number of live opponents
- `Position` - Bot's position (first/middle/last)

**Hand Strength:**
- `HavePair`, `HaveTwoPair`, `HaveSet` - Basic hand strength
- `HaveTopPair`, `HaveOverPair` - Pair quality
- `HaveFlush`, `HaveStraight` - Made hands
- `HaveNuts` - Best possible hand

**Board Analysis:**
- `FlushPossible`, `StraightPossible` - Draw possibilities
- `PairOnBoard` - Board texture
- `Overcards` - Number of overcards to board

**Draws:**
- `HaveFlushDraw`, `HaveStraightDraw` - Drawing hands
- `HaveNutFlushDraw` - Premium draws

## Navigation Tips

1. **By Game Situation**: Start with the appropriate module based on what you're trying to analyze
2. **By Street**: Use the betting rounds module for street-specific logic
3. **By Hand Type**: Hand strength module for made hands, draws module for drawing hands
4. **By Game Variant**: Check Omaha-specific sections for 4-card games

## Additional Resources

- Each module includes detailed explanations and restrictions for every variable
- Variables are grouped logically within each module
- Cross-references are provided where variables relate to multiple categories

For comprehensive coverage of all PPL variables, refer to the individual module documents linked above. 