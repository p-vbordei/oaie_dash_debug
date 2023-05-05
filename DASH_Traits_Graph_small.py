import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
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


#### EXAMPLE HOW TO USE FORCE GRAPH
"""chart = ForceGraph(miserables, {
    nodeId: d => d.id,
    nodeGroup: d => d.group,
    nodeTitle: d => `${d.id}\n${d.group}`,
    linkStrokeWidth: l => Math.sqrt(l.value),
    width,
    height: 600,
    invalidation // a promise to stop the simulation when the cell is re-run
  })"""


#### SAMPLE DATA {"nodes": [{"id": "B01M4OV4Q4", "label": "B01M4OV4Q4", "color": "grey", "type": "Product"}, {"id": "Magnetic board", "label": "Magnetic board", "color": "green", "type": "Fact"}, {"id": "B07XCRT49W", "label": "B07XCRT49W", "color": "grey", "type": "Product"}, {"id": "Magnetic drawing board", "label": "Magnetic drawing board", "color": "green", "type": "Fact"}, {"id": "balls get stuck", "label": "balls get stuck", "color": "red", "type": "Issue"}, {"id": "B07XCRVK2Y", "label": "B07XCRVK2Y", "color": "grey", "type": "Product"}, {"id": "Availability of replacement pens", "label": "Availability of replacement pens", "color": "blue", "type": "Improvement"}, {"id": "B07X7YFZWG", "label": "B07X7YFZWG", "color": "grey", "type": "Product"}], "links": [{"source": "B01M4OV4Q4", "target": "Magnetic board", "rating": 3}, {"source": "B07XCRT49W", "target": "Magnetic drawing board", "rating": 4}, {"source": "B07XCRT49W", "target": "balls get stuck", "rating": 3}, {"source": "B07XCRVK2Y", "target": "balls get stuck", "rating": 3}, {"source": "B07XCRT49W", "target": "Availability of replacement pens", "rating": 2}, {"source": "B07X7YFZWG", "target": "Availability of replacement pens", "rating": 2}]}


ForceGraphFunction = '''
function ForceGraph({
    nodes, // an iterable of node objects (typically [{id}, …])
    links // an iterable of link objects (typically [{source, target}, …])
  }, {
    nodeId = d => d.id, // given d in nodes, returns a unique identifier (string)
    nodeGroup, // given d in nodes, returns an (ordinal) value for color
    nodeGroups, // an array of ordinal values representing the node groups
    nodeTitle, // given d in nodes, a title string
    nodeFill = "currentColor", // node stroke fill (if not using a group color encoding)
    nodeStroke = "#fff", // node stroke color
    nodeStrokeWidth = 1.5, // node stroke width, in pixels
    nodeStrokeOpacity = 1, // node stroke opacity
    nodeRadius = 5, // node radius, in pixels
    nodeStrength,
    linkSource = ({source}) => source, // given d in links, returns a node identifier string
    linkTarget = ({target}) => target, // given d in links, returns a node identifier string
    linkStroke = "#999", // link stroke color
    linkStrokeOpacity = 0.6, // link stroke opacity
    linkStrokeWidth = 1.5, // given d in links, returns a stroke width in pixels
    linkStrokeLinecap = "round", // link stroke linecap
    linkStrength,
    colors = d3.schemeTableau10, // an array of color strings, for the node groups
    width = 640, // outer width, in pixels
    height = 400, // outer height, in pixels
    invalidation // when this promise resolves, stop the simulation
  } = {}) {
    // Compute values.
    const N = d3.map(nodes, nodeId).map(intern);
    const LS = d3.map(links, linkSource).map(intern);
    const LT = d3.map(links, linkTarget).map(intern);
    if (nodeTitle === undefined) nodeTitle = (_, i) => N[i];
    const T = nodeTitle == null ? null : d3.map(nodes, nodeTitle);
    const G = nodeGroup == null ? null : d3.map(nodes, nodeGroup).map(intern);
    const W = typeof linkStrokeWidth !== "function" ? null : d3.map(links, linkStrokeWidth);
    const L = typeof linkStroke !== "function" ? null : d3.map(links, linkStroke);
  
    // Replace the input nodes and links with mutable objects for the simulation.
    nodes = d3.map(nodes, (_, i) => ({id: N[i]}));
    links = d3.map(links, (_, i) => ({source: LS[i], target: LT[i]}));
  
    // Compute default domains.
    if (G && nodeGroups === undefined) nodeGroups = d3.sort(G);
  
    // Construct the scales.
    const color = nodeGroup == null ? null : d3.scaleOrdinal(nodeGroups, colors);
  
    // Construct the forces.
    const forceNode = d3.forceManyBody();
    const forceLink = d3.forceLink(links).id(({index: i}) => N[i]);
    if (nodeStrength !== undefined) forceNode.strength(nodeStrength);
    if (linkStrength !== undefined) forceLink.strength(linkStrength);
  
    const simulation = d3.forceSimulation(nodes)
        .force("link", forceLink)
        .force("charge", forceNode)
        .force("center",  d3.forceCenter())
        .on("tick", ticked);
  
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;");
  
    const link = svg.append("g")
        .attr("stroke", typeof linkStroke !== "function" ? linkStroke : null)
        .attr("stroke-opacity", linkStrokeOpacity)
        .attr("stroke-width", typeof linkStrokeWidth !== "function" ? linkStrokeWidth : null)
        .attr("stroke-linecap", linkStrokeLinecap)
      .selectAll("line")
      .data(links)
      .join("line");
  
    const node = svg.append("g")
        .attr("fill", nodeFill)
        .attr("stroke", nodeStroke)
        .attr("stroke-opacity", nodeStrokeOpacity)
        .attr("stroke-width", nodeStrokeWidth)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
        .attr("r", nodeRadius)
        .call(drag(simulation));
  
    if (W) link.attr("stroke-width", ({index: i}) => W[i]);
    if (L) link.attr("stroke", ({index: i}) => L[i]);
    if (G) node.attr("fill", ({index: i}) => color(G[i]));
    if (T) node.append("title").text(({index: i}) => T[i]);
    if (invalidation != null) invalidation.then(() => simulation.stop());
  
    function intern(value) {
      return value !== null && typeof value === "object" ? value.valueOf() : value;
    }
  
    function ticked() {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
  
      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    }
  
    function drag(simulation) {    
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }
      
      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }
      
      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }
      
      return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }
  
    return Object.assign(svg.node(), {scales: {color}});
  }

'''


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(id='graph-container', style={'width': '100%', 'height': '500px'}),
    html.Script(src='https://d3js.org/d3.v5.min.js'),
    html.Script(ForceGraphFunction),
    dcc.Interval(id='draw-graph-interval', interval=6000, n_intervals=0)
])

@app.callback(Output('graph-container', 'children'),
              Input('draw-graph-interval', 'n_intervals'))
def draw_graph(n_intervals):
    return html.Script(f'ForceGraph({json.dumps(graph_data)});')

if __name__ == '__main__':
    app.run_server(debug=True, port=8070)