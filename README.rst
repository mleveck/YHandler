YHandler
========

Yahoo Fantasy Sports OAuth And Request Handler

This is the Python Script I use to access the Yahoo Fantasy Sports API via OAuth for my desktop app. It's still far from polished, and not the most generalized, but has been updated to work with newer version of the requests library. It should be okay with future versions of Requests as the OAuth support has been written specifically for Yahoo's OAuth 1.0a process, which allows refresh of the access token. It looks like they now also support OAuth 2.0, but still remain backward compatible with OAuth1.0a.


Installation
------------

You can install using `pip`::

	pip install YHandler


How To Use
-----------

Copy the auth.json.sample file and rename to auth.json and then place your consumer key, and consumer secret in the auth.json file.

::

	In [1]: from YHandler import YHandler, YQuery

	In [2]: handler = YHandler()

	In [3]: query = YQuery(handler, 'nfl')

	In [4]: query.get_games_info()
	Out[4]: 
	[{'code': 'nfl',
	  'key': '359',
	  'name': 'Football',
	  'season': '2016',
	  'type': '2016'}]

	In [5]: query.get_games_info(True)
	Out[5]: 
	[{'code': 'nfl',
	  'key': '359',
	  'name': 'Football',
	  'season': '2016',
	  'type': '2016'}]

	In [10]: query.get_user_leagues()
	Out[10]: 
	[{'id': '577090',
	  'is_finished': True,
	  'name': 'IniTeCh',
	  'season': '2015',
	  'week': '16'},
	 {'id': '126737',
	  'is_finished': False,
	  'name': 'Yahoo Public 126737',
	  'season': '2016',
	  'week': '1'}]

	In [17]: query.find_player(126737, 'antonio brown')
	Out[17]: [{'id': '24171', 'name': 'Antonio Brown', 'team': 'Pittsburgh Steelers'}]

	In [18]: query.get_player_week_stats(24171, '8')
	Out[18]: 
	{'0': {'detail': 'Games Played', 'name': 'GP', 'value': '0'},
	 '1': {'detail': 'Passing Attempts', 'name': 'Pass Att', 'value': '0'},
	 '10': {'detail': 'Rushing Touchdowns', 'name': 'Rush TD', 'value': '0'},
	 '11': {'detail': 'Receptions', 'name': 'Rec', 'value': '0'},
	 '12': {'detail': 'Reception Yards', 'name': 'Rec Yds', 'value': '0'},
	 '13': {'detail': 'Reception Touchdowns', 'name': 'Rec TD', 'value': '0'},
	 '14': {'detail': 'Return Yards', 'name': 'Ret Yds', 'value': '0'},
	 '15': {'detail': 'Return Touchdowns', 'name': 'Ret TD', 'value': '0'},
	 '16': {'detail': '2-Point Conversions', 'name': '2-PT', 'value': '0'},
	 '17': {'detail': 'Fumbles', 'name': 'Fum', 'value': '0'},
	 '18': {'detail': 'Fumbles Lost', 'name': 'Fum Lost', 'value': '0'},
	 '2': {'detail': 'Completions', 'name': 'Comp', 'value': '0'},
	 '3': {'detail': 'Incomplete Passes', 'name': 'Inc', 'value': '0'},
	 '4': {'detail': 'Passing Yards', 'name': 'Pass Yds', 'value': '0'},
	 '5': {'detail': 'Passing Touchdowns', 'name': 'Pass TD', 'value': '0'},
	 '57': {'detail': 'Offensive Fumble Return TD',
	  'name': 'Fum Ret TD',
	  'value': '0'},
	 '58': {'detail': 'Pick Sixes Thrown', 'name': 'Pick Six', 'value': '0'},
	 '59': {'detail': '40+ Yard Completions', 'name': '40 Yd Comp', 'value': '0'},
	 '6': {'detail': 'Interceptions', 'name': 'Int', 'value': '0'},
	 '60': {'detail': '40+ Yard Passing Touchdowns',
	  'name': '40 Yd Pass TD',
	  'value': '0'},
	 '61': {'detail': '40+ Yard Run', 'name': '40 Yd Rush', 'value': '0'},
	 '62': {'detail': '40+ Yard Rushing Touchdowns',
	  'name': '40 Yd Rush TD',
	  'value': '0'},
	 '63': {'detail': '40+ Yard Receptions', 'name': '40 Yd Rec', 'value': '0'},
	 '64': {'detail': '40+ Yard Reception Touchdowns',
	  'name': '40 Yd Rec TD',
	  'value': '0'},
	 '7': {'detail': 'Sacks', 'name': 'Sack', 'value': '0'},
	 '78': {'detail': 'Targets', 'name': 'Targets', 'value': '0'},
	 '79': {'detail': 'Passing 1st Downs', 'name': 'Pass 1st Downs', 'value': '0'},
	 '8': {'detail': 'Rushing Attempts', 'name': 'Rush Att', 'value': '0'},
	 '80': {'detail': 'Receiving 1st Downs',
	  'name': 'Rec 1st Downs',
	  'value': '0'},
	 '81': {'detail': 'Rushing 1st Downs', 'name': 'Rush 1st Downs', 'value': '0'},
	 '9': {'detail': 'Rushing Yards', 'name': 'Rush Yds', 'value': '0'}}



