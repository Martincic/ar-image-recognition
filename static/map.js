//Campus map points

import * as Graph from './graph.js';
import * as Coordinates from './coordinates.js';

let graph = new Graph.Graph(Coordinates.map);

export function getCoordinatesForRoute(start_id, destination_id){
    let nodes = [];
    // Get shortest path ID's using internal map (defined at line 147@map.js)
    let path = graph.findShortestPath(start_id, destination_id);
    // for every ID, find the element and get XY coordinates
    path.forEach(node_id => {
        let x,y = 0;
        let node = document.getElementById(node_id); 
        
        // Parse coordinates from different types of SVG objects
        if(node.attributes.class.value.split(' ').includes('item')){
            let points = node.attributes.points.value.split(' ');
            y = points[5];
            x = (parseFloat(points[4]) + parseFloat(points[10])) / 2;
        }
        else if(node.attributes.class.value.split(' ').includes('point')){
            x = node.attributes.cx.value;
            y = node.attributes.cy.value;
        }
        else if (node.attributes.class.value.split(' ').includes('destination')) {
            x = node.attributes.x.value;
            y = node.attributes.y.value;
        }
        let coords = {'x':parseFloat(x),'y':parseFloat(y)}
        nodes.push(coords);
    });

    return nodes;
}