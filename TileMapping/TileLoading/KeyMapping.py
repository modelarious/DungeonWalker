from TileMapping.TileLoading.TileSimilarity import Same, Different
def map_key_that_doesnt_exist_in_tileset_to_one_that_does(tileNeighborSettings):
	upperNeighbor = tileNeighborSettings[0][1]
	lowerNeighbor = tileNeighborSettings[2][1]
	leftNeighbor  = tileNeighborSettings[1][0]
	rightNeighbor = tileNeighborSettings[1][2]

	# build-a-key
	# if right neighbor is different, make all right tiles Different
	# if bottom neighbor is different, make all bottom tiles Different
	# etc...
	buildAKey = [
		[Same, Same, Same],
		[Same, Same, Same],
		[Same, Same, Same]
	]

	#apply all 4 of the following tests to map to a tile in the dataset
	if rightNeighbor == Different:
		# set the right side to Different
		# ex:
		# 	correctedKey = (
  		# 		(Same, Same, Different),
  		# 		(Same, Same, Different),
  		# 		(Same, Same, Different)
		# 	)
		for row in range(len(buildAKey)):
			buildAKey[row][-1] = Different
	
	if leftNeighbor == Different:
		# set the left side to Different
		# ex:
		# 	correctedKey = (
  		# 		(Different, Same, Same),
  		# 		(Different, Same, Same),
  		# 		(Different, Same, Same)
		# 	)
		for row in range(len(buildAKey)):
			buildAKey[row][0] = Different
	
	if lowerNeighbor == Different:
		# set the bottom row side to Different
		# ex:
		# 	correctedKey = (
  		# 		(Same, Same, Same),
  		# 		(Same, Same, Same),
  		# 		(Different, Different, Different)
		# 	)
		buildAKey[-1] = [Different, Different, Different]
	
	if upperNeighbor == Different:
		# set the top row side to Different
		# ex:
		# 	correctedKey = (
  		# 		(Same, Same, Same),
  		# 		(Same, Same, Same),
  		# 		(Different, Different, Different)
		# 	)
		buildAKey[0] = [Different, Different, Different]

	# turn our 3x3 array into 3x3 tuple so it is hashable
	tupleCorrectedKey = []
	for row in buildAKey:
		tupleCorrectedKey.append(tuple(row))

	return tuple(tupleCorrectedKey)

