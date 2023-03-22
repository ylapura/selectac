# This code is to run a simple dashboard to select aircraft

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

# Load the data
# acdata = pd.read_excel(r"https://github.com/ylapura/selectac/blob/main/AC%20Info%20for%20Niya_pivot.xlsx", sheet_name="DATA")
acdata = pd.read_excel("https://github.com/ylapura/selectac/blob/main/AC%20Info%20for%20Niya_pivot.xlsx?raw=true", sheet_name="DATA", engine="openpyxl")

acdata = acdata.sort_values('Age', ascending=False)

# Create the dropdown menu
subfleet = dcc.Dropdown(
    id='Subfleet',
    options=[{'label': x, 'value': x} for x in acdata['Subfleet'].unique()],
    value=acdata['Subfleet'].unique()[0]
)

# Create the data table
table_columns = [
    {'name': 'AC#', 'id': 'AC#'},
    {'name': 'Age', 'id': 'Age'},
    {'name': 'Retired', 'id': 'Retired'},
    {'name': 'Eng Type', 'id': 'Eng Type'},
    {'name': 'Etops', 'id': 'Etops'}
]
table_data = []
table = dash_table.DataTable(
    id='table',
    columns=table_columns,
    data=table_data,
    sort_action='native',
    filter_action='native',
    page_action='native',
    page_size=20,
    export_format='xlsx',
    export_headers='display'
)

# Create the app layout
app_layout = html.Div(children=[
    html.H1(children='AC Data Dashboard'),
    html.Div(children='''Select subfleet:'''),
    subfleet,
    html.Div(children=[
        dcc.Graph(id='bar-chart'),
        table
    ])
])

# Create the app
app = dash.Dash(__name__)
server = app.server
app.layout = app_layout

# Define the callback function to update the plots when the dropdown or bar chart is changed
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('table', 'data')],
    [Input('Subfleet', 'value'),
     Input('bar-chart', 'clickData')],
    [State('table', 'data')]
)
def update_plots(subfleet, click_data, table_data):
    # Update the bar chart
    filtered_data = acdata[acdata['Subfleet'] == subfleet]
    filtered_data = filtered_data.sort_values('Age', ascending=False)

    if click_data is not None:
        selected_ac = click_data['points'][0]['x']
        selected_row = acdata[acdata['AC#'] == selected_ac].iloc[0]
        new_row = selected_row.to_dict()
        table_data.append(new_row)

    bar_fig = px.bar(filtered_data, x='AC#', y='Age', color='Retired', hover_data=['AC#', 'Age', 'Retired', 'Eng Type', 'Etops'],
                     title='Age vs. AC for {} subfleet'.format(subfleet),
                     range_x=[filtered_data['AC#'].min(), filtered_data['AC#'].max()])

    return bar_fig, table_data


if __name__ == '__main__':
    app.run_server(debug=True)
