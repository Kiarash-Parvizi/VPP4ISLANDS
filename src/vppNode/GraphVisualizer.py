import networkx as nx
import matplotlib.pyplot as plt
from .VppNode import VppNode

class GraphVisualizer:
    def __init__(self, vppNode: VppNode) -> None:
        self.vppNode = vppNode
        self.graph = nx.Graph()
        self.process()
    
    def process(self):
        self.graph.clear()
        for id, edge in self.vppNode.edgeMp.getItems():
            self.graph.add_edge(edge.junctions[0], edge.junctions[1])
    
    def draw(self):
        plt.subplot(121)
        #
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.subplot(122)
        #
        nx.draw_shell(self.graph, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
        plt.show()