#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from nba_api.stats.static import *
import nba

teamlist = teams.get_teams()
playerlist = players.get_players()
clicks = 0

team_stats = [
    'TEAM_ID',
    'TEAM_CITY',
    'TEAM_NAME',
    'YEAR',
    'GP',
    'WINS',
    'LOSSES',
    'WIN_PCT',
    'CONF_RANK',
    'DIV_RANK',
    'PO_WINS',
    'PO_LOSSES',
    'CONF_COUNT',
    'DIV_COUNT',
    'NBA_FINALS_APPEARANCE',
    'FGM',
    'FGA',
    'FG_PCT',
    'FG3M',
    'FG3A',
    'FG3_PCT',
    'FTM',
    'FTA',
    'FT_PCT',
    'OREB',
    'DREB',
    'REB',
    'AST',
    'PF',
    'STL',
    'TOV',
    'BLK',
    'PTS',
    'PTS_RANK',
    ]

player_stats = [
    'PLAYER_ID',
    'SEASON_ID',
    'LEAGUE_ID',
    'TEAM_ID',
    'TEAM_ABBREVIATION',
    'PLAYER_AGE',
    'GP',
    'GS',
    'MIN',
    'FGM',
    'FGA',
    'FG_PCT',
    'FG3M',
    'FG3A',
    'FG3_PCT',
    'FTM',
    'FTA',
    'FT_PCT',
    'OREB',
    'DREB',
    'REB',
    'AST',
    'STL',
    'BLK',
    'TOV',
    'PF',
    'PTS',
    ]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.RadioItems(id='teamplayer', options=[{'label': 'Team',
                   'value': 'team'}, {'label': 'Player',
                   'value': 'player'}], value='team',
                   labelStyle={'display': 'inline-block',
                   'margin-right': 10}),
    dcc.Dropdown(id='drop1', multi=False),
    dcc.Dropdown(id='drop2', multi=False),
    dcc.Dropdown(id='drop3', multi=False),
    dcc.Checklist(id='stats', labelStyle={'margin-right': '10',
                  'display': 'inline-block'}, values=[]),
    html.Button('Graph', id='graph_btn'),
    html.Div(id='container'),
    ])


@app.callback([Output('drop1', 'options'), Output('drop2', 'options'),
              Output('drop3', 'options'), Output('stats', 'options')],
              [Input('teamplayer', 'value')])
def setDropDown(selection):
    if selection == 'team':
        return ([{'label': i['full_name'], 'value': i['id']} for i in
                teamlist], [{'label': i['full_name'], 'value': i['id']}
                for i in teamlist], [{'label': i['full_name'],
                'value': i['id']} for i in teamlist], [{'label': i,
                'value': i} for i in team_stats])
    else:

        return ([{'label': i['full_name'], 'value': i['id']} for i in
                playerlist], [{'label': i['full_name'], 'value': i['id'
                ]} for i in playerlist], [{'label': i['full_name'],
                'value': i['id']} for i in playerlist], [{'label': i,
                'value': i} for i in player_stats])


@app.callback(Output('container', 'children'), [Input('graph_btn',
              'n_clicks'), Input('drop1', 'value'), Input('stats',
              'values'), Input('teamplayer', 'value')])
def graphStats(n_clicks, id, stat_list, teamplayer):
    global clicks
    if n_clicks == clicks or n_clicks is None:
        raise PreventUpdate
    else:
        clicks += 1
        if (teamplayer == 'team'):
            id1 = nba.Team(id)
        else:
            id1 = nba.Player(id)

        objects = [id1]
        graphs = []
        for j in stat_list:
            traces = []
            for i in objects:
                df = i.get_stats(j, '1975', '2020')
                traces.append(dict(x=str(df.index), y=df,
                              name=i.name))

                graphs.append(dcc.Graph(id=j, figure={'data': traces,
                              'layout': dict(xaxis={'title': 'Range'},
                              yaxis={'title': j}, title=j,
                              showlegend=True)}))

        return html.Div(graphs)
if __name__ == '__main__':
    app.run_server(debug=True)

