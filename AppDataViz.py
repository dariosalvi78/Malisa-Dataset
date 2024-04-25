import dash
from dash import Dash,dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import webbrowser
import tkinter as tk
import threading

details_csv = pd.read_excel('Details_CSV.xlsx', header=0)

ts = pd.read_csv('TS.csv')

def plot_acc(participant, num_test):
    fig1={}
    fig2={}
    fig3={}
    fig4={}

    df = {}

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_back_motion_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        acc_back = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_back_motion_{num_test}.csv')
        acc_back['ms'] = acc_back['ts']-start
        df['acc_back']=acc_back

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_accel_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        acc_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_accel_{num_test}.csv')
        acc_bangle['ms'] = acc_bangle['ts']-start
        df['acc_bangle']=acc_bangle

    bool3 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_motion_{num_test}.csv']
    bool3.reset_index(drop=True, inplace=True)
    if bool3['empty ? '][0] == 'No':
        acc_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_motion_{num_test}.csv')
        acc_hand['ms'] = acc_hand['ts']-start
        df['acc_hand']=acc_hand

    bool4 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_msafety_acc_{num_test}.csv']
    bool4.reset_index(drop=True, inplace=True)
    if bool4['empty ? '][0] == 'No':
        acc_msafety = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_msafety_acc_{num_test}.csv')
        acc_msafety['ms'] = acc_msafety['ts']-start
        df['acc_msafety']=acc_msafety

    if df :
        for key in df :

            if key == 'acc_back':

                fig1 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig1.add_trace(go.Scatter(x=acc_back['ms'], y=acc_back['accGx'], mode='lines', name='Acceleration X'))
                fig1.add_trace(go.Scatter(x=acc_back['ms'], y=acc_back['accGy'], mode='lines', name='Acceleration Y'))
                fig1.add_trace(go.Scatter(x=acc_back['ms'], y=acc_back['accGz'], mode='lines', name='Acceleration Z'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Acceleration - Participant: {participant}, Test: {num_test}, Device: Back Phone',
                    xaxis_title='Time (ms)',
                    yaxis_title='Acceleration (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'))

            elif key == 'acc_bangle':

                fig2 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig2.add_trace(go.Scatter(x=acc_bangle['ms'], y=acc_bangle['accGx'], mode='lines', name='Acceleration X'))
                fig2.add_trace(go.Scatter(x=acc_bangle['ms'], y=acc_bangle['accGy'], mode='lines', name='Acceleration Y'))
                fig2.add_trace(go.Scatter(x=acc_bangle['ms'], y=acc_bangle['accGz'], mode='lines', name='Acceleration Z'))

                # Mettre à jour la disposition de la figure
                fig2.update_layout(title=f'Acceleration - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (ms)',
                    yaxis_title='Acceleration (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'))

            elif key == 'acc_hand':

                fig3 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig3.add_trace(go.Scatter(x=acc_hand['ms'], y=acc_hand['accGx'], mode='lines', name='Acceleration X'))
                fig3.add_trace(go.Scatter(x=acc_hand['ms'], y=acc_hand['accGy'], mode='lines', name='Acceleration Y'))
                fig3.add_trace(go.Scatter(x=acc_hand['ms'], y=acc_hand['accGz'], mode='lines', name='Acceleration Z'))

                # Mettre à jour la disposition de la figure
                fig3.update_layout(title=f'Acceleration - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (ms)',
                    yaxis_title='Acceleration (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'))

            elif key == 'acc_msafety':

                fig4 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig4.add_trace(go.Scatter(x=acc_msafety['ms'], y=acc_msafety['accGx'], mode='lines', name='Acceleration X'))
                fig4.add_trace(go.Scatter(x=acc_msafety['ms'], y=acc_msafety['accGy'], mode='lines', name='Acceleration Y'))
                fig4.add_trace(go.Scatter(x=acc_msafety['ms'], y=acc_msafety['accGz'], mode='lines', name='Acceleration Z'))

                # Mettre à jour la disposition de la figure
                fig4.update_layout(title=f'Acceleration - Participant: {participant}, Test: {num_test}, Device: Msafety',
                    xaxis_title='Time (ms)',
                    yaxis_title='Acceleration (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'))
    return fig1, fig2, fig3, fig4


def plot_rot(participant, num_test):
    fig1={}
    fig2={}
    fig3={}
    fig4={}

    df = {}

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_back_orientation_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        rot_back = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_back_orientation_{num_test}.csv')
        rot_back['ms'] = rot_back['ts']-start
        df['rot_back']=rot_back

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_compass_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        rot_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_compass_{num_test}.csv')
        rot_bangle['ms'] = rot_bangle['ts']-start
        df['rot_bangle']=rot_bangle

    bool3 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_orientation_{num_test}.csv']
    bool3.reset_index(drop=True, inplace=True)
    if bool3['empty ? '][0] == 'No':
        rot_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_orientation_{num_test}.csv')
        rot_hand['ms'] = rot_hand['ts']-start
        df['rot_hand']=rot_hand

    if df :
        for key in df :

            if key == 'rot_back':

                fig1 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig1.add_trace(go.Scatter(x=rot_back['ms'], y=rot_back['alpha'], mode='lines', name='Alpha'))
                fig1.add_trace(go.Scatter(x=rot_back['ms'], y=rot_back['beta'], mode='lines', name='Beta'))
                fig1.add_trace(go.Scatter(x=rot_back['ms'], y=rot_back['gamma'], mode='lines', name='Gamma'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Back Phone',
                    xaxis_title='Time (ms)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

            elif key == 'rot_bangle':

                fig2 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig2.add_trace(go.Scatter(x=rot_bangle['ms'], y=rot_bangle['alpha'], mode='lines', name='Alpha'))
                fig2.add_trace(go.Scatter(x=rot_bangle['ms'], y=rot_bangle['beta'], mode='lines', name='Beta'))
                fig2.add_trace(go.Scatter(x=rot_bangle['ms'], y=rot_bangle['gamma'], mode='lines', name='Gamma'))

                # Mettre à jour la disposition de la figure
                fig2.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (ms)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

            elif key == 'rot_hand':

                fig3 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig3.add_trace(go.Scatter(x=rot_hand['ms'], y=rot_hand['alpha'], mode='lines', name='Alpha'))
                fig3.add_trace(go.Scatter(x=rot_hand['ms'], y=rot_hand['beta'], mode='lines', name='Beta'))
                fig3.add_trace(go.Scatter(x=rot_hand['ms'], y=rot_hand['gamma'], mode='lines', name='Gamma'))

                # Mettre à jour la disposition de la figure
                fig3.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (ms)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

    return fig1, fig2, fig3, fig4


def plot_ppg(participant, num_test):
    fig1={}
    fig2={}
    fig3={}
    fig4={}

    df = {}

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_msafety_ppg_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        ppg = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_msafety_ppg_{num_test}.csv')
        ppg['ms'] = ppg['ts']-start
        df['ppg']=ppg

    if df :
        for key in df :

            if key == 'ppg':

                fig1 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig1.add_trace(go.Scatter(x=ppg['ms'], y=ppg['ppg'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'PPG - Participant: {participant}, Test: {num_test}, Device: Msafety',
                    xaxis_title='Time (ms)',
                    yaxis_title='PPG',
                    legend=dict(x=0, y=1, traceorder='normal'))

    return fig1, fig2, fig3, fig4


def plot_hr(participant, num_test):
    fig1={}
    fig2={}
    fig3={}
    fig4={}

    df = {}

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_hr_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        hr = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_hr_{num_test}.csv')
        hr['ms'] = hr['ts']-start
        df['hr']=hr

    if df :
        for key in df :

            if key == 'hr':

                fig1 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig1.add_trace(go.Scatter(x=hr['ms'], y=hr['hr'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Heart Rate - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (ms)',
                    yaxis_title='Heart Rate',
                    legend=dict(x=0, y=1, traceorder='normal'))

    return fig1, fig2, fig3, fig4


def plot_steps(participant,num_test):
    fig1={}
    fig2={}
    fig3={}
    fig4={}

    df = {}

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_steps_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        steps_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_steps_{num_test}.csv')
        steps_bangle['ms'] = steps_bangle['ts']-start
        df['steps_bangle']=steps_bangle

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_cadence_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        steps_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_cadence_{num_test}.csv')
        steps_hand['ms'] = steps_hand['ts']-start
        df['steps_hand']=steps_hand

    if df :
        for key in df :

            if key == 'steps_bangle':

                fig1 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig1.add_trace(go.Scatter(x=steps_bangle['ms'], y=steps_bangle['steps'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Cadence - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (ms)',
                    yaxis_title='Cadence',
                    legend=dict(x=0, y=1, traceorder='normal'))

            elif key == 'steps_hand':

                fig2 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig2.add_trace(go.Scatter(x=steps_hand['ms'], y=steps_hand['instantaneousSpeed'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig2.update_layout(title=f'Vitesse - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (ms)',
                    yaxis_title='Vitesse',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig3 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig3.add_trace(go.Scatter(x=steps_hand['ms'], y=steps_hand['instantaneousCadence'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig3.update_layout(title=f'Cadence - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (ms)',
                    yaxis_title='Cadence',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig4 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig4.add_trace(go.Scatter(x=steps_hand['ms'], y=steps_hand['instantaneousStrideLength'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig4.update_layout(title=f'Longueur des pas - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (ms)',
                    yaxis_title='Longueur des pas',
                    legend=dict(x=0, y=1, traceorder='normal'))

    return fig1, fig2, fig3, fig4


class DashThread(threading.Thread):
    def __init__(self, data_list):
        threading.Thread.__init__(self)
        self.data_list = data_list

        self.app = Dash(__name__)

        # Données
        participants = ['DS', 'DL', 'MB', 'RC', 'PB', 'LC']
        tests = ['1','2','3','4','5','6','7','8','9','10']
        metrics = ["Acceleration", "Rotation","PPG", "Heart Rate", "Cadence"]

        # Initialize
        self.app.layout = html.Div([
            html.H1("Visualisation de données"),

            # Menu déroulant pour sélectionner le participant
            dcc.Dropdown(
                id='participant-dropdown',
                options=[{'label': participant, 'value': participant} for participant in participants],
                value=None,
                placeholder="Sélectionner un participant"
            ),

            # Menu déroulant pour sélectionner le test
            dcc.Dropdown(
                id='test-dropdown',
                options=[{'label': test, 'value': test} for test in tests],
                value=None,
                placeholder="Sélectionner un test"
            ),

            # Menu déroulant pour sélectionner la métrique
            dcc.Dropdown(
                id='metric-dropdown',
                options=[{'label': metric, 'value': metric} for metric in metrics],
                value=None,
                placeholder="Sélectionner une métrique"
            ),

            # Bouton pour actualiser les graphiques
            html.Button('Actualiser', id='button', n_clicks=0),

            # Graphique 1
            dcc.Graph(id='graph1'),

            # Graphique 2
            dcc.Graph(id='graph2'),

            # Graphique 3
            dcc.Graph(id='graph3'),

            # Graphique 4
            dcc.Graph(id='graph4')
        ])

        @self.app.callback(
            [Output('graph1', 'figure'),
            Output('graph2', 'figure'),
            Output('graph3', 'figure'),
            Output('graph4', 'figure')],
            [Input('button', 'n_clicks')],
            [Input('participant-dropdown', 'value'),
            Input('test-dropdown', 'value'),
            Input('metric-dropdown', 'value')]
        )

        def update_graphs(n_clicks, participant, test, metric):

            # Vérifier si toutes les sélections sont faites
            if participant is None or test is None or metric is None:
                return {},{},{},{}

            # Charger les données correspondant aux sélections (à remplacer par vos propres données)
            if metric == 'Acceleration':
                figure1, figure2, figure3, figure4 = plot_acc(participant, test)

            if metric == 'Rotation':
                figure1, figure2, figure3, figure4 = plot_rot(participant, test)

            if metric == 'PPG':
                figure1, figure2, figure3, figure4 = plot_ppg(participant, test)

            if metric == 'Heart Rate':
                figure1, figure2, figure3, figure4 = plot_hr(participant, test)

            if metric == 'Cadence':
                figure1, figure2, figure3, figure4 = plot_steps(participant, test)

            return figure1, figure2, figure3, figure4

    def run(self):
        self.app.run_server(debug=False)



class App:
    def __init__(self, root):
        self.root = root
        self.data_list = {"ETHUSDT": [], "BTCUSD": [], "BNBUSDT": []}

        # Start the Dash application in a separate thread
        dash_thread = DashThread(self.data_list)
        dash_thread.start()

        # Open Dash app in web browser
        webbrowser.open("http://localhost:8050")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)


