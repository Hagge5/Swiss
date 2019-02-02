from tournament import Tournament
from player import Player
from test_utilities import swedish_championship_tournament_and_wanted_pairings
from matchups import matchups_from_tuple_list
import unittest
import matchup_strategies.min_cost


class TestMatchupPossibilities(unittest.TestCase):

    def setUp(self):
        self.tournament = Tournament(matchup_strategies.min_cost)
        self.players = [Player(str(i)) for i in range(32)]


    def test_6_players_have_1_possible_matchups(self):
        for i in range(6):
            self.tournament.add_player(self.players[i])
        self.assertEqual(self.tournament.number_of_possible_pairings(), 1)


    def test_7_players_have_1_possible_matchups(self):
        for i in range(7):
            self.tournament.add_player(self.players[i])
        self.assertEqual(self.tournament.number_of_possible_pairings(), 1)


    def test_players_face_closest_player_in_list(self):
        for i in range(6):
            self.tournament.add_player(self.players[i])
        matchups = self.tournament.pairings()
        self.assertTrue(matchups.players_are_matched(self.players[0], \
                                                     self.players[1]))
        self.assertTrue(matchups.players_are_matched(self.players[2], \
                                                     self.players[3]))
        self.assertTrue(matchups.players_are_matched(self.players[4], \
                                                     self.players[5]))

    def test_players_face_closest_player_in_list_after_one_round(self):
        for i in range(8):
            self.tournament.add_player(self.players[i])
        matchups = self.tournament.pairings()
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        self.assertEqual(self.tournament.match_log().times_match_win(self.players[0]), 1)
        self.assertEqual(self.tournament.match_log().times_match_win(self.players[1]), 0)
        self.assertEqual(self.tournament.match_log().times_match_win(self.players[2]), 1)
        self.assertEqual(self.tournament.match_log().times_match_win(self.players[3]), 0)
        self.assertEqual(self.tournament.match_log().times_match_win(self.players[4]), 1)
        self.assertEqual(self.tournament.match_log().times_match_win(self.players[5]), 0)
        self.assertEqual(self.tournament.match_log().times_match_win(self.players[6]), 1)
        self.assertEqual(self.tournament.match_log().times_match_win(self.players[7]), 0)
        matchups = self.tournament.pairings()
        self.assertTrue(matchups.players_are_matched(self.players[0], \
                                                     self.players[2]))
        self.assertTrue(matchups.players_are_matched(self.players[4], \
                                                     self.players[6]))
        self.assertTrue(matchups.players_are_matched(self.players[1], \
                                                     self.players[3]))
        self.assertTrue(matchups.players_are_matched(self.players[5], \
                                                     self.players[7]))

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


    def test_mtg_swedish_championship(self):
        self.tournament, wanted = swedish_championship_tournament_and_wanted_pairings()
        wanted_players = [(self.tournament.player_name_player(e[0]), \
                           self.tournament.player_name_player(e[1])) \
                          for e in wanted]
        wanted_matchups = matchups_from_tuple_list(wanted_players, self.tournament.cost_map())
        m = self.tournament.pairings()
        print(m.badness_values(64))
        print(wanted_matchups.badness_values(64))
        self.assertEqual(m.badness(), wanted_matchups.badness())



if __name__ == "__main__":
    unittest.main()
