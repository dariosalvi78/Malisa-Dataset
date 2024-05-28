import dash
from dash import Dash,dcc, html, Input, Output, State, ctx
import pandas as pd
import plotly.graph_objs as go
import webbrowser
import tkinter as tk
import threading


details_csv = pd.read_excel('Details_CSV.xlsx', header=0)

ts = pd.read_csv('TS_sec.csv')

## Plot acceleration

def plot_acc(participant, num_test, test_name):
    df = {}
    id = []

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_back_motion_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        acc_back = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_back_motion_{num_test}.csv')
        acc_back['s'] = acc_back['timestamp']-start
        df['acc_back']=acc_back

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_accel_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        acc_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_accel_{num_test}.csv')
        acc_bangle['s'] = acc_bangle['timestamp']-start
        df['acc_bangle']=acc_bangle

    bool3 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_motion_{num_test}.csv']
    bool3.reset_index(drop=True, inplace=True)
    if bool3['empty ? '][0] == 'No':
        acc_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_motion_{num_test}.csv')
        acc_hand['s'] = acc_hand['timestamp']-start
        df['acc_hand']=acc_hand

    bool4 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_msafety_acc_{num_test}.csv']
    bool4.reset_index(drop=True, inplace=True)
    if bool4['empty ? '][0] == 'No':
        acc_msafety = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_msafety_acc_{num_test}.csv')
        acc_msafety['s'] = acc_msafety['timestamp']-start
        df['acc_msafety']=acc_msafety

    if df :
        fig = []
        for key in df :

            if key == 'acc_back':

                fig1 = go.Figure()

                fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGx'], mode='lines', name='Acceleration X'))
                fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGy'], mode='lines', name='Acceleration Y'))
                fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGz'], mode='lines', name='Acceleration Z'))

                fig1.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Back Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration (with G) (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                id.append(f'{participant}_{num_test}_acc_back')

            elif key == 'acc_bangle':

                fig2 = go.Figure()

                fig2.add_trace(go.Scatter(x=acc_bangle['s'], y=acc_bangle['accGGx'], mode='lines', name='Acceleration X'))
                fig2.add_trace(go.Scatter(x=acc_bangle['s'], y=acc_bangle['accGGy'], mode='lines', name='Acceleration Y'))
                fig2.add_trace(go.Scatter(x=acc_bangle['s'], y=acc_bangle['accGGz'], mode='lines', name='Acceleration Z'))

                fig2.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration (g)',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig2)
                id.append(f'{participant}_{num_test}_acc_bangle')

            elif key == 'acc_hand':

                fig3 = go.Figure()

                fig3.add_trace(go.Scatter(x=acc_hand['s'], y=acc_hand['accGx'], mode='lines', name='Acceleration X'))
                fig3.add_trace(go.Scatter(x=acc_hand['s'], y=acc_hand['accGy'], mode='lines', name='Acceleration Y'))
                fig3.add_trace(go.Scatter(x=acc_hand['s'], y=acc_hand['accGz'], mode='lines', name='Acceleration Z'))

                fig3.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration (with G) (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig3)
                id.append(f'{participant}_{num_test}_acc_hand')

            elif key == 'acc_msafety':

                fig4 = go.Figure()

                fig4.add_trace(go.Scatter(x=acc_msafety['s'], y=acc_msafety['accGx'], mode='lines', name='Acceleration X'))
                fig4.add_trace(go.Scatter(x=acc_msafety['s'], y=acc_msafety['accGy'], mode='lines', name='Acceleration Y'))
                fig4.add_trace(go.Scatter(x=acc_msafety['s'], y=acc_msafety['accGz'], mode='lines', name='Acceleration Z'))

                fig4.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Msafety',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration (with G) (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig4)
                id.append(f'{participant}_{num_test}_acc_msafety')

        if len(fig)>0:
            return html.Div([
                html.H2(f"Acceleration for {participant} in {test_name}.")]
                +[dcc.Graph(id=i, figure=f, style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}) for i, f in zip(id,fig)]
            ),fig,id

    else:
        return html.Div([
                html.H2(f"Acceleration for {participant} in {test_name}."),
                dcc.Markdown('Metric not available for this participant and this test.')
            ]), [], []


## Plot rotation

def plot_rot(participant, num_test,test_name):
    df = {}
    id = []

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_back_orientation_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        rot_back = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_back_orientation_{num_test}.csv')
        rot_back['s'] = rot_back['timestamp']-start
        df['rot_back']=rot_back

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_compass_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        rot_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_compass_{num_test}.csv')
        rot_bangle['s'] = rot_bangle['timestamp']-start
        df['rot_bangle']=rot_bangle

    bool3 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_orientation_{num_test}.csv']
    bool3.reset_index(drop=True, inplace=True)
    if bool3['empty ? '][0] == 'No':
        rot_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_orientation_{num_test}.csv')
        rot_hand['s'] = rot_hand['timestamp']-start
        df['rot_hand']=rot_hand

    if df :
        fig = []
        for key in df :

            if key == 'rot_back':

                fig1 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig1.add_trace(go.Scatter(x=rot_back['s'], y=rot_back['alpha'], mode='lines', name='Alpha'))
                fig1.add_trace(go.Scatter(x=rot_back['s'], y=rot_back['beta'], mode='lines', name='Beta'))
                fig1.add_trace(go.Scatter(x=rot_back['s'], y=rot_back['gamma'], mode='lines', name='Gamma'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Back Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                id.append(f'{participant}_{num_test}_rot_back')

            elif key == 'rot_bangle':

                fig2 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig2.add_trace(go.Scatter(x=rot_bangle['s'], y=rot_bangle['magnRawx'], mode='lines', name='magnRawx'))
                fig2.add_trace(go.Scatter(x=rot_bangle['s'], y=rot_bangle['magnRawy'], mode='lines', name='magnRawy'))
                fig2.add_trace(go.Scatter(x=rot_bangle['s'], y=rot_bangle['magnRawz'], mode='lines', name='magnRawy'))

                # Mettre à jour la disposition de la figure
                fig2.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (sec)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig2)
                id.append(f'{participant}_{num_test}_rot_bangle')


            elif key == 'rot_hand':

                fig3 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig3.add_trace(go.Scatter(x=rot_hand['s'], y=rot_hand['alpha'], mode='lines', name='Alpha'))
                fig3.add_trace(go.Scatter(x=rot_hand['s'], y=rot_hand['beta'], mode='lines', name='Beta'))
                fig3.add_trace(go.Scatter(x=rot_hand['s'], y=rot_hand['gamma'], mode='lines', name='Gamma'))

                # Mettre à jour la disposition de la figure
                fig3.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig3)
                id.append(f'{participant}_{num_test}_rot_hand')

        if len(fig)>0:
            return html.Div([
                html.H2(f"Rotation for {participant} in {test_name}.")]
                +[dcc.Graph(id=i, figure=f, style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}) for i, f in zip(id,fig)]
            ),fig,id

    else :
        return html.Div([
                html.H2(f"Rotation for {participant} in {test_name}."),
                dcc.Markdown('Metric not available for this participant and this test.')
            ]),[],[]



## Plot ppg

def plot_ppg(participant, num_test,test_name):
    df = {}
    id = []

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_msafety_ppg_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        ppg = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_msafety_ppg_{num_test}.csv')
        ppg['s'] = ppg['timestamp']-start
        df['ppg']=ppg

    if df :
        fig = []

        for key in df :

            if key == 'ppg':

                fig1 = go.Figure()

                fig1.add_trace(go.Scatter(x=ppg['s'], y=ppg['ppg'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'PPG - Participant: {participant}, Test: {num_test}, Device: Msafety',
                    xaxis_title='Time (sec)',
                    yaxis_title='PPG',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                id.append(f'{participant}_{num_test}_ppg_msafety')

        if len(fig)==1:
            return html.Div([
                html.H2(f"PPG for {participant} in {test_name}."),
                dcc.Graph(id=f'{participant}_{num_test}_ppg_msafety', figure=fig[0], style={'width': '50%', 'height': '50vh', 'display': 'inline-block'})
            ]),fig,id

    else :
        return html.Div([
                html.H2(f"PPG for {participant} in {test_name}."),
                dcc.Markdown('Metric not available for this participant and this test.')
            ]),[],[]


## Plot hr

def plot_hr(participant, num_test,test_name):
    df = {}
    id = []

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_hr_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        hr = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_hr_{num_test}.csv')
        hr['s'] = hr['timestamp']-start
        df['hr']=hr

    if df :
        fig=[]
        for key in df :

            if key == 'hr':

                fig1 = go.Figure()

                fig1.add_trace(go.Scatter(x=hr['s'], y=hr['hr'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Heart Rate - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (sec)',
                    yaxis_title='Heart Rate',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                id.append(f'{participant}_{num_test}_hr_bangle')

        if len(fig)==1:
            return html.Div([
                html.H2(f"Heart-Rate for {participant} in {test_name}."),
                dcc.Graph(id=f'{participant}_{num_test}_hr_bangle', figure=fig[0], style={'width': '50%', 'height': '50vh', 'display': 'inline-block'})
            ]),fig,id

    else :
        return html.Div([
                html.H2(f"Heart-Rate for {participant} in {test_name}."),
                dcc.Markdown('Metric not available for this participant and this test.')
            ]),[],[]


## Plot steps

def plot_step(participant,num_test, test_name):
    df = {}
    id = []

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_steps_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        steps_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_steps_{num_test}.csv')
        steps_bangle['s'] = steps_bangle['timestamp']-start
        df['steps_bangle']=steps_bangle

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_cadence_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        steps_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_cadence_{num_test}.csv')
        steps_hand['s'] = steps_hand['timestamp']-start
        df['steps_hand']=steps_hand

    if df :
        fig=[]
        for key in df :

            if key == 'steps_bangle':

                fig1 = go.Figure()

                fig1.add_trace(go.Scatter(x=steps_bangle['s'], y=steps_bangle['steps'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Step - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (sec)',
                    yaxis_title='Step',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                id.append(f'{participant}_{num_test}_step_bangle')


            elif key == 'steps_hand':

                fig2 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig2.add_trace(go.Scatter(x=steps_hand['s'], y=steps_hand['instantaneousSpeed'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig2.update_layout(title=f'Speed - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Speed',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig2)
                id.append(f'{participant}_{num_test}_speed_hand')

                fig3 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig3.add_trace(go.Scatter(x=steps_hand['s'], y=steps_hand['instantaneousCadence'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig3.update_layout(title=f'Step - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Step',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig3)
                id.append(f'{participant}_{num_test}_step_hand')

                fig4 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig4.add_trace(go.Scatter(x=steps_hand['s'], y=steps_hand['instantaneousStrideLength'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig4.update_layout(title=f'Stride Length - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Stride Length',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig4)
                id.append(f'{participant}_{num_test}_stride_hand')

        if len(fig)>0:
            return html.Div([
                html.H2(f"Step for {participant} in {test_name}.")]
                +[dcc.Graph(id=i, figure=f, style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}) for i, f in zip(id,fig)]
            ),fig,id

    else :
        return html.Div([
                html.H2(f"Step for {participant} in {test_name}."),
                dcc.Markdown('Metric not available for this participant and this test.')
            ]),[],[]


## main
class DashThread(threading.Thread):
    def __init__(self, data_list):
        threading.Thread.__init__(self)
        self.data_list = data_list

        self.app = Dash(__name__)

        existing_graphs = []
        graphs = []
        id_graphs = []

        coordinates =  {'DS':{
                    '1':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '2':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '3':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '4':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '5':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '6':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '7':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '8':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '9':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '10':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]}
                    },
                    'DL':{
                    '1':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '2':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '3':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '4':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '5':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '6':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '7':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '8':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '9':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '10':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]}
                    },
                    'MB':{
                    '1':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '2':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '3':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '4':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '5':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '6':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '7':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '8':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '9':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '10':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]}
                    },
                    'RC':{
                    '1':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '2':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '3':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '4':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '5':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '6':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '7':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '8':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '9':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '10':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]}
                    },
                    'PB':{
                    '1':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '2':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '3':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '4':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '5':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '6':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '7':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '8':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '9':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '10':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]}
                    },
                    'LC':{
                    '1':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '2':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '3':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '4':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '5':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '6':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '7':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '8':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '9':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]},
                    '10':{'acc_back':{'x':[], 'y':[], 'z':[]}, 'acc_hand':{'x':[], 'y':[], 'z':[]}, 'acc_bangle':{'x':[], 'y':[], 'z':[]}, 'acc_msafety':{'x':[], 'y':[], 'z':[]}, 'rot_back':{'a':[], 'b':[], 'g':[]}, 'rot_bangle':{'a':[], 'b':[], 'g':[]}, 'rot_hand':{'a':[], 'b':[], 'g':[]}, 'ppg_msafety':[], 'hr_bangle':[], 'step_bangle':[], 'step_hand':[], 'speed_hand':[], 'stride_hand':[]}
                    }
                }

        # Données
        participants = ['DS', 'DL', 'MB', 'RC', 'PB', 'LC']
        tests = ['TUG 1','TUG 2','TUG slow 1','TUG slow 2','30CST','Locomo','10MWT 1','10MWT 2','partial 6MWT 1','partial 6MWT 2']
        metrics = ["All","Acceleration", "Rotation","PPG", "Heart Rate", "Step"]

        # Création de la liste déroulante pour la sélection du participant
        dropdown_participant = dcc.Dropdown(
            id='dropdown-participant',
            options=[{'label': participant, 'value': participant} for participant in participants],
            value=None
        )

        # Création de la liste déroulante pour la sélection du test
        dropdown_test = dcc.Dropdown(
            id='dropdown-test',
            options=[{'label': test, 'value': test} for test in tests],
            value=None
        )

        # Création de la liste déroulante pour la sélection de la métrique
        dropdown_metric = dcc.Dropdown(
            id='dropdown-metric',
            options=[{'label': metric, 'value': metric} for metric in metrics],
            value=None
        )

        # Création du bouton d'ajout
        add_button = html.Button('Add', id='add-button', n_clicks=0)

        # Création du conteneur pour les graphiques
        graph_container = html.Div(id='graph-container')

        graph_container2 = html.Div(id='graph-container2')

        # Création d'un bouton pour vider la page
        clear_button = html.Button('Clear', id='clear-button')

        # Mise en page de l'application
        self.app.layout = html.Div([
            html.H1("Data vizualisation"),
            html.Div([
                html.Label('Participant'),
                dropdown_participant,
                html.Label('Test'),
                dropdown_test,
                html.Label('Metric'),
                dropdown_metric
            ], id='selection-form'),
            add_button,
            clear_button,
            graph_container
        ])

        @self.app.callback(
            Output('graph-container', 'children'),
            Input('add-button','n_clicks'),
            Input('clear-button','n_clicks'),
            [State('dropdown-participant', 'value'),
            State('dropdown-test', 'value'),
            State('dropdown-metric', 'value')]
        )

        def update_graphs(add_clicks, clear_clicks, participant, test, metric):

            if 'clear-button'==ctx.triggered_id :
                existing_graphs.clear()
                graphs.clear()
                id_graphs.clear()
                return dcc.Markdown('Choose a participant, a test and a metric.')

            if add_clicks==0:
                if participant is None or test is None or metric is None:
                    return dcc.Markdown('Choose a participant, a test and a metric.')

            if participant is None or test is None or metric is None:
                return dcc.Markdown('Choose a participant, a test and a metric.')

            if test == 'TUG 1' :
                t = 1
            elif test == 'TUG 2':
                t = 2
            elif test == 'TUG slow 1':
                t = 3
            elif test == 'TUG slow 2':
                t = 4
            elif test == '30CST':
                t=5
            elif test == 'Locomo':
                t=6
            elif test == '10MWT 1':
                t=7
            elif test == '10MWT 2':
                t=8
            elif test == 'partial 6MWT 1':
                t=9
            elif test == 'partial 6MWT 2':
                t=10

            if metric == 'All':
                d,g,ig = plot_acc(participant,t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                d,g,ig = plot_rot(participant, t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                d,g,ig = plot_ppg(participant, t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                d,g,ig = plot_hr(participant, t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                d,g,ig = plot_step(participant, t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                return existing_graphs

            if metric == 'Acceleration':
                d,g,ig = plot_acc(participant,t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                return existing_graphs

            if metric == 'Rotation':
                d,g,ig = plot_rot(participant, t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                return existing_graphs

            if metric == 'PPG':
                d,g,ig = plot_ppg(participant, t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                return existing_graphs

            if metric == 'Heart Rate':
                d,g,ig = plot_hr(participant, t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                return existing_graphs

            if metric == 'Step':
                d,g,ig = plot_step(participant, t,test)
                existing_graphs.append(d)
                graphs.extend(g)
                id_graphs.extend(ig)
                return existing_graphs

        # @self.app.callback(
        #     Output('graph-container2', 'children'),
        #     [Input(t, "clickData") for t in id_graphs]
        # )
        # def display_click_data(input_value,*vals):
        #
        #     if id_graphs :
        #         if all(element is None for element in vals) :
        #             raise dash.exceptions.PreventUpdate
        #
        #         else :
        #             id = ctx.triggered[0]['prop_id'].split('.')[0]
        #             ind =  id_graphs.index(id)
        #             clickData = vals[ind]
        #             if clickData != None :
        #
        #                 id = list(id)
        #                 participant = id[:2]
        #                 participant = ''.join(participant)
        #                 n_t = id[3]
        #                 device = id[5:]
        #                 device = ''.join(device)
        #
        #                 # Récupération des coordonnées du clic
        #                 x = clickData['points'][0]['x']
        #                 y = clickData['points'][0]['y']
        #
        #                 # Récupération du nom de la courbe sur laquelle le clic a eu lieu
        #                 curve_name = clickData['points'][0]['curveNumber']
        #
        #                 # Enregistrement des coordonnées dans la liste correspondante
        #                 if curve_name==0:
        #                     if (x,y) not in coordinates[participant][n_t][device]['x'] :
        #                         coordinates[participant][n_t][device]['x'].append((x, y))
        #                 if curve_name==1:
        #                     if (x,y) not in coordinates[participant][n_t][device]['y'] :
        #                         coordinates[participant][n_t][device]['y'].append((x, y))
        #                 if curve_name==2:
        #                     if (x,y) not in coordinates[participant][n_t][device]['z'] :
        #                         coordinates[participant][n_t][device]['z'].append((x, y))
        #             print(coordinates)
        #             return existing_graphs
        #
        #     else:
        #         return existing_graphs

    def run(self):
        self.app.run_server(debug=False,port=8075)



class App:
    def __init__(self, root):
        self.root = root
        self.data_list = {"ETHUSDT": [], "BTCUSD": [], "BNBUSDT": []}

        # Start the Dash application in a separate thread
        dash_thread = DashThread(self.data_list)
        dash_thread.start()

        # Open Dash app in web browser
        webbrowser.open("http://localhost:8075")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)


