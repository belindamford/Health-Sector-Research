import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load your dataset
df = pd.read_csv("C:/Users/belin/PycharmProjects/Population Health/PBS/PBS_all_fin_year.csv")
df.columns = df.columns.str.strip()  # Clean up column names
df['FY24 All'] = df['FY24 All'].replace(',', '', regex=True).astype(int)
df['FY24 change'] = df['FY24 change'].replace(',', '', regex=True).astype(int)

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("PBS Dashboard", style={'textAlign': 'center'}),

    # Filters (Slicers)
    html.Div([
        html.Label("Select Medication Type:"),
        dcc.Dropdown(
            id='medication-type',
            options=[{'label': 'All', 'value': 'All'}] +
                    [{'label': mt, 'value': mt} for mt in df['Medication_Type'].unique()],
            value='All'
        ),

        html.Label("Select GCCSA Name:"),
        dcc.Dropdown(
            id='gccsa-name',
            options=[{'label': 'All', 'value': 'All'}] +
                    [{'label': g, 'value': g} for g in df['GCCSA_NAME_2021'].unique()],
            value='All'
        ),

        html.Label("Select State:"),
        dcc.Dropdown(
            id='state',
            options=[{'label': 'All', 'value': 'All'}] +
                    [{'label': s, 'value': s} for s in df['State'].unique()],
            value='All'
        ),

        html.Label("Select LGA:"),
        dcc.Dropdown(
            id='lga-name',
            options=[{'label': 'All', 'value': 'All'}] +
                    [{'label': l, 'value': l} for l in df['LGA_Name'].unique()],
            value='All'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'}),

    # Bar charts
    html.Div([
        dcc.Graph(id='bar-chart-1'),
        dcc.Graph(id='bar-chart-2'),
    ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'})
])


# Callback for interactive filtering and chart updates
@app.callback(
    [Output('bar-chart-1', 'figure'),
     Output('bar-chart-2', 'figure')],
    [Input('medication-type', 'value'),
     Input('gccsa-name', 'value'),
     Input('state', 'value'),
     Input('lga-name', 'value')]
)
def update_charts(medication_type, gccsa_name, state, lga_name):
    # Filter data based on slicers
    filtered_df = df.copy()
    if medication_type != 'All':
        filtered_df = filtered_df[filtered_df['Medication_Type'] == medication_type]
    if gccsa_name != 'All':
        filtered_df = filtered_df[filtered_df['GCCSA_NAME_2021'] == gccsa_name]
    if state != 'All':
        filtered_df = filtered_df[filtered_df['State'] == state]
    if lga_name != 'All':
        filtered_df = filtered_df[filtered_df['LGA_Name'] == lga_name]

    # Total PBS Scripts by GCCSA
    data1 = filtered_df.groupby('GCCSA_NAME_2021')['FY24 All'].sum().reset_index().sort_values(by='FY24 All',
                                                                                               ascending=False)
    fig1 = px.bar(data1, x='GCCSA_NAME_2021', y='FY24 All', title="Total PBS Scripts by GCCSA")

    # Change in PBS Scripts by GCCSA
    data2 = filtered_df.groupby('GCCSA_NAME_2021')['FY24 change'].sum().reset_index().sort_values(by='FY24 change',
                                                                                                  ascending=False)
    fig2 = px.bar(data2, x='GCCSA_NAME_2021', y='FY24 change', title="Change in PBS Scripts by GCCSA")

    return fig1, fig2


# Export charts to HTML
fig1.write_html("pbs_total_by_gccsa.html")
fig2.write_html("pbs_change_by_gccsa.html")