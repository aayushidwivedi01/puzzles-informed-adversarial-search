import homework3 as hw3
import unittest
import timeit

class TestTilePuzzle(unittest.TestCase):

    def test_is_legal_move(self):
        b = [[True, False], [True, False]];
        g = hw3.DominoesGame(b);
        self.assertFalse(g.is_legal_move(1,1,True));       

    def test_legal_moves(self):
        g = hw3.create_dominoes_game(3, 3)        
        self.assertEqual(list(g.legal_moves(True)), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),(1, 2)]);
        
        self.assertEqual(list(g.legal_moves(False)), [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0),(2, 1)]);

        b = [[True, False], [True, False]];
        g = hw3.DominoesGame(b);
        self.assertEqual(list(g.legal_moves(True)), [(0, 1)]);

        self.assertEqual(list(g.legal_moves(False)), []);

    def test_perform_move(self):
        g = hw3.create_dominoes_game(3, 3);
        g.perform_move(0, 1, True);
        self.assertEquals(g.get_board(), [[False, True,  False],\
                                         [False, True,  False],\
                                         [False, False, False]]);

        g = hw3.create_dominoes_game(3, 3)
        g.perform_move(1,0,False);
        self.assertEquals(g.get_board(), [[False, False, False],\
                                         [True,  True,  False],\
                                         [False, False, False]]);

    def test_game_over(self):
        b = [[False, False], [False, False]];
        g = hw3.DominoesGame(b);
        self.assertFalse(g.game_over(True));
        self.assertFalse(g.game_over(False));

        b = [[True, False], [True, False]];
        g = hw3.DominoesGame(b);
        self.assertFalse(g.game_over(True));
        self.assertTrue(g.game_over(False));

    def test_copy(self):
        g = hw3.create_dominoes_game(4, 4);
        g2 = g.copy();
        self.assertTrue(g.get_board() == g2.get_board());

    def test_successors(self):
        b = [[False, False], [False, False]];
        g = hw3.DominoesGame(b);
        for m, new_g in g.successors(True):
            print m, new_g.get_board();

        b = [[True, False], [True, False]]
        g = hw3.DominoesGame(b)
        for m, new_g in g.successors(True):
            print m, new_g.get_board()
    
    def test_get_random_move(self):
        g = hw3.create_dominoes_game(4,4);
        #print g.get_random_move(True);

    def test_score(self):
        b = [[False] * 3 for i in range(3)];
        g = hw3.DominoesGame(b)
        print g.get_best_move(True, 1)
        print g.get_best_move(True, 2)
        g.perform_move(0, 1, True);
        print g.get_best_move(False, 1)
        print g.get_best_move(False, 2)        
if __name__ == '__main__':
    unittest.main()


