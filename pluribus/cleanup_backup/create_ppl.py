#!/usr/bin/env python3
"""Generate a properly formatted PPL file"""

ppl_content = """custom

preflop
when hand = AK suited and position = last raise 2 force
when hand = 22 and position = first fold force

flop
when hand = AK and havetoppair raisemax force

turn
when hand = AK and havetwopair raisemax force

river
when hand = AK fold force"""

with open('demo_strategy.ppl', 'w') as f:
    f.write(ppl_content)

print("Created properly formatted PPL file: demo_strategy.ppl") 