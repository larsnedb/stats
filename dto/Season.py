#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from Helper import MatchResult as MatchResult


class Season(object):
    team_name = ""
    matches = []
    goals_for = []
    goals_against = []
    assists = []
    penalties = []
    top_scorers = []
    match_results = []

    def __init__(self, team_name, matches):
        self.team_name = team_name
        self.matches = get_matches_for_team(team_name, matches)
        self.goals_for = get_goals_for(self, self.matches)
        self.goals_against = get_goals_against(self, self.matches)
        self.top_scorers = get_events_grouped_by_player(self.goals_for)
        self.assists = get_assists_by_player(self.goals_for)
        self.penalties = get_penalty_minutes_per_player(get_penalties(self, self.matches))
        self.match_results = get_match_results_for_team(self, self.matches)

    def __str__(self):
        return "Team name : {}" \
               "\nNumber of matches played: {}" \
               "\nNumber of full time wins: {}" \
               "\nNumber of penalty wins: {}" \
               "\nNumber of penalty losses: {}" \
               "\nNumber of full time losses: {}" \
               "\nNumber of goals scored: {}" \
               "\nNumber of goals conceded: {}" \
               "\nGoal Differential: {}" \
               "\nNumber of points for team: {}" \
               "\n\nNumber of goal scorers: {}" \
               "\nNumber of players with penalties: {}" \
               "\n\nScorers: {}" \
               "\n\nAssists: {}" \
               "\n\nPenalty minutes per player: {}" \
            .format(self.team_name,
                    len(self.matches),
                    get_number_of_occurrences(self.match_results, MatchResult.WIN),
                    get_number_of_occurrences(self.match_results, MatchResult.WIN_PEN),
                    get_number_of_occurrences(self.match_results, MatchResult.LOSS_PEN),
                    get_number_of_occurrences(self.match_results, MatchResult.LOSS),
                    len(self.goals_for), len(self.goals_against),
                    len(self.goals_for) - len(self.goals_against),
                    find_number_of_points(self.match_results),

                    len(self.top_scorers),
                    len(self.penalties),
                    print_entries_sorted(self.top_scorers),
                    print_entries_sorted(self.assists),
                    print_entries_sorted(self.penalties))


def get_matches_for_team(team_name, matches):
    matches_for_team = []
    for match in matches:
        if match.home_team == team_name or match.away_team == team_name:
            matches_for_team.append(match)
    return matches_for_team


def get_penalties(self, matches):
    penalties = []

    for match in matches:
        for penalty in match.penalties:
            if penalty.team == self.team_name:
                penalties.append(penalty)
    return penalties


def get_goals_for(self, matches):
    goals = []
    for match in matches:
        for goal in match.goals:
            if goal.team == self.team_name:
                goals.append(goal)
    return goals


def get_goals_against(self, matches):
    goals = []
    for match in matches:
        for goal in match.goals:
            if goal.team != self.team_name:
                goals.append(goal)
    return goals


def get_assists(self, matches):
    assists = []
    for match in matches:
        for goal in match.goals:
            if goal.team == self.team_name and goal.assist != "":
                assists.append(goal.assist)
    return assists


def get_penalty_minutes_per_player(penalties):
    minutes_per_player = {}
    for entry in penalties:
        if entry.player not in minutes_per_player:
            minutes_per_player[entry.player] = entry.duration
        else:
            minutes_per_player[entry.player] += entry.duration
    return minutes_per_player


def get_events_grouped_by_player(list_of_events):
    events = []
    for goal in list_of_events:
        events.append(goal.player)
    return Counter(events)


def get_assists_by_player(goals):
    assists = []
    for goal in goals:
        if goal.assist != "":
            assists.append(goal.assist)
    return Counter(assists)


def get_match_results_for_team(self, matches):
    results = []
    for match in matches:
        if match.home_team == self.team_name:
            results.append(match.match_info.result_for_home_team)
        elif match.away_team == self.team_name:
            results.append(match.match_info.result_for_away_team)
        else:
            raise ValueError('Team must be either home or away')
    return results


def find_number_of_points(results):
    points = 0
    for result in results:
        if result == MatchResult.WIN:
            points += 3
        elif result == MatchResult.WIN_PEN:
            points += 2
        elif result == MatchResult.LOSS_PEN:
            points += 1
    return points


def get_number_of_occurrences(match_results, final_result):
    occurrences = 0
    for result in match_results:
        if result == final_result:
            occurrences += 1
    return occurrences


def print_entries_sorted(match_events):
    s = ""
    for key, value in sorted(match_events.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        s += '\n' + key + ": " + str(value)
    return s.encode('utf-8')