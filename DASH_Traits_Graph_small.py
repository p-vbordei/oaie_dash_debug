import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
import json
##  pip install dash-defer-js-import
# import dash_defer_js_import as ddji

draw_function = '''
function drawGraph(graphData) {
    console.log('drawGraph called with data:', graphData);
    // Load D3 library
    const d3 = window.d3;
  
    // Find graph container
    const container = document.getElementById('graph-container');
    if (!container) {
      console.error('Could not find graph container');
      return;
    }
    // container.innerHTML = '';
  
    // Create SVG
    const svg = d3.select(container)
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%');
  
    // Set up simulation
    const simulation = d3.forceSimulation()
        .force('link', d3.forceLink().id(d => d.id))
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(window.innerWidth / 2, window.innerHeight / 2));
  
    // Create links and nodes
    const link = svg.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(graphData.links)
        .enter().append('line')
        .attr('stroke-width', 2)
        .attr('stroke', '#008000'); // Green
  
    const node = svg.append('g')
        .attr('class', 'nodes')
        .selectAll('circle')
        .data(graphData.nodes)
        .enter().append('circle')
        .attr('r', 8);
  
    node.append('title')
        .text(d => d.label);
  
    // Update link and node positions on simulation tick
    simulation
        .nodes(graphData.nodes)
        .on('tick', ticked);
  
    simulation.force('link')
        .links(graphData.links);
  
    // Tick function
    function ticked() {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
  
        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
    }
  }
  

'''


# Load the data
weighted_product_facts_df_graph = pd.read_csv('weighted_product_facts_df_graph.csv')

# Create the nodes and links of the graph
nodes = []
links = []

# Add nodes and links for weighted_product_facts_df_graph
for idx, row in weighted_product_facts_df_graph.head(10).iterrows():
    source_node = row['asin.original']
    target_node = row['data_label']
    nodes.append({'id': source_node, 'label': source_node, 'color': 'grey', 'type': 'Product'})
    nodes.append({'id': target_node, 'label': target_node, 'color': 'green', 'type': 'Fact'})
    links.append({'source': source_node, 'target': target_node, 'rating': int(row['weighted_rating'])})

# Remove duplicate nodes
nodes = list({node['id']: node for node in nodes}.values())


graph_data = {
    'nodes': nodes,
    'links': links
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(id='graph-container', style={'width': '100%', 'height': '500px'}),
    html.Script(src='https://d3js.org/d3.v5.min.js'),
    html.Script(draw_function),
    dcc.Store(id='graph-data', data=json.dumps(graph_data)),
    dcc.Interval(id='draw-graph-interval', interval=6000, n_intervals=0)
])
 
@app.callback(Output('graph-container', 'children'),
              Input('graph-data', 'data'),
              Input('draw-graph-interval', 'n_intervals'))
def draw_graph(graph_data, n_intervals):
    if graph_data is not None:
        graph_data = json.loads(graph_data)
        # Write graph data to JSON file
        with open('graph_data.json', 'w') as f:
            json.dump(graph_data, f)
        return html.Script('drawGraph(' + json.dumps(graph_data) + ');')
    else:
        return html.Div('No Data Available', style={'fontSize': '24px', 'textAlign': 'center'})

if __name__ == '__main__':
    app.run_server(debug=True, port = 8070)
