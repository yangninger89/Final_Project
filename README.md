# Blackjack Game Variant

## Team Member(s): 

**Nan Yang, Wei Zhong**

# Monte Carlo Simulation Scenario & Purpose:

- **Purpose**: use monte carlo to test whether the blackjack variant is profitable for casinos, according to real life blackjack strategy

- **Base Model**: single deck, single player, original blackjack rules

- **Updated Model**: add new rules to the original game, such
as paying initial fee for changing pay rate under the same color, having choice of bet under double down


## Simulation's Variables of Uncertainty:

- **Simulation Variable**: initial fees to play; pay rate under same color situation based on the initial fees

- **Distribution of Variable**: both variables follow uniform distribution [a, b]

## Different Strategy to Play the Game:

- **Advanced Strategy**: hit; stay; split; double down; all depending on the cards at hand

- **Dumb Strategy**: hit until 16

## Hypothesis or hypotheses before running the simulation:

- The variant version will bring more profit for casinos
- The advanced strategy will increase the difference of winning probability between dealer and player

## Analytical Summary of your findings: 

- Paying additional fees for a higher pay rate, even with a general fee of as small as 1 dollar, casino should be able 
to profit most of the time.

- With the advanced strategy, the House has an advantage of winning by around 5%; while using simple strategy seems to 
widen the gap to around 7%. Screenshots showing above result are also included in the repository.

## Files in the program:

- black_jack_strategy.csv: constructed based on the strategy chart downloaded from blackjackclassroom.com.
- black_jack_sim.py: user can simulate different scenarios by changing the boolean value of two indicator variable:
`is_simple_strategy` (line 374) and `fee_option` (line 375).

## All Sources Used:

- https://www.blackjackclassroom.com/blackjack-basic-strategy-charts
