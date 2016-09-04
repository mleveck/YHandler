from YHandler import YHandler
from YHandler import YQuery
import json

handler = YHandler('../auth.json')
query = YQuery(handler, 'nfl')
leagues = query.get_user_leagues()
# player = query.find_player(leagues[1]['id'], 'Tom Brady')
# stats = query.get_player_season_stats(player[0]['id'])
# f = open('stats.json', 'w')
# json.dump(stats, f)
# f.close()