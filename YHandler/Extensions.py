import lxml.etree
import requests
import re


"""
Other methods for retrieving sports related information
from Yahoo's network.
"""

def get_player_id(player_name, sport_code):
    """
    Uses Yahoo's player search to find player IDs according to the search criteria.
    NOTE: This query uses the player search outside of Yahoo's fantasy network, and may
    be unstable for continued use. Use with caution. You may want to also look at the find
    player in the YQuery class. It peforms the search within the fantasy API.
    :param: player_name - player name to search for
    :param: sport_code - sport abbreviation (I think) (e.g. nfl, nba, mlb, nhl)
    :returns: list of player IDs that can be used Yahoo fantasy API to query player resources (info, stats, etc...)
    """
    resp = requests.get(str.format('http://sports.yahoo.com/{0}/players', sport_code),
                        params={ 'type': 'lastname', 'first': '1', 'query': player_name})
    results = []
    if resp.status_code != requests.codes['ok']:
        return results
    selector = lxml.etree.fromstring(resp.content, lxml.etree.HTMLParser())
    player_ids = selector.xpath('//table/tr[contains(td,"Search Results")]/following::tr[position()>1]/td[1]//@href')
    if player_ids:
        for p in player_ids:
            id = re.search(r'\d+', p)
            if id:
                results.append(id.group(0))
    return results