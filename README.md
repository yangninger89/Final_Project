Create a FORK of this repository to store your code, data, and documentation for the final project. Detailed instructions for this assignment are in the course Moodle site.  The reason I'm asking you to fork this empty repository instead of creating a stand-alone repository is that it will be much easier for me and all students in the course to find all of our projects for code review and for grading. You can even get code review from students in the other section of IS590PR this way.

Even though your fork of this repository shall be public, you'll still need to explicitly add any students on your team as Collaborators in the Settings. That way you can grant them write privileges.

DELETE these lines from TEMPLATE up.

TEMPLATE for your report:

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

- Paying additional fees for a higher pay rate, even with a general fee of as small as 1 dollar, casino is profiting

- With dumb strategy, the difference of winning probability of dealer and player is around 2%, while advanced strategy 
allows player to increase the difference up to 5%.

## Instructions on how to use the program:

## All Sources Used:

