
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        drawGraph: function(graphData) {
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
            

            data = JSON.parse(graphData)
            
            // Create links and nodes
            const link = svg.append('g')
                .attr('class', 'links')
                .selectAll('line')
                .data(data.links)
                .enter().append('line')
                .attr('stroke-width', 2)
                .attr('stroke', '#008000'); // Green
        
            const node = svg.append('g')
                .attr('class', 'nodes')
                .selectAll('circle')
                .data(data.nodes)
                .enter().append('circle')
                .attr('r', 8);
        
            node.append('title')
                .text(d => d.label);
        
            // Update link and node positions on simulation tick
            simulation
                .nodes(data.nodes)
                .on('tick', ticked);
        
            simulation.force('link')
                .links(data.links);
        
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
}});