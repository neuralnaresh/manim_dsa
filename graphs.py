from manim import *
import numpy as np

class CustomGraph:
    def __init__(self, vertices, edges, config=None, layout = "circular"):
        self.vertices = vertices
        self.edges = edges
        self.layout = layout
        self.config = {
            "layout": self.layout,
            "layout_scale": 2,
            "vertex_config": {"fill_color": "#ffcbf2", "radius": 0.35},
            "root_vertex": 8,
            "edge_config": {"color": GRAY},
            "arrow_tip_length": 0.12,
            "arrow_colors": {"left": RED, "right": GREEN},
            "arrow_buff": 0.1,
            "max_tip_length_to_length_ratio": 0.5,
        }
        if config:
            self.config.update(config)

    def create_graph(self):

        g = Graph(self.vertices, self.edges, layout=self.config["layout"],
                  layout_scale=self.config["layout_scale"],
                  labels=True,
                  vertex_config=self.config["vertex_config"],
                  root_vertex=self.config["root_vertex"],
                  edge_config=self.config["edge_config"])
        
        return g

    def create_arrows(self, g):

        shortest_edge_length = max(
            np.linalg.norm(g[edge[1]].get_center() - g[edge[0]].get_center()) for edge in self.edges
        )

        tip_length = shortest_edge_length * self.config["arrow_tip_length"]

        arrows = VGroup()
        animations = []
        for edge in self.edges:
            start_node = g[edge[0]]
            end_node = g[edge[1]]
            direction = end_node.get_center() - start_node.get_center()
            direction_normalized = direction / np.linalg.norm(direction) * (start_node.width / 2 - 0.08)
            arrow_color = self.config["arrow_colors"]["left"] if end_node.get_center()[0] < start_node.get_center()[0] else self.config["arrow_colors"]["right"]
            arrow = Arrow(start_node.get_center() + direction_normalized,
                          end_node.get_center() - direction_normalized,
                          buff=self.config["arrow_buff"],
                          tip_length= tip_length,
                          max_tip_length_to_length_ratio=self.config["max_tip_length_to_length_ratio"],
                          color=arrow_color).set_z_index(1)
            arrows.add(arrow)
            # animations.append(Create(arrow))
        return arrows
