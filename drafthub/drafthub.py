import csv
import json
import os
import pdb

from yahoo_oauth import OAuth1
from myql import MYQL
from myql.utils import prettyfy as dump

from flask.json import jsonify
from flask import (
    Flask,
    render_template,
    request,
)

here = os.path.abspath(os.path.dirname(__file__))
app = Flask('drafthub')
state = None

QUERY_DRAFT_RESULTS = "select draft_results from fantasysports.draftresults where league_key='{}';"
QUERY_PLAYER_KEYS = "select * from fantasysports.players where player_key in ({});";
QUERY_TEAMS = "select * from fantasysports.teams where league_key='{}';"


class DraftState(object):
    def __init__(self, league_key, credentials='credentials.json'):
        oauth = OAuth1(None, None, from_file=credentials)
        self.yql = MYQL(format='json', oauth=oauth)

        self.last_pick = 0
        self.league_key = league_key

        self.teams = self._query(QUERY_TEAMS.format(self.league_key))['team']
        self.teams = { t['team_key']: t['name'] for t in self.teams }
        print(json.dumps(self.teams, indent=2))

        self.rosters = { name: [] for name in self.teams.values() }

    def _query(self, query):
        response = self.yql.raw_query(query)
        data = json.loads(response.content)
        return data['query']['results']

    def refresh(self):
        # TODO exclude known picks from query
        picks = self._query(QUERY_DRAFT_RESULTS.format(self.league_key))['league']['draft_results']['draft_result'][self.last_pick:]
        player_keys = []
        teams = []
        for p in picks:
            if 'player_key' in p and p['player_key']:
                player_keys.append("'{}'".format(p['player_key']))
                teams.append(self.teams[p['team_key']])
            else:
                self.last_pick = int(p['pick']) - 1
                break

        players = []

        if player_keys:
            players = self._query(QUERY_PLAYER_KEYS.format(', '.join(player_keys)))['player']
            if isinstance(players, dict):
                players = [players]

            players = [p['name']['full'] for p in players]

        return jsonify(picks=players, teams=teams)


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/draft', methods=['GET', 'POST'])
def draft():
    global state

    if request.method == 'POST':
        reader = csv.reader(request.files['csv_path'])
        lines = []
        for row in reader:
            lines.append(row)

        if request.form['game'] and request.form['league_id']:
            league_key = '{}.l.{}'.format(request.form['game'], request.form['league_id'])
            state = DraftState(league_key)

        header = lines.pop(0)
        for i, td in enumerate(header):
            if isinstance(td, basestring) and td.lower() in ('name', 'player'):
                player_index = i
                break
        else:
            player_index = None

        context = {
            'header': header,
            'players': lines,
            'player_index': player_index,
        }
        if state:
            context['teams'] = sorted(state.teams.values())
        return render_template('draft.html', **context)
    return render_template('upload.html')


@app.route('/_refresh')
def refresh():
    global state
    if state:
        return state.refresh()
    return ''


if __name__ == '__main__':
    app.run(debug=True)
