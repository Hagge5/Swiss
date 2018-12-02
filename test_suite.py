from tournament import Tournament
from player import Player
import unittest
import matchup_strategies.min_cost


class TestMatchupPossibilities(unittest.TestCase):

    def setUp(self):
        self.tournament = Tournament(matchup_strategies.min_cost)
        self.players = [Player(str(i)) for i in range(32)]


    def test_6_players_have_15_possible_matchups(self):
        for i in range(6):
            self.tournament.add_player(self.players[i])
        self.assertEqual(self.tournament.number_of_possible_pairings(), 15)


    def test_7_players_have_105_possible_matchups(self):
        for i in range(7):
            self.tournament.add_player(self.players[i])
        self.assertEqual(self.tournament.number_of_possible_pairings(), 105)


    def test_6_players_result_removes_3_matchups(self):
        for i in range(6):
            self.tournament.add_player(self.players[i])
        self.tournament.add_result(self.players[0], self.players[1], 1, 0)
        self.assertEqual(self.tournament.number_of_possible_pairings(), 15 - 3)


    def test_4_players_two_rounds(self):
        for i in range(4):
            self.tournament.add_player(self.players[i])
        # First round
        matchups = self.tournament.pairings()
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.ranking()
        self.assertEqual(ranking.entries()[0].score(), 1)
        self.assertEqual(ranking.entries()[1].score(), 1)
        self.assertEqual(ranking.entries()[2].score(), 0)
        self.assertEqual(ranking.entries()[3].score(), 0)
        # Second round
        matchups = self.tournament.pairings()
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.ranking()
        self.assertEqual(ranking.entries()[0].score(), 2)
        self.assertEqual(ranking.entries()[1].score(), 1)
        self.assertEqual(ranking.entries()[2].score(), 1)
        self.assertEqual(ranking.entries()[3].score(), 0)


    def test_8_players_three_rounds(self):
        for i in range(8):
            self.tournament.add_player(self.players[i])
        # First round
        matchups = self.tournament.pairings()
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.ranking()
        self.assertEqual(ranking.entries()[0].score(), 1)
        self.assertEqual(ranking.entries()[1].score(), 1)
        self.assertEqual(ranking.entries()[2].score(), 1)
        self.assertEqual(ranking.entries()[3].score(), 1)
        self.assertEqual(ranking.entries()[4].score(), 0)
        self.assertEqual(ranking.entries()[5].score(), 0)
        self.assertEqual(ranking.entries()[6].score(), 0)
        self.assertEqual(ranking.entries()[7].score(), 0)
        # Second round
        matchups = self.tournament.pairings()
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.ranking()
        self.assertEqual(ranking.entries()[0].score(), 2)
        self.assertEqual(ranking.entries()[1].score(), 2)
        self.assertEqual(ranking.entries()[2].score(), 1)
        self.assertEqual(ranking.entries()[3].score(), 1)
        self.assertEqual(ranking.entries()[4].score(), 1)
        self.assertEqual(ranking.entries()[5].score(), 1)
        self.assertEqual(ranking.entries()[6].score(), 0)
        self.assertEqual(ranking.entries()[7].score(), 0)
        # Third round
        matchups = self.tournament.pairings()
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.ranking()
        self.assertEqual(ranking.entries()[0].score(), 3)
        self.assertEqual(ranking.entries()[1].score(), 2)
        self.assertEqual(ranking.entries()[2].score(), 2)
        self.assertEqual(ranking.entries()[3].score(), 2)
        self.assertEqual(ranking.entries()[4].score(), 1)
        self.assertEqual(ranking.entries()[5].score(), 1)
        self.assertEqual(ranking.entries()[6].score(), 1)
        self.assertEqual(ranking.entries()[7].score(), 0)


    def test_no_players(self):
        m = self.tournament.pairings()
        self.assertEqual(m.pairs, [])
        self.assertIsNone(m.bye_player, None)
        self.assertEqual(self.tournament.number_of_possible_pairings(), 1)


    def test_one_player(self):
        self.tournament.add_player(self.players[0])
        m = self.tournament.pairings()
        self.assertEqual(m.pairs, [])
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(self.tournament.number_of_possible_pairings(), 1)


    def test_two_players(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        m = self.tournament.pairings()
        self.assertTrue(m.players_are_matched(self.players[0], self.players[1]))
        self.assertEqual(len(m.pairs), 1)
        self.assertIsNone(m.bye_player, None)
        self.assertEqual(self.tournament.number_of_possible_pairings(), 1)


    def test_player_added_twice_should_be_the_same_as_added_once(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[0])
        m = self.tournament.pairings()
        self.assertEqual(m.pairs, [])
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(self.tournament.number_of_possible_pairings(), 1)


    def test_three_players_worst_performer_gets_bye(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        self.tournament.add_player(self.players[2])
        self.tournament.add_result(self.players[0], self.players[1], 1, 0)
        self.tournament.add_result(self.players[1], self.players[2], 1, 0)
        m = self.tournament.pairings()
        self.assertTrue(m.players_are_matched(self.players[0], self.players[1]))
        self.assertEqual(len(m.pairs), 1)
        self.assertEqual(m.bye_player, self.players[2])
        self.assertEqual(self.tournament.number_of_possible_pairings(), 1)


    def test_byed_player_dont_get_byed_again(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        self.tournament.add_player(self.players[2])
        self.tournament.add_result(self.players[0], self.players[1], 1, 0)
        self.tournament.add_result(self.players[0], self.players[2], 1, 0)
        self.tournament.add_bye(self.players[1])
        self.tournament.add_bye(self.players[2])
        m = self.tournament.pairings()
        self.assertTrue(m.players_are_matched(self.players[1], self.players[2]))
        self.assertEqual(len(m.pairs), 1)
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(self.tournament.number_of_possible_pairings(), 1)


    def test_first_round_any_player_can_be_randomly_byed(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        self.tournament.add_player(self.players[2])
        max_attempts = 8192
        byed_players = set()
        for i in range(max_attempts):
            m = self.tournament.pairings()
            self.assertEqual(len(m.pairs), 1)
            self.assertIsNotNone(m.bye_player)
            byed_players.add(m.bye_player)
            if len(byed_players) == 3:
                break
        self.assertEqual(len(byed_players), 3)
        self.assertEqual(self.tournament.number_of_possible_pairings(), 3)

if __name__ == "__main__":
    unittest.main()
