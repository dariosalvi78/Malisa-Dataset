import dash
from dash import dcc, html, Input, Output, ctx, State
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)

# Initialisation de la liste des coordonnées
coordinates =  {'DS':{
            '1':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}
            }}}

start = 1698411735

participant = 'DS'

num_test = 1

n_t='1'

acc_back = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_back_motion_{num_test}.csv')
acc_back['s'] = acc_back['timestamp']-start

fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGx'], mode='lines', name='Acceleration X'))
fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGy'], mode='lines', name='Acceleration Y'))
fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGz'], mode='lines', name='Acceleration Z'))

fig1.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Back Phone',
    xaxis_title='Time (sec)',
    yaxis_title='Acceleration (with G) (m/s^2)',
    legend=dict(x=0, y=1, traceorder='normal'))

acc_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_motion_{num_test}.csv')
acc_hand['s'] = acc_hand['timestamp']-start

fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGx'], mode='lines', name='Acceleration X'))
fig2.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGy'], mode='lines', name='Acceleration Y'))
fig2.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGz'], mode='lines', name='Acceleration Z'))

fig2.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
    xaxis_title='Time (sec)',
    yaxis_title='Acceleration (with G) (m/s^2)',
    legend=dict(x=0, y=1, traceorder='normal'))

id_graphs = ["DS_1_acc_back", "DS_1_acc_hand"]

app.layout = html.Div([
    html.Div([
    dcc.Graph(
        id='DS_1_acc_back',
        figure=fig1
    ),
    dcc.Graph(
        id='DS_1_acc_hand',
        figure=fig2
    )],id='graph'),
    html.Div(id='click-output')
])


@app.callback(
    Output("click-output", "children"),
    [Input(t, "clickData") for t in id_graphs],
)
def display_click_data(*vals):
    if vals[0]==None and vals[1]==None:
        return ''

    else :
        ide = ctx.triggered[0]['prop_id'].split('.')[0]
        ind =  id_graphs.index(ide)
        clickData = vals[ind]
        if clickData != None :
            # Récupération des coordonnées du clic

            print(id)
            ide = list(ide)
            participant = ide[:2]
            participant = ''.join(participant)
            n_t = ide[3]
            device = ide[5:]
            device = ''.join(device)

            x = clickData['points'][0]['x']
            y = clickData['points'][0]['y']

            # Récupération du nom de la courbe sur laquelle le clic a eu lieu
            curve_name = clickData['points'][0]['curveNumber']

            # Enregistrement des coordonnées dans la liste correspondante
            if curve_name==0:
                if (x,y) not in coordinates[participant][n_t][device]['x'] :
                    coordinates[participant][n_t][device]['x'].append((x, y))
            if curve_name==1:
                if (x,y) not in coordinates[participant][n_t][device]['y'] :
                    coordinates[participant][n_t][device]['y'].append((x, y))
            if curve_name==2:
                if (x,y) not in coordinates[participant][n_t][device]['z'] :
                    coordinates[participant][n_t][device]['z'].append((x, y))

            print(coordinates)



        # Affichage de la liste entière des coordonnées
        #output = []
        #for curve, coords in coordinates[participant][n_t][device].items() :
        #   output.append(html.Div([
        #       html.Div(f'Device : {device}'),
        #       html.Div(f'Coordonnées enregistrées sur {curve}:'),
        #       html.Ul([html.Li(f'x={coord[0]}, y={coord[1]}') for coord in coords])
        #   ]))

        #return output

        return ''




if __name__ == "__main__":
    app.run(debug=True)