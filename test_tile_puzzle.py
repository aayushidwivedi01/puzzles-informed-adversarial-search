import homework3 as hw3
import timeit
import unittest

#Tile Puzzle
class TestTilePuzzle(unittest.TestCase):
	def test_init(self):
		board = [[1, 2], [3, 0]]
		puzzle = hw3.TilePuzzle(board)
		self.assertEquals(puzzle.get_board(), board)
		
		board = [[0, 1], [3, 2]]
		puzzle = hw3.TilePuzzle(board)
		self.assertEquals(puzzle.get_board(), board)
		
	def test_create_tile_puzzle(self):
		puzzle = hw3.create_tile_puzzle(3,3)
		self.assertEquals(puzzle.get_board(), [[1, 2, 3], [4, 5, 6], [7, 8, 0]])
		
		puzzle = hw3.create_tile_puzzle(2,4)
		self.assertEquals(puzzle.get_board(), [[1, 2, 3, 4], [5, 6, 7, 0]])
		
		puzzle = hw3.create_tile_puzzle(4,0)
		self.assertEquals(puzzle.get_board(), [[], [], [], []])
		
		#puzzle = hw3.create_tile_puzzle(0,0)
		#self.assertEquals(puzzle.get_board(), [])
		
	def test_perform_move(self):
		puzzle = hw3.create_tile_puzzle(3,3)
		self.assertTrue(puzzle.perform_move("up"))
		self.assertEquals(puzzle.get_board(), [[1, 2, 3], [4, 5, 0], [7, 8, 6]])
		puzzle = hw3.TilePuzzle([[0, 2, 3], [4, 5, 6], [7, 8, 1]])
		self.assertFalse(puzzle.perform_move("up"))
		self.assertEquals(puzzle.get_board(), [[0, 2, 3], [4, 5, 6], [7, 8, 1]])
		self.assertTrue(puzzle.perform_move("right"))
		self.assertEquals(puzzle.get_board(), [[2, 0, 3], [4, 5, 6], [7, 8, 1]])
		puzzle = hw3.create_tile_puzzle(3,3)
		self.assertFalse(puzzle.perform_move("right"))
		self.assertEquals(puzzle.get_board(), [[1, 2, 3], [4, 5, 6], [7, 8, 0]])
		puzzle = hw3.TilePuzzle([[0, 2, 3], [4, 5, 6], [7, 8, 1]])
		puzzle = hw3.create_tile_puzzle(3,3)
		self.assertFalse(puzzle.perform_move("down"))
		self.assertEquals(puzzle.get_board(), [[1, 2, 3], [4, 5, 6], [7, 8, 0]])
		self.assertTrue(puzzle.perform_move("left"))
		self.assertEquals(puzzle.get_board(), [[1, 2, 3], [4, 5, 6], [7, 0, 8]])
		
	def test_is_solved(self):
		puzzle = hw3.TilePuzzle([[1, 2], [3, 0]])
		self.assertTrue(puzzle.is_solved())
		puzzle.perform_move("up")
		self.assertFalse(puzzle.is_solved())
		puzzle = hw3.TilePuzzle([[1, 2], [3, 0]])
		puzzle.perform_move("right")
		self.assertTrue(puzzle.is_solved())
		puzzle = hw3.TilePuzzle([[0, 2], [3, 1]])
		self.assertFalse(puzzle.is_solved())
		
	def test_copy(self):
		puzzle = hw3.create_tile_puzzle(3,3)
		puzzle2 = puzzle.copy()
		self.assertTrue(puzzle.get_board() == puzzle2.get_board())
		
		puzzle = hw3.create_tile_puzzle(3,3)
		puzzle2 = puzzle.copy()
		puzzle.perform_move("left")
		self.assertFalse(puzzle.get_board() == puzzle2.get_board())
		
	#def test_successors(self):
	#	puzzle = hw3.create_tile_puzzle(3, 3)
	#	i = 0
	#	successors = [("up",[[1, 2, 3], [4, 5, 0], [7, 8, 6]]), ("left", [[1, 2, 3], [4, 5, 6], [7, 0, 8]])]
	#	result = list(puzzle.successors())
	#	self.assertEquals([(move, puzzle.get_board()) for (move, puzzle) in result],successors)
		
	#	board = [[1,2,3], [4,0,5], [6,7,8]]
	#	puzzle = hw3.TilePuzzle(board)
	#	successors = [("up", [[1, 0, 3], [4, 2, 5], [6, 7, 8]]),("down",[[1, 2, 3], [4, 7, 5], [6, 0, 8]]),("left",[[1, 2, 3], [0, 4, 5], [6, 7, 8]]),("right",[[1, 2, 3], [4, 5, 0], [6, 7, 8]])]	
	#	result = list(puzzle.successors())
	#	self.assertEquals([(move, puzzle.get_board()) for (move, puzzle) in result],successors)
		
	#	board = [[1,2], [0,3]]
	#	puzzle = hw3.TilePuzzle(board)
	#	successors = [("up", [[0,2], [1, 3]]), ("right", [[1,2], [3,0]])]
	#	result = list(puzzle.successors())
	#	self.assertEquals([(move, puzzle.get_board()) for (move, puzzle) in result],successors)
		
	def test_find_solutions_iddfs(self):
		board = [[1,2], [0,3]]
		puzzle = hw3.TilePuzzle(board)
		solutions = list(puzzle.find_solutions_iddfs())
		self.assertEquals(solutions, [["right"]])
		
		board = [[1,2], [3,0]]
		puzzle = hw3.TilePuzzle(board)
		solutions = list(puzzle.find_solutions_iddfs())
		self.assertEquals(solutions, [[]])
		
		board = [[1,2,3], [4,0,8], [7,6,5]]
		puzzle = hw3.TilePuzzle(board)
		solutions = list(puzzle.find_solutions_iddfs())
		self.assertEquals(solutions, [['down', 'right', 'up', 'left', 'down','right'], ['right', 'down', 'left','up', 'right', 'down']])
		
		board = [[4,1,2], [0,5,3], [7,8,6]]
		puzzle = hw3.TilePuzzle(board)
		solutions = list(puzzle.find_solutions_iddfs())
		self.assertEquals(solutions, [['up', 'right', 'right', 'down', 'down']])	
		
		board = [[4,1,2], [0,5,3], [7,8,6]]
		puzzle = hw3.TilePuzzle(board)
		solutions = puzzle.find_solutions_iddfs()
		self.assertEquals(next(solutions), ['up', 'right', 'right', 'down', 'down'])
		
	def test_find_solution_a_star(self):
		board = [[1,2], [0,3]]
		puzzle = hw3.TilePuzzle(board)
		self.assertEquals(puzzle.find_solution_a_star(), ["right"])
		
		board = [[4,1,2], [0,5,3], [7,8,6]]
		puzzle = hw3.TilePuzzle(board)
		self.assertEquals(puzzle.find_solution_a_star(), ['up', 'right', 'right', 'down', 'down'])
		
		board = [[1,2,3], [4,0,5], [6,7,8]]
		puzzle = hw3.TilePuzzle(board)
		self.assertEquals(puzzle.find_solution_a_star(), ['right', 'down', 'left', 'left', 'up','right', 'down', 'right', 'up', 'left','left', 'down', 'right', 'right'])
		

#Grid Navigation
class TestGridNavigation(unittest.TestCase):
	
	#def test_get_euclidean_score(self):
	#	self.assertEquals(hw3.get_euclidean_score((1,1), (1,1)), 0)
	#	self.assertEquals(hw3.get_euclidean_score((1,1), (0,0)), 2**0.5)
		
	def test_get_next_states(self):
		scene = [[False, False, False],[False, True , False],[False, False, False]]
		curresnt_pos  = (0,0)
		successors = list(hw3.get_next_states(curresnt_pos, scene))
		self.assertEquals(successors, [(1,0), (0,1)])
		
		scene = [[False, False, False],[False, False , False],[False, False, False]]
		curresnt_pos  = (1,1)
		successors = list(hw3.get_next_states(curresnt_pos, scene))
		self.assertEquals(successors, [(0,1),(2,1),(1,0),(1,2),(0,0),(0,2),(2,0),(2,2)])
		
		scene = [[False, False, False],[False, False , False],[False, False, True]]
		curresnt_pos  = (1,1)
		successors = list(hw3.get_next_states(curresnt_pos, scene))
		self.assertEquals(successors, [(0,1),(2,1),(1,0),(1,2),(0,0),(0,2),(2,0)])
		
	def test_find_path(self):
		scene = [[False, False, False],[False, True , False],[False, False, False]]
		self.assertEquals(hw3.find_path((0, 0), (2, 1), scene), [(0, 0), (1, 0), (2, 1)])
		
		scene = [[False, True, False],[False, True , False],[False, True, False]]
		self.assertEquals(hw3.find_path((0, 0), (0, 2), scene), None)
		
#Linear Disk Movement
class TestLinearDiskMovement(unittest.TestCase):		
	# def test_solve_distinct_disks(self):
		# #print 'disks'
		# self.assertEqual(hw3.solve_distinct_disks(4,2), [(0, 2), (2, 3), (1, 2)])
		# self.assertEqual(hw3.solve_distinct_disks(5,2), [(0, 2), (1, 3), (2, 4)])
		# self.assertEqual(hw3.solve_distinct_disks(4,3), [(1, 3), (0, 1), (2, 0), (3, 2), (1, 3),(0, 1)])
		# self.assertEqual(hw3.solve_distinct_disks(5,3), [(1, 3), (2, 1), (0, 2), (2, 4), (1, 2)])
		# self.assertEqual(hw3.solve_distinct_disks(0,0), [])
		# self.assertEqual(hw3.solve_distinct_disks(5,5), None)
		# self.assertEqual(hw3.solve_distinct_disks(5,0), [])
		# res = hw3.solve_distinct_disks(8,7)
		# self.assertEqual(len(res), 28)
		# #print len(res)
		# res = hw3.solve_distinct_disks(10,5)
		# self.assertEqual(len(res), 15)
		# #print len(res)
		# res = hw3.solve_distinct_disks(9,6)
		# self.assertEqual(len(res), 23)
		# #print len(res)
		# res = hw3.solve_distinct_disks(11,4)
		# self.assertEqual(len(res), 18)
		# #print len(res)
		# res = hw3.solve_distinct_disks(7,8)
		# self.assertEqual(res, None)
		# #print res
		
	def test_solve_distinct_disks(self):
		#print 'a star'
		sol = hw3.solve_distinct_disks(4,2)
		self.assertEqual(len(sol), 3)
		sol = hw3.solve_distinct_disks(5,2)
		self.assertEqual(len(sol), 3)
		sol = hw3.solve_distinct_disks(4,3)
		self.assertEqual(len(sol), 6)
		sol = hw3.solve_distinct_disks(5,3)
		self.assertEqual(len(sol), 5)
		sol = hw3.solve_distinct_disks(0,0)
		self.assertEqual(len(sol), 0)
		sol = hw3.solve_distinct_disks(5,5)
		self.assertEqual(sol, None)
		sol = hw3.solve_distinct_disks(5,0)
		self.assertEqual(len(sol), 0)
		sol = hw3.solve_distinct_disks(8,7)
		self.assertEqual(len(sol), 28)
		#print len(sol)
		sol = hw3.solve_distinct_disks(10,5)
		self.assertEqual(len(sol), 15)
		#print len(sol)
		sol = hw3.solve_distinct_disks(9,6)
		self.assertEqual(len(sol), 23)
		#print len(sol)
		sol = hw3.solve_distinct_disks(11,4)
		self.assertEqual(len(sol), 18)
		#print len(sol)
		sol = hw3.solve_distinct_disks(7,8)
		self.assertEqual(sol, None)
		#print sol
		sol = hw3.solve_distinct_disks(16,8)
		self.assertEqual(len(sol), 36)
		#print len(sol)
		sol = hw3.solve_distinct_disks(18,6)
		self.assertEqual(len(sol), 39)
		#print len(sol)
		
#Dominoes
class TestDominoes(unittest.TestCase):
	def test_init(self):
		b = [[False, False], [False, False]]
		g = hw3.DominoesGame(b)
		self.assertEqual(g.get_board(), b)
		
		b = [[True, False], [True, False]]
		g = hw3.DominoesGame(b)
		self.assertEqual(g.get_board(), b)
		
		#b = []
		#g = hw3.DominoesGame(b)
		#self.assertEqual(g.get_board(), b)
	
	def test_create_dominoes_game(self):
		g = hw3.create_dominoes_game(2, 2)
		self.assertEqual(g.get_board(), [[False, False], [False, False]])
		
		g = hw3.create_dominoes_game(2, 3)
		self.assertEqual(g.get_board(), [[False, False, False],[False, False, False]])
		
		g = hw3.create_dominoes_game(2, 0)
		self.assertEqual(g.get_board(), [[],[]])
		
		#g = hw3.create_dominoes_game(0, 0)
		#self.assertEqual(g.get_board(), [])
		
	def test_reset(self):
		b = [[True, True], [True, False]]
		g = hw3.DominoesGame(b)
		g.reset()
		self.assertEqual(g.get_board(), [[False, False], [False, False]])
		
		b = [[True, True], [True, True]]
		g = hw3.DominoesGame(b)
		g.reset()
		self.assertEqual(g.get_board(), [[False, False], [False, False]])
		
		g = hw3.create_dominoes_game(2, 2)
		g.reset()
		self.assertEqual(g.get_board(), [[False, False], [False, False]])
		
		#g = hw3.create_dominoes_game(0, 0)
		#g.reset()
		#self.assertEqual(g.get_board(), [])
		
	def test_valid_move(self):
		g = hw3.create_dominoes_game(2, 2)
		self.assertTrue(g.is_legal_move(0, 0, True))
		self.assertTrue(g.is_legal_move(0, 0, False))
		self.assertFalse(g.is_legal_move(1, 1, False))
		
		b = [[True, False], [False, False]]
		g = hw3.DominoesGame(b)
		self.assertFalse(g.is_legal_move(0, 0, True))
		self.assertFalse(g.is_legal_move(0, 0, False))
		self.assertTrue(g.is_legal_move(0, 1, True))
		self.assertFalse(g.is_legal_move(0, 1, False))
		self.assertTrue(g.is_legal_move(1, 0, False))
		
	def test_legal_moves(self):
		g = hw3.create_dominoes_game(3, 3)
		self.assertEqual(list(g.legal_moves(True)), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)])
		self.assertEqual(list(g.legal_moves(False)), [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0),(2, 1)])
		
		b = [[True, False], [True, False]]
		g = hw3.DominoesGame(b)
		self.assertEqual(list(g.legal_moves(True)), [(0, 1)])
		self.assertEqual(list(g.legal_moves(False)), [])
		
	def test_perform_move(self):
		g = hw3.create_dominoes_game(3, 3)
		g.perform_move(0, 1, True)
		self.assertEqual(g.get_board(), [[False, True,  False],[False, True,  False],[False, False, False]])
		
		g = hw3.create_dominoes_game(3, 3)
		g.perform_move(1, 0, False)
		self.assertEqual(g.get_board(), [[False, False,  False],[True, True,  False],[False, False, False]])
		
	def test_game_over(self):
		b = [[False, False], [False, False]]
		g = hw3.DominoesGame(b)
		self.assertFalse(g.game_over(True))
		self.assertFalse(g.game_over(False))
		
		b = [[True, False], [True, False]]
		g = hw3.DominoesGame(b)
		self.assertFalse(g.game_over(True))
		self.assertTrue(g.game_over(False))
		
	def test_copy(self):
		g = hw3.create_dominoes_game(4, 4)
		g2 = g.copy()
		self.assertTrue((g.get_board() == g2.get_board()))
		
		g = hw3.create_dominoes_game(4, 4)
		g2 = g.copy()
		g.perform_move(0, 0, False)
		self.assertFalse((g.get_board() == g2.get_board()))
		
	#def test_successors(self):
	#	b = [[False, False], [False, False]]
	#	g = hw3.DominoesGame(b)
	#	result = [((0, 0), [[True, False], [True, False]]), ((0, 1) ,[[False, True], [False, True]])]
	#	self.assertEqual(result, [(move, game.get_board()) for move, game in list(g.successors(True))])
		
	#	b = [[True, False], [True, False]]
	#	g = hw3.DominoesGame(b)
	#	result = [((0, 1), [[True, True], [True, True]])]
	#	self.assertEqual(result, [(move, game.get_board()) for move, game in list(g.successors(True))])
		
	def test_get_random_move(self):
		g = hw3.create_dominoes_game(3, 3)
		self.assertTrue((g.get_random_move(True) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]))
		self.assertTrue((g.get_random_move(True) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]))
		self.assertTrue((g.get_random_move(True) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]))
		self.assertTrue((g.get_random_move(True) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]))
		self.assertTrue((g.get_random_move(True) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]))
		self.assertTrue((g.get_random_move(True) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]))
		self.assertTrue((g.get_random_move(True) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]))
		self.assertTrue((g.get_random_move(True) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]))
		
	#def test_get_score(self):
	#	g = hw3.create_dominoes_game(2, 2)
	#	self.assertEqual(g.get_score(True), 0)
	#	self.assertEqual(g.get_score(False), 0)
	#	b = [[False, True, False], [False, True, False], [False, False, False]]
	#	g = hw3.DominoesGame(b)
	#	self.assertEqual(g.get_score(True), 2)
	#	self.assertEqual(g.get_score(False), -2)
		
	def test_get_best_move(self):
		b = [[False] * 3 for i in xrange(3)]
		g = hw3.DominoesGame(b)
		best_score = g.get_best_move(True, 1)
		self.assertEqual(best_score, ((0, 1), 2, 6))
		best_score = g.get_best_move(True, 2)
		self.assertEqual(best_score, ((0, 1), 3, 10))
		g.perform_move(0, 1, True)
		best_score = g.get_best_move(False, 1)
		self.assertEqual(best_score, ((2, 0), -3, 2))
		best_score = g.get_best_move(False, 2)
		self.assertEqual(best_score, ((2, 0), -2, 5))
		
		b = [[True] * 3 for i in xrange(3)]
		g = hw3.DominoesGame(b)
		best_score = g.get_best_move(True, 2)
		self.assertEqual(best_score, (None, 0, 1))
		best_score = g.get_best_move(False, 2)
		self.assertEqual(best_score, (None, 0, 1))
		
		b = [[False] * 5 for i in xrange(5)]
		g = hw3.DominoesGame(b)
		best_score = g.get_best_move(True, 5)
		
if __name__ == '__main__':
	unittest.main()
