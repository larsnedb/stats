import TimeParseUtils


class MatchEvent(object):
    # todo team?
    period = 0
    minutes = 0
    seconds = 0

    # todo sort by period, minutes, seconds so that goals and penalties are intertwined



class Goal(MatchEvent):
    scorer = ""
    assist = ""
    partial_result = ""
    team_name = ""


    def __init__(self, scorer, assist, partial_result, team_name, time):
        # type: (String, String, String, String, String) -> Goal
        self.scorer = scorer
        self.assist = assist
        self.partial_result = partial_result
        self.team_name = team_name
        self.period = TimeParseUtils.get_period_number(time)
        self.minutes, self.seconds = TimeParseUtils.get_time_in_minutes_and_seconds(time)

    def __str__(self):
        return "Goal: {}, time = {}:{}, scorer = {}"\
            .format(self.partial_result, self.minutes, self.seconds, self.scorer)


class Penalty(MatchEvent):
    team = ""
    player = ""
    duration = ""
    reason = ""

    def __init__(self, team, time, penalty):
        self.team = team
        self.period = TimeParseUtils.get_period_number(time)
        self.minutes, self.seconds = TimeParseUtils.get_time_in_minutes_and_seconds(time)
        self.player, self.duration, self.reason = get_player_info(penalty)

    def __str__(self):
        return "Penalty: team: {}, time = {}:{}, player = {}, duration = {}, reason: {}" \
            .format(self.team, self.minutes, self.seconds, self.player, self.duration, self.reason)


def get_player_info(penalty):
    player, duration, reason = penalty.split(',')
    return player.strip(), duration.strip(), reason.strip()