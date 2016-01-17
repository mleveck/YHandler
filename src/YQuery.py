from YHandler import YHandler
from collections import OrderedDict
import requests
import re
import pkgutil
import json
from Selectors.DefaultSelector import DefaultSelector
from urllib import quote_plus


class YQuery:
    """
    A class with a few convenicence methods for querying the Yahoo Fantasy API.
    All queries occur for the current user underneath a game context, which for 
    Yahoo's API means that it occurs for a particular fantasy game (i.e. season long), 
    and not a specific player or team game.
    """
    def __init__(self, yhandler, game_key, selector=None):
        """
        Constructor creates a YQuery object with a particular fantasy game context, and maps that
        games stats into the stat_categories dictionary
        :param: yhandler - YHandler object
        :param: game_key - Yahoo fantasy API game key - these signify fantasy games, not sport games
        :param: [optional, BaseSelector] selector - selector to use for the querying the xml
        """
        self.yhandler = yhandler
        self.query_format = 'xml'
        self.stat_categories = {}
        self.game_key = game_key
        self.selector = selector if selector else DefaultSelector()
        self.ns = {'yh': 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng'}
        self.map_stat_categories()

    def map_stat_categories(self):
        """
        Maps a games stat categories to a Python dictionary. If successful,
        the mapping will be held under the stat_categories data attribute.
        :returns: bool - true if the mapping is succesful, false otherwise
        """
        save_format = self.yhandler.format
        self.yhandler.format = self.query_format
        resp = self.yhandler.api_req(str.format('game/{0}/stat_categories', self.game_key))
        self.yhandler.format = save_format
        if resp.status_code != requests.codes['ok']:
            return False
        selector = self.selector.selector(resp.content)
        for cat in selector.findall('.//yh:stats/yh:stat', self.ns):
            stat_id = cat.findall('./yh:stat_id', self.ns)[0].text
            self.stat_categories[stat_id] = {
                'name': cat.findall('./yh:display_name', self.ns)[0].text,
                'detail': cat.findall('./yh:name', self.ns)[0].text,
                'position_type': cat.findall('./yh:position_types/yh:position_type', self.ns)[0].text,
            }
        return True

    def get_games_info(self):
        """
        Get game information from Yahoo. This is only the fantasy games
        a particular user is involved in. Not the games of their league.
        :returns: response containing the game keys, codes (nfl, nba, et...), and
        types for the current user
        """
        resp = self.yhandler.api_req('games')
        if resp.status_code != requests.codes['ok']:
            return None
        return self.selector.selector(resp.content)

    def get_user_leagues(self):
        """
        Get the leagues a user has played in.
        :returns: list - Dictionary of league name/id pairs, None if fail
        """
        save_format = self.yhandler.format
        self.yhandler.format = self.query_format
        resp = self.yhandler.api_req(str.format('users;use_login=1/games;game_key={0}/leagues', self.game_key))
        self.yhandler.format = save_format
        if (resp.status_code != requests.codes['ok']):
            return None
        sel = self.selector.selector(resp.content)
        result = []
        for league in sel.findall('.//yh:league', self.ns):
            result.append({
                            league.findall('./yh:name', self.ns)[0].text: league.findall('./yh:league_id', self.ns)[0].text
                           })
        return result

    def query_player(self, player_id, resource):
        """
        Query a player resource for a particular fantasy game.
        :param: player_id - Yahoo player id
        :param: resource - Yahoo player resource to query
        :returns: response content, None if fail
        """
        save_format = self.yhandler.format
        self.yhandler.format = self.query_format
        resp = self.yhandler.api_req(str.format('player/{0}.p.{1}/{2}',
                                                self.game_key, player_id, resource))
        self.yhandler.format = save_format
        if resp.status_code != requests.codes['ok']:
            return None
        return self.selector.selector(resp.content)

    def get_player_stats(self, player_stats):
        stats = []
        for stat in player_stats.findall('.//yh:player_stats/yh:stats/yh:stat', self.ns):
            stat_id = stat.findall('./yh:stat_id', self.ns)[0].text
            stat_detail = self.stat_categories[stat_id].copy()
            stat_detail.remove('position_type')
            stat_detail['value'] = stat.findall('./yh:value', self.ns)[0].text
            stat_map = {stat_id: stat_detail}
            stats.append(stat_map)
        return stats

    def get_player_season_stats(self, player_id):
        resp = self.query_player(player_id, "stats")
        if resp == None:
            return None
        return self.get_player_stats(self.selector.selector(resp.content))

    def get_player_week_stats(self, player_id, week):
        resp = self.query_player(player_id, "stats;type=week;week=" + week)
        if resp == None:
            return None
        return self.get_player_stats(self.selector.selector(resp.content))

    def find_player(self, league_id, player_name):
        save_format = self.yhandler.format
        self.yhandler.format = self.query_format
        resp = self.yhandler.api_req(str.format('leagues;league_keys={0}.l.{1}/players;search={2}',
                                     self.game_key, league_id, quote_plus(player_name)))
        self.yhandler.format = save_format
        if resp == None:
            return None
        sel = self.selector.selector(resp.content)
        players = []
        for player in sel.findall('.//yh:players/yh:player', self.ns):
            player_detail = {}
            player_detail['id'] = player.findall('./yh:player_id', self.ns)[0].text
            player_detail['name'] = player.findall('./yh:name/yh:full', self.ns)[0].text
            player_detail['team'] = player.findall('./yh:editorial_team_full_name', self.ns)[0].text
            players.append(player_detail)
        return players

    def query_league(self, league_id, resource):
        """
        Query a league resource for a particular fantasy game.
        :param: league_id - Yahoo league id
        :param: resource - Yahoo league resource to query
        :returns: response content, None if fail
        """
        save_format = self.yhandler.format
        self.yhandler.format = self.query_format
        resp = self.yhandler.api_req(str.format('league/{0}.l.{1}/{2}', self.game_key, leage_id, resource))
        self.yhandler.format = save_format
        if (resp.status_code != requests.codes['ok']):
            return None
        return self.selector.selector(resp.content)




