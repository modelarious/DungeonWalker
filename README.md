Starting:

- implement A_star based on a neighbor list
- generate arbitrary maze
- process maze structure into a condensed neighbor list (take a hint from computerphile maze traversal video)


scratchpad:

- Rooms should be defined as an area that is 2*2 or larger... hmm... maybe just track where you put each room and the size of the room.. as a maze could technically be entirely open
- Rooms will have A_star run on them to determine the quickest path from each endpoint
- Rooms can optionally be a maze
- Generate a tree structure before hand that defines which rooms have which neighboring rooms, then determine the path length between those rooms
randomly.  Then use BFS to search to the depth of that length and generate a path to the next room of the desired length
- player agent will move through the space based on the A_star output which should tell them the easiest way to get to the goal
- player will use 10-ply minimax to determine how to act if an enemy is within 4 spaces of them
- enemies will use A_star to determine the quickest path to the player.  They should be able to do this is in a grand scale to
figure out which rooms to take to get to the player the quickest, only resorting to calling A_star when they get in the room with the player
- figure out a way to combine the objective function of A_star reaching the goal quickly, with the strategic advantage of minimax search
- I can't decide if I should train a convnet based on the 5*5 grid surrounding the player or if I should use a recurrent neural net.. as time steps matter

- What about an implementation of monte carlo tree search, where the move ordering is:
	- the first move is always what A* suggests: move towards the goal
	- the rest of the moves are ordered by a 15 ply minimax search
	- a bad result is based on how much damage the agent sustained and how much they travelled towards the goal.. need some intuitive way of weighting this because I don't want them trading all their health to get close to the exit, but I don't want them wandering aimlessly if they just care about sustaining their health... maybe give them 1 health?
	- maximum score is all health and travelled 15 spaces towards the goal
	- min score is lost all health


