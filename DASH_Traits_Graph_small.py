import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State, ClientsideFunction
import json


# Load the data
weighted_product_facts_df_graph = pd.read_csv('weighted_product_facts_df_graph.csv')

# Create the nodes and links of the graph
nodes = []
links = []

# Add nodes and links for weighted_product_facts_df_graph
for idx, row in weighted_product_facts_df_graph.head(10).iterrows():
    source_node = row['asin.original']
    target_node = row['data_label']
    nodes.append({'id': source_node, 'label': source_node})
    nodes.append({'id': target_node, 'label': target_node})
    links.append({'source': source_node, 'target': target_node})

# Remove duplicate nodes
nodes = list({node['id']: node for node in nodes}.values())


graph_data = {
    'nodes': nodes,
    'links': links
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Script(src='https://d3js.org/d3.v5.min.js'),
    html.Div(id='graph-container', style={'width': '100%', 'height': '500px'}),
    html.Div(id='code'),
    
    #html.Script(draw_function),
    dcc.Store(id='graph-data', data=json.dumps(graph_data)),
    dcc.Interval(id='draw-graph-interval', interval=6000, n_intervals=0)
])

app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='drawGraph'
        ),
        Output('code','children'),
        Input('graph-data', 'data')
)

if __name__ == '__main__':
    app.run_server(debug=True, port = 8070)

