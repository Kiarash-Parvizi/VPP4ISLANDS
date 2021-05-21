from src.vppNode.VppBoxNode import VppBoxNode
from src.vppNode.VppNode import VppNode
from src.vppNode.Junction import Junction
from typing import Dict
from src.vppNode.LineProps import LineProps


NNodes = 15

vppNode = VppNode()

nodes: Dict[int, Junction] = {3: VppBoxNode(node_id=3, p_max=100, i_max=100),
                                4: VppBoxNode(node_id=4, p_max=100, i_max=100),
                                7: VppBoxNode(node_id=7, p_max=100, i_max=100),
                                8: VppBoxNode(node_id=8, p_max=100, i_max=100),
                                11: VppBoxNode(node_id=11, p_max=100, i_max=100),
                                13: VppBoxNode(node_id=13, p_max=100, i_max=100),
                                14: VppBoxNode(node_id=14, p_max=100, i_max=100),
                                15: VppBoxNode(node_id=15, p_max=100, i_max=100)}

for i in range(1, NNodes + 1):
    if i not in nodes.keys():
        nodes[i] = Junction()

for _, node in nodes.items():
    if isinstance(node, VppBoxNode):
        node.load_resources_from_api()

j_ids = {_id: vppNode.add_junction(item) for _id, item in nodes.items()}

connections = [
    {
        'nodes': (1, 2),
        'line': LineProps(1.35309, 1.32349, 241.444, 2)
    },

    {
        'nodes': (2, 3),
        'line': LineProps(1.17024, 1.14464, 228.16502204493, 1.89)
    },

    {
        'nodes': (2, 6),
        'line': LineProps(2.55727, 1.7249, 241.444467772412, 2)
    },

    {
        'nodes': (2, 9),
        'line': LineProps(2.01317, 1.3579, 152.834348099937, 1.266)
    },

    {
        'nodes': (3, 4),
        'line': LineProps(0.84111, 0.82271, 228.16502204493, 1.89)
    },

    {
        'nodes': (3, 11),
        'line': LineProps(1.79553, 1.2111, 152.834348099937, 1.266)
    },

    {
        'nodes': (4, 5),
        'line': LineProps(1.52348, 1.0276, 152.834348099937, 1.266)
    },

    {
        'nodes': (4, 14),
        'line': LineProps(2.23081, 1.5047, 152.834348099937, 1.266)
    },

    {
        'nodes': (4, 15),
        'line': LineProps(1.19702, 0.8074, 152.834348099937, 1.266)
    },

    {
        'nodes': (6, 7),
        'line': LineProps(1.0882, 0.734, 241.444467772412, 2)
    },

    {
        'nodes': (6, 8),
        'line': LineProps(1.25143, 0.8441, 241.444467772412, 2)
    },

    {
        'nodes': (9, 10),
        'line': LineProps(1.68671, 1.1377, 152.834348099937, 1.266)
    },

    {
        'nodes': (11, 12),
        'line': LineProps(2.44845, 1.6515, 152.834348099937, 1.266)
    },

    {
        'nodes': (12, 13),
        'line': LineProps(2.01317, 1.3579, 152.834348099937, 1.266)
    },
]

connections_history = {}
for connection in connections:
    _id = vppNode.add_edge_by_line(connection['nodes'], connection['line'])
    connections_history[_id] = connection

