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
    A class with a few convenience methods for querying the Yahoo Fantasy API.
    All queries occur for the current user underneath a game context, which for 
    Yahoo's API means that it occurs for a particular sport and fantasy game (i.e. nfl - season long),
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
        selector = self.yhandler.format = save_format
        if resp.status_code != requests.codes['ok']:
            return False
        self.selector.parse(resp.content)
        for cat in self.selector.iter_select('.//yh:stats/yh:stat', self.ns):
            stat_id = cat.select_one('./yh:stat_id', self.ns).text
            self.stat_categories[stat_id] = {
                'name': cat.select_one('./yh:display_name', self.ns).text,
                'detail': cat.select_one('./yh:name', self.ns).text,
                'position_type': cat.select_one('./yh:position_types/yh:position_type', self.ns).text,
            }
        return True

    def get_games_info(self, available_only=False):
        """
        Get game information from Yahoo. This is only the fantasy games
        a particular user is involved in. Not the games of their league.
        :param: available_only - only returns available games for the user
        :returns: selector of games xml for the current user
        """
        if available_only:
            resp = self.yhandler.api_req('games;is_available=1')
        else:
            resp = self.yhandler.api_req('games')
        if resp.status_code != requests.codes['ok']:
            return None

        games = []
        for game in self.selector.iter_select('.//yh:game', self.ns):
            game_detail = {
                'key': game.select_one('./yh:game_key', self.ns).text,
                'code': game.select_one('./yh:code', self.ns).text,
                'name': game.select_one('./yh:name', self.ns).text,
                'season': game.select_one('./yh:season', self.ns).text,
                'type': game.select_one('./yh:season', self.ns).text
            }
            games.append(game_detail)
        return games

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
        sel = self.selector.parse(resp.content)
        result = []
        for league in sel.iter_select('.//yh:league', self.ns):
            result.append({
                'id': league.select_one('./yh:league_id', self.ns).text,
                'name': league.select_one('./yh:name', self.ns).text,
                'season': league.select_one('./yh:season', self.ns).text,
                'week': league.select_one('./yh:current_week', self.ns).text,
                'is_finished': (lambda val: True if val else False)(league.select_one('./yh:is_finished', self.ns).text)
             })
        return result

    def query_player(self, player_id, resource):
        """
        Query a player resource for a particular fantasy game.
        :param: player_id - Yahoo player id
        :param: resource - Yahoo player resource to query
        :returns: selector around response content, None if fail
        """
        save_format = self.yhandler.format
        self.yhandler.format = self.query_format
        resp = self.yhandler.api_req(str.format('player/{0}.p.{1}/{2}',
                                                self.game_key, player_id, resource))
        self.yhandler.format = save_format
        if resp.status_code != requests.codes['ok']:
            return None
        return self.selector.parse(resp.content)

    def get_player_stats(self, player_stats):
        """
        Get dictionary of player stats
        :param: player_stats - selector around stats xml response
        :returns: stats as a dictionary
        """
        stats = {}
        for stat in player_stats.iter_select('.//yh:player_stats/yh:stats/yh:stat', self.ns):
            stat_id = stat.select_one('./yh:stat_id', self.ns).text
            stat_detail = self.stat_categories[stat_id].copy()
            stat_detail.pop('position_type', None)
            stat_detail['value'] = stat.select_one('./yh:value', self.ns).text
            stat_map = {stat_id: stat_detail}
            stats.update(stat_map)
        return stats

    def get_player_season_stats(self, player_id):
        resp = self.query_player(player_id, "stats")
        if not resp:
            return None
        return self.get_player_stats(resp)

    def get_player_week_stats(self, player_id, week):
        resp = self.query_player(player_id, "stats;type=week;week=" + week)
        if not resp:
            return None
        return self.get_player_stats(resp)

    def find_player(self, league_id, player_name):
        save_format = self.yhandler.format
        self.yhandler.format = self.query_format
        resp = self.yhandler.api_req(str.format('leagues;league_keys={0}.l.{1}/players;search={2}',
                                     self.game_key, league_id, quote_plus(player_name)))
        self.yhandler.format = save_format
        if not resp:
            return None
        sel = self.selector.parse(resp.content)
        players = []
        for player in sel.iter_select('.//yh:players/yh:player', self.ns):
            player_detail = {}
            player_detail['id'] = player.select_one('./yh:player_id', self.ns).text
            player_detail['name'] = player.select_one('./yh:name/yh:full', self.ns).text
            player_detail['team'] = player.select_one('./yh:editorial_team_full_name', self.ns).text
            players.append(player_detail)
        return players

    def query_league(self, league_id, resource):
        """
        Query a league resource for a particular fantasy game.
        :param: league_id - Yahoo league id
        :param: resource - Yahoo league resource to query
        :returns: selector of response content, None if fail
        """
        save_format = self.yhandler.format
        self.yhandler.format = self.query_format
        resp = self.yhandler.api_req(str.format('league/{0}.l.{1}/{2}', self.game_key, league_id, resource))
        self.yhandler.format = save_format
        if resp.status_code != requests.codes['ok']:
            return None
        return self.selector.parse(resp.content)
