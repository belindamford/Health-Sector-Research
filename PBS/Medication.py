import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Load your dataset
df = pd.read_csv("C:/Users/belin/PycharmProjects/Population Health/PBS/PBS_all_fin_year.csv")
df.columns = df.columns.str.strip()  # Clean up column names
df['FY24 All'] = df['FY24 All'].replace(',', '', regex=True).astype(int)
df['FY24 change'] = df['FY24 change'].replace(',', '', regex=True).astype(int)

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("PBS Dashboard", style={'textAlign': 'center'}),

    # Slicers (Dropdowns)
    html.Div([
        html.Div([
            html.Label("Select Medication Type:"),
            dcc.Dropdown(
                id='medication-slicer',
                options=[{'label': 'All', 'value': 'All'}] +
                        [{'label': mt, 'value': mt} for mt in df['Medication_Type'].unique()],
                value='All',
                clearable=False,
                style={'font-size': '12px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label("Select GCCSA Name:"),
            dcc.Dropdown(
                id='gccsa-slicer',
                options=[{'label': 'All', 'value': 'All'}] +
                        [{'label': gc, 'value': gc} for gc in df['GCCSA_NAME_2021'].unique()],
                value='All',
                clearable=False,
                style={'font-size': '12px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label("Select State:"),
            dcc.Dropdown(
                id='state-slicer',
                options=[{'label': 'All', 'value': 'All'}] +
                        [{'label': st, 'value': st} for st in df['State'].unique()],
                value='All',
                clearable=False,
                style={'font-size': '12px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '10px 0'}),

    # Charts Row 1: Two Medication Type charts
    html.Div([
        html.Div([
            dcc.Graph(id='chart-5')  # Total PBS Scripts by Medication Type
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        html.Div([
            dcc.Graph(id='chart-6')  # Change in PBS Scripts by Medication Type
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    # Charts Row 2: Two GCCSA charts
    html.Div([
        html.Div([
            dcc.Graph(id='chart-1')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        html.Div([
            dcc.Graph(id='chart-2')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    # Charts Row 3: Two LGA charts
    html.Div([
        html.Div([
            dcc.Graph(id='chart-3')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        html.Div([
            dcc.Graph(id='chart-4')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
])

# Helper function to filter data
def filter_data(medication_type, gccsa_name, state):
    filtered_df = df
    if medication_type != 'All':
        filtered_df = filtered_df[filtered_df['Medication_Type'] == medication_type]
    if gccsa_name != 'All':
        filtered_df = filtered_df[filtered_df['GCCSA_NAME_2021'] == gccsa_name]
    if state != 'All':
        filtered_df = filtered_df[filtered_df['State'] == state]
    return filtered_df

# Callbacks
@app.callback(
    [Output('chart-1', 'figure'),
     Output('chart-2', 'figure'),
     Output('chart-3', 'figure'),
     Output('chart-4', 'figure'),
     Output('chart-5', 'figure'),
     Output('chart-6', 'figure')],
    [Input('medication-slicer', 'value'),
     Input('gccsa-slicer', 'value'),
     Input('state-slicer', 'value')]
)
def update_charts(medication_type, gccsa_name, state):
    # Filter the data based on slicers
    filtered_df = filter_data(medication_type, gccsa_name, state)

    # Chart 1: FY24 Total PBS Scripts by GCCSA
    chart_data_1 = filtered_df.groupby('GCCSA_NAME_2021')['FY24 All'].sum().reset_index().sort_values(by='FY24 All', ascending=False)
    fig1 = go.Figure(data=go.Bar(
        x=chart_data_1['GCCSA_NAME_2021'],
        y=chart_data_1['FY24 All'],
        name="Total PBS Scripts"
    ))
    fig1.update_layout(title="Total PBS Scripts by GCCSA")

    # Chart 2: Change in PBS Scripts by GCCSA
    chart_data_2 = filtered_df.groupby('GCCSA_NAME_2021')['FY24 change'].sum().reset_index().sort_values(by='FY24 change', ascending=False)
    fig2 = go.Figure(data=go.Bar(
        x=chart_data_2['GCCSA_NAME_2021'],
        y=chart_data_2['FY24 change'],
        name="Change in PBS Scripts"
    ))
    fig2.update_layout(title="Change in PBS Scripts by GCCSA")

    # Chart 3: Total PBS Scripts by LGA
    chart_data_3 = filtered_df.groupby('LGA_Name')['FY24 All'].sum().reset_index().sort_values(by='FY24 All', ascending=False)
    fig3 = go.Figure(data=go.Bar(
        x=chart_data_3['LGA_Name'],
        y=chart_data_3['FY24 All'],
        name="Total PBS Scripts"
    ))
    fig3.update_layout(title="Total PBS Scripts by LGA")

    # Chart 4: Change in PBS Scripts by LGA
    chart_data_4 = filtered_df.groupby('LGA_Name')['FY24 change'].sum().reset_index().sort_values(by='FY24 change', ascending=False)
    fig4 = go.Figure(data=go.Bar(
        x=chart_data_4['LGA_Name'],
        y=chart_data_4['FY24 change'],
        name="Change in PBS Scripts"
    ))
    fig4.update_layout(title="Change in PBS Scripts by LGA")

    # Chart 5: Total PBS Scripts by Medication Type
    chart_data_5 = filtered_df.groupby('Medication_Type')['FY24 All'].sum().reset_index().sort_values(by='FY24 All', ascending=False)
    fig5 = go.Figure(data=go.Bar(
        x=chart_data_5['Medication_Type'],
        y=chart_data_5['FY24 All'],
        name="Total PBS Scripts"
    ))
    fig5.update_layout(title="Total PBS Scripts by Medication Type",
                       xaxis=dict(tickangle=-45, title_font=dict(size=10)))

    # Chart 6: Change in PBS Scripts by Medication Type
    chart_data_6 = filtered_df.groupby('Medication_Type')['FY24 change'].sum().reset_index().sort_values(by='FY24 change', ascending=False)
    fig6 = go.Figure(data=go.Bar(
        x=chart_data_6['Medication_Type'],
        y=chart_data_6['FY24 change'],
        name="Change in PBS Scripts"
    ))
    fig6.update_layout(title="Change in PBS Scripts by Medication Type",
                       xaxis=dict(tickangle=-45, title_font=dict(size=10)))

    return fig1, fig2, fig3, fig4, fig5, fig6

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8050)

