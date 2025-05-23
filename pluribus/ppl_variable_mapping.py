#!/usr/bin/env python3
"""
PPL Variable Mapping - Comprehensive mapping of all PPL variables
This ensures our AI training can understand and use all PPL concepts
"""

from typing import Dict, List, Any, Set
from dataclasses import dataclass

@dataclass
class PPLVariable:
    """Represents a PPL variable with its properties"""
    name: str
    type: str  # 'boolean' or 'numeric'
    category: str
    restrictions: List[str]
    description: str

class PPLVariableMapper:
    """Comprehensive mapping of all PPL variables for AI training"""
    
    def __init__(self):
        self.initialize_all_variables()
    
    def initialize_all_variables(self):
        """Initialize all PPL variables from documentation"""
        
        # All PPL variables organized by category
        self.variables = {
            
            # GAME STATE AND BETTING VARIABLES
            'betting_numeric': [
                PPLVariable('AmountToCall', 'numeric', 'betting', [], 'Amount needed to call in big blinds'),
                PPLVariable('Bets', 'numeric', 'betting', [], 'Number of bets by opponents this round'),
                PPLVariable('BetSize', 'numeric', 'betting', [], 'Current bet size in big blinds'),
                PPLVariable('BotsActionsOnThisRound', 'numeric', 'betting', [], 'Bot actions involving chips this round'),
                PPLVariable('Calls', 'numeric', 'betting', [], 'Number of calls by opponents this round'),
                PPLVariable('CallsSinceLastRaise', 'numeric', 'betting', [], 'Calls since last opponent raise'),
                PPLVariable('Checks', 'numeric', 'betting', [], 'Number of checks by opponents this round'),
                PPLVariable('Folds', 'numeric', 'betting', [], 'Number of folds this round'),
                PPLVariable('PotSize', 'numeric', 'betting', [], 'Current pot size in big blinds'),
                PPLVariable('Raises', 'numeric', 'betting', [], 'Number of raises by opponents this round'),
                PPLVariable('RaisesSinceLastPlay', 'numeric', 'betting', [], 'Raises since bot last action'),
                PPLVariable('TotalInvested', 'numeric', 'betting', [], 'Total chips invested this hand'),
                PPLVariable('Random', 'numeric', 'utility', [], 'Random number 1-100 for randomization'),
            ],
            
            'betting_boolean': [
                PPLVariable('BotCalledBeforeFlop', 'boolean', 'betting', [], 'True if bot called preflop'),
                PPLVariable('BotIsLastRaiser', 'boolean', 'betting', [], 'True if bot last to raise'),
                PPLVariable('BotRaisedBeforeFlop', 'boolean', 'betting', [], 'True if bot raised preflop'),
                PPLVariable('BotRaisedOnFlop', 'boolean', 'betting', ['post-flop'], 'True if bot raised on flop'),
                PPLVariable('CalledOnFlop', 'boolean', 'betting', ['post-flop'], 'True if bot called on flop'),
                PPLVariable('RaisesBeforeFlop', 'boolean', 'betting', ['post-flop'], 'True if any opponent raised preflop'),
                PPLVariable('RaisesOnFlop', 'boolean', 'betting', ['turn-river'], 'True if any opponent raised on flop'),
                PPLVariable('RaisesOnTurn', 'boolean', 'betting', ['river'], 'True if any opponent raised on turn'),
            ],
            
            # HAND STRENGTH VARIABLES
            'hand_strength_boolean': [
                PPLVariable('HaveFlush', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has made flush'),
                PPLVariable('HaveFullHouse', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has full house'),
                PPLVariable('HavePair', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has any pair'),
                PPLVariable('HaveQuads', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has four of a kind'),
                PPLVariable('HaveSet', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has three of a kind with pocket pair'),
                PPLVariable('HaveStraight', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has made straight'),
                PPLVariable('HaveStraightFlush', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has straight flush'),
                PPLVariable('HaveTrips', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has trips (pair on board)'),
                PPLVariable('HaveTwoPair', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has two pair'),
                
                # Pair types
                PPLVariable('HaveBottomPair', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has bottom pair'),
                PPLVariable('HaveTopPair', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has top pair'),
                PPLVariable('HaveOverPair', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has overpair'),
                PPLVariable('HaveUnderPair', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has underpair'),
                
                # Nut hands
                PPLVariable('HaveNuts', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has best possible hand'),
                PPLVariable('HaveNutFlush', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has nut flush'),
                PPLVariable('HaveNutStraight', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has nut straight'),
                PPLVariable('HaveNutStraightFlush', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has nut straight flush'),
                
                # Kickers
                PPLVariable('HaveBestKicker', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has best kicker'),
                PPLVariable('HaveBestKickerOrBetter', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has best kicker or better'),
                
                # Special evaluations
                PPLVariable('HaveNothing', 'boolean', 'hand_strength', ['post-flop'], 'True if bot has no made hand or draws'),
            ],
            
            'hand_strength_numeric': [
                PPLVariable('Overcards', 'numeric', 'hand_strength', ['post-flop'], 'Number of hole card overcards to board'),
                PPLVariable('OvercardsOnBoard', 'numeric', 'hand_strength', ['post-flop'], 'Number of board overcards to hole cards'),
                PPLVariable('NutFullHouseOrFourOfAKind', 'numeric', 'hand_strength', ['post-flop'], 'Nut ranking of full house/quads (1st, 2nd, etc.)'),
            ],
            
            # DRAW VARIABLES
            'draw_boolean': [
                PPLVariable('HaveFlushDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has flush draw'),
                PPLVariable('HaveNutFlushDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has nut flush draw'),
                PPLVariable('Have2ndNutFlushDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has 2nd nut flush draw'),
                PPLVariable('Have3rdNutFlushDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has 3rd nut flush draw'),
                PPLVariable('Have4thNutFlushDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has 4th nut flush draw'),
                PPLVariable('Have5thNutFlushDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has 5th nut flush draw'),
                
                PPLVariable('HaveStraightDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has straight draw (7+ outs)'),
                PPLVariable('HaveInsideStraightDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has inside straight draw (4+ outs)'),
                PPLVariable('HaveNutStraightDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has nut straight draw'),
                PPLVariable('HaveInsideNutStraightDraw', 'boolean', 'draws', ['post-flop'], 'True if bot has inside nut straight draw'),
                
                # Backdoor draws (flop only)
                PPLVariable('HaveBackdoorFlushDraw', 'boolean', 'draws', ['flop'], 'True if bot has backdoor flush draw'),
                PPLVariable('HaveBackdoorNutFlushDraw', 'boolean', 'draws', ['flop'], 'True if bot has backdoor nut flush draw'),
                PPLVariable('HaveBackdoor2ndNutFlushDraw', 'boolean', 'draws', ['flop'], 'True if bot has backdoor 2nd nut flush draw'),
                PPLVariable('HaveBackdoor3rdNutFlushDraw', 'boolean', 'draws', ['flop'], 'True if bot has backdoor 3rd nut flush draw'),
            ],
            
            # BOARD TEXTURE VARIABLES
            'board_texture_boolean': [
                PPLVariable('PairOnBoard', 'boolean', 'board_texture', ['post-flop'], 'True if pair on board'),
                PPLVariable('TwoPairOnBoard', 'boolean', 'board_texture', ['post-flop'], 'True if two pair on board'),
                PPLVariable('TripsOnBoard', 'boolean', 'board_texture', ['post-flop'], 'True if trips on board'),
                PPLVariable('QuadsOnBoard', 'boolean', 'board_texture', ['post-flop'], 'True if quads on board'),
                PPLVariable('FullHouseOnBoard', 'boolean', 'board_texture', ['post-flop'], 'True if full house on board'),
                
                PPLVariable('FlushPossible', 'boolean', 'board_texture', ['post-flop'], 'True if flush possible'),
                PPLVariable('StraightPossible', 'boolean', 'board_texture', ['post-flop'], 'True if straight possible'),
                PPLVariable('StraightFlushPossible', 'boolean', 'board_texture', ['post-flop'], 'True if straight flush possible'),
                PPLVariable('FlushOnBoard', 'boolean', 'board_texture', ['river'], 'True if flush on board'),
                PPLVariable('StraightOnBoard', 'boolean', 'board_texture', ['post-flop'], 'True if straight on board'),
                
                PPLVariable('OneCardFlushPossible', 'boolean', 'board_texture', ['post-flop'], 'True if one-card flush possible'),
                PPLVariable('OneCardStraightPossible', 'boolean', 'board_texture', ['post-flop'], 'True if one-card straight possible'),
                PPLVariable('OnlyOneStraightPossible', 'boolean', 'board_texture', ['post-flop'], 'True if only one straight possible'),
                
                PPLVariable('ThreeCardStraightOnBoard', 'boolean', 'board_texture', ['post-flop'], 'True if three-card straight on board'),
                PPLVariable('UncoordinatedFlop', 'boolean', 'board_texture', ['post-flop'], 'True if uncoordinated flop'),
            ],
            
            'board_texture_numeric': [
                PPLVariable('SuitsOnBoard', 'numeric', 'board_texture', ['post-flop'], 'Number of suits on board'),
                PPLVariable('SuitsOnFlop', 'numeric', 'board_texture', ['post-flop'], 'Number of suits on flop'),
            ],
            
            # OPPONENT AND TABLE VARIABLES
            'opponent_numeric': [
                PPLVariable('Opponents', 'numeric', 'opponents', [], 'Number of live opponents'),
                PPLVariable('OpponentsLeft', 'numeric', 'opponents', [], 'Same as Opponents'),
                PPLVariable('OpponentsAtTable', 'numeric', 'opponents', [], 'Total players at table'),
                PPLVariable('StillToAct', 'numeric', 'opponents', [], 'Players behind who haven\'t acted'),
                PPLVariable('MaxCurrentOpponentStackSize', 'numeric', 'opponents', [], 'Largest live opponent stack'),
                PPLVariable('MaxOpponentStackSize', 'numeric', 'opponents', [], 'Largest opponent stack at hand start'),
                PPLVariable('MinOpponentStackSize', 'numeric', 'opponents', [], 'Smallest opponent stack at hand start'),
                PPLVariable('OpponentsWithHigherStack', 'numeric', 'opponents', [], 'Opponents with larger stacks'),
                PPLVariable('OpponentsWithLowerStack', 'numeric', 'opponents', [], 'Opponents with smaller stacks'),
            ],
            
            # SYSTEM VARIABLES
            'system_numeric': [
                PPLVariable('StackSize', 'numeric', 'system', [], 'Bot stack size in big blinds'),
                PPLVariable('StartingStackSize', 'numeric', 'system', [], 'Bot starting stack size'),
            ],
            
            'system_boolean': [
                PPLVariable('StackUnknown', 'boolean', 'system', [], 'True if stack size cannot be read'),
            ],
        }
        
        # Actions mapping
        self.actions = {
            'fold': 'Fold current hand',
            'call': 'Call current bet',
            'check': 'Check (when no bet to call)',
            'bet': 'Make a bet',
            'raise': 'Raise current bet',
            'raise X': 'Raise to X big blinds',
            'raisemax': 'Raise maximum/all-in',
        }
        
        # Comparators for numeric variables
        self.comparators = ['<', '<=', '=', '>=', '>', '!=']
        
        # Boolean operators
        self.boolean_operators = ['and', 'or', 'not']
        
        # Position values
        self.position_values = ['first', 'middle', 'last']
        
        # Special action values
        self.action_values = ['none', 'beep', 'raise', 'bet', 'call', 'check']
    
    def get_all_variables(self) -> List[PPLVariable]:
        """Get all PPL variables as a flat list"""
        all_vars = []
        for category in self.variables.values():
            if isinstance(category, list):
                all_vars.extend(category)
        return all_vars
    
    def get_variables_by_category(self, category: str) -> List[PPLVariable]:
        """Get variables by category"""
        result = []
        for var_list in self.variables.values():
            for var in var_list:
                if var.category == category:
                    result.append(var)
        return result
    
    def get_variables_for_street(self, street: str) -> List[PPLVariable]:
        """Get variables available for a specific street"""
        available = []
        all_vars = self.get_all_variables()
        
        for var in all_vars:
            # Check restrictions
            if street == 'preflop':
                if 'post-flop' not in var.restrictions:
                    available.append(var)
            elif street in ['flop', 'turn', 'river']:
                if 'preflop-only' not in var.restrictions:
                    if street == 'flop':
                        if 'turn-river' not in var.restrictions:
                            available.append(var)
                    elif street == 'turn':
                        if 'river' not in var.restrictions and 'flop' not in var.restrictions:
                            available.append(var)
                    elif street == 'river':
                        if 'flop' not in var.restrictions and 'turn' not in var.restrictions:
                            available.append(var)
        
        return available
    
    def generate_variable_condition(self, var: PPLVariable, value: Any = None) -> str:
        """Generate a PPL condition string for a variable"""
        if var.type == 'boolean':
            return var.name.lower()
        elif var.type == 'numeric':
            if value is None:
                value = 5  # Default value
            comparator = '='
            return f"{var.name.lower()} {comparator} {value}"
        
        return var.name.lower()
    
    def validate_ppl_rule(self, rule: str) -> bool:
        """Validate a PPL rule for syntax and variable usage"""
        # Basic validation - could be expanded
        if not rule.startswith('when '):
            return False
        if ' force' not in rule:
            return False
        return True
    
    def get_training_context(self) -> Dict[str, Any]:
        """Get comprehensive context for AI training"""
        return {
            'total_variables': len(self.get_all_variables()),
            'categories': list(set(var.category for var in self.get_all_variables())),
            'variable_types': list(set(var.type for var in self.get_all_variables())),
            'actions': list(self.actions.keys()),
            'comparators': self.comparators,
            'boolean_operators': self.boolean_operators,
            'position_values': self.position_values,
            'preflop_variables': len(self.get_variables_for_street('preflop')),
            'flop_variables': len(self.get_variables_for_street('flop')),
            'turn_variables': len(self.get_variables_for_street('turn')),
            'river_variables': len(self.get_variables_for_street('river')),
        }

def main():
    """Demonstrate the PPL variable mapping"""
    print("🎯 PPL VARIABLE MAPPING SYSTEM")
    print("=" * 60)
    
    mapper = PPLVariableMapper()
    context = mapper.get_training_context()
    
    print(f"📊 PPL System Overview:")
    print(f"• Total Variables: {context['total_variables']}")
    print(f"• Categories: {len(context['categories'])}")
    print(f"• Variable Types: {context['variable_types']}")
    print(f"• Available Actions: {len(context['actions'])}")
    print(f"• Boolean Operators: {context['boolean_operators']}")
    
    print(f"\n🃏 Variables by Street:")
    print(f"• Preflop: {context['preflop_variables']} variables")
    print(f"• Flop: {context['flop_variables']} variables") 
    print(f"• Turn: {context['turn_variables']} variables")
    print(f"• River: {context['river_variables']} variables")
    
    print(f"\n📚 Categories Available:")
    for cat in context['categories']:
        vars_in_cat = len(mapper.get_variables_by_category(cat))
        print(f"• {cat.title()}: {vars_in_cat} variables")
    
    # Show some example variables
    print(f"\n🔍 Example Hand Strength Variables:")
    hand_vars = mapper.get_variables_by_category('hand_strength')[:5]
    for var in hand_vars:
        condition = mapper.generate_variable_condition(var)
        print(f"• {condition}")
    
    print(f"\n✅ PPL mapping system ready for AI training integration!")

if __name__ == "__main__":
    main() 