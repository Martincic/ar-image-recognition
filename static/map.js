//Campus map points
var Graph = (function (undefined) {

	var extractKeys = function (obj) {
		var keys = [], key;
		for (key in obj) {
		    Object.prototype.hasOwnProperty.call(obj,key) && keys.push(key);
		}
		return keys;
	}

	var sorter = function (a, b) {
		return parseFloat (a) - parseFloat (b);
	}

	var findPaths = function (map, start, end, infinity) {
		infinity = infinity || Infinity;

		var costs = {},
		    open = {'0': [start]},
		    predecessors = {},
		    keys;

		var addToOpen = function (cost, vertex) {
			var key = "" + cost;
			if (!open[key]) open[key] = [];
			open[key].push(vertex);
		}

		costs[start] = 0;

		while (open) {
			if(!(keys = extractKeys(open)).length) break;

			keys.sort(sorter);

			var key = keys[0],
			    bucket = open[key],
			    node = bucket.shift(),
			    currentCost = parseFloat(key),
			    adjacentNodes = map[node] || {};

			if (!bucket.length) delete open[key];

			for (var vertex in adjacentNodes) {
			    if (Object.prototype.hasOwnProperty.call(adjacentNodes, vertex)) {
					var cost = adjacentNodes[vertex],
					    totalCost = cost + currentCost,
					    vertexCost = costs[vertex];

					if ((vertexCost === undefined) || (vertexCost > totalCost)) {
						costs[vertex] = totalCost;
						addToOpen(totalCost, vertex);
						predecessors[vertex] = node;
					}
				}
			}
		}

		if (costs[end] === undefined) {
			return null;
		} else {
			return predecessors;
		}

	}

	var extractShortest = function (predecessors, end) {
		var nodes = [],
		    u = end;

		while (u !== undefined) {
			nodes.push(u);
			u = predecessors[u];
		}

		nodes.reverse();
		return nodes;
	}

	var findShortestPath = function (map, nodes) {
		var start = nodes.shift(),
		    end,
		    predecessors,
		    path = [],
		    shortest;

		while (nodes.length) {
			end = nodes.shift();
			predecessors = findPaths(map, start, end);

			if (predecessors) {
				shortest = extractShortest(predecessors, end);
				if (nodes.length) {
					path.push.apply(path, shortest.slice(0, -1));
				} else {
					return path.concat(shortest);
				}
			} else {
				return null;
			}

			start = end;
		}
	}

	var toArray = function (list, offset) {
		try {
			return Array.prototype.slice.call(list, offset);
		} catch (e) {
			var a = [];
			for (var i = offset || 0, l = list.length; i < l; ++i) {
				a.push(list[i]);
			}
			return a;
		}
	}

	var Graph = function (map) {
		this.map = map;
	}

	Graph.prototype.findShortestPath = function (start, end) {
		if (Object.prototype.toString.call(start) === '[object Array]') {
			return findShortestPath(this.map, start);
		} else if (arguments.length === 2) {
			return findShortestPath(this.map, [start, end]);
		} else {
			return findShortestPath(this.map, toArray(arguments));
		}
	}

	Graph.findShortestPath = function (map, start, end) {
		if (Object.prototype.toString.call(start) === '[object Array]') {
			return findShortestPath(map, start);
		} else if (arguments.length === 3) {
			return findShortestPath(map, [start, end]);
		} else {
			return findShortestPath(map, toArray(arguments, 1));
		}
	}

	return Graph;

})();

let map = {
    'C': { //enterance
        'B':1
    },
    'B': { //enterance hallway
        'd-lounge':1,
        'd-R':1,
        '3':1,
        '2':1,
        'C':1,
        'd-12':1,
    },'d-lounge':{'B':1, 'D':1},'d-R':{'B':1},'d-12':{'B':1},
    '2': { //in front of toilet
        'B':1,
        'd-19':1,
        'A':1,
        '1':1
    },'d-19':{'2':1},
    '1': {
        'd-13':1,
        'd-14':1,
        'd-15':1,
        'd-16':1,
    },'d-13':{'1':1},'d-14':{'1':1},'d-15':{'1':1},'d-16':{'1':1},
    'A':{
        'd-17':1,
        '2':1
    },'d-17':{'A':1},
    'D':{
        'd-lounge':1,
        'E':1
    },
    'E':{
        'D':1,
        'd-20':1,
        'd-21':1,
        'd-22':1,
        'd-23':1,
        'd-24':1,
        'd-25':1
    },'d-20':{'E':1},'d-21':{'E':1},'d-22':{'E':1},'d-23':{'E':1},'d-24':{'E':1},'d-25':{'E':1},
    '3':{
        'B':1,
        'd-1':1,
        'F':1,
    },'d-1':{'3':1},
    'F':{
        '5':1, //5 je gore
        '4':1,
        'G':1
    },
    '5':{
        'd-2':1,
        'd-3':1,
        'd-4':1,
        'F':1,
    },'d-2':{'5':1},'d-3':{'5':1},'d-4':{'5':1},
    '4':{
        'F':1,
        'd-8':1,
        'd-9':1,
        'd-10':1,
        'd-11':1,
    },'d-8':{'4':1},'d-9':{'4':1},'d-10':{'4':1},
    'd-11':{
        '4':1,
        'd-studentLab':1
    },'d-studentLab':{'d-11':1},
    'G':{
        'F':1,
        '6':1,
        'd-7':1,
    },'d-7':{'G':1},
    '6':{
        'd-5':1,
        'H':1
    },'d-5':{'6':1},
    'H':{
        '6':1,
        '7':1
    },
    '7':{
        'H':1,
        'd-6':1,
        '8':1,
    },'d-6':{'7':1},
    '8':{
        '7':1,
        'd-27':1,
        'I':1
    },'d-27':{'8':1},
    'I':{
        'd-lounge2':1,
        'd-SG':1,
        'J':1,
        '8':1,
    },'d-lounge2':{'I':1},'d-SG':{'I':1},
    'J':{
        'I':1,
        'd-gym':1,
        'd-29':1
    },'d-gym':{'J':1},'d-29':{'I':1}
};

let graph = new Graph(map);

let path = graph.findShortestPath('C', 'd-gym');

let nodes = [];
path.forEach(node_id => {

    node = document.getElementById(node_id);
    nodes.push(node);
    let x, y = 0;
    try{
        x = node.attributes.cx.value;
        y = node.attributes.cy.value;
    }
    catch(e){
        if (e instanceof TypeError) {
            console.log('type error');
        }
        else {
            x = node.attributes.x.value;
            y = node.attributes.y.value;
        }
    }
    console.log('ID:'+node_id + " x:"+x + " y:"+y);

});

console.log(nodes);