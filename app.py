# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from nba_api.stats.static import *

'''

teamlist = teams.get_teams()
playerlist = players.get_players()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.RadioItems(
            id='teamplayer',
            options = [{'label': "Team", 'value': 'team'},
                       {'label': "Player", 'value': 'player'}],
            value = 'team'

    ),
    dcc.Dropdown(id='drop1', multi=True)
])

@app.callback(
Output('drop1', 'options'),
[Input('teamplayer', 'value')])
def setDropDown(selection):
    if selection == 'team':
        return [{'label': i['full_name'], 'value': i['id']} for i in teamlist]
    else:
        return  [{'label': i['full_name'], 'value': i['id']} for i in playerlist]





if __name__ == '__main__':
    app.run_server(debug=True)
'''