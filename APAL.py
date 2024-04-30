from __future__ import absolute_import
from __future__ import division
from Graph import Graph


class APAL:
    def __init__(self):
        self.graph = Graph()
        self.communities = dict()
        self.community_count = 0

    def evaluate(self, candidate_community, threshold):
        communities_to_remove = list()
        if self.fitness(candidate_community) < threshold:
            return
        selected_community = None
        temporary_max_value = 0
        for community in self.communities:
            temporary_value = len(self.communities[community].intersection(candidate_community)) / len(candidate_community.union(self.communities[community]))
            if candidate_community.issubset(self.communities[community]):
                return
            elif self.communities[community].issubset(candidate_community):
                communities_to_remove.append(community)
            elif temporary_value > threshold and temporary_value > temporary_max_value and self.fitness(candidate_community.union(self.communities[community])) >= threshold:
                temporary_max_value = temporary_value
                selected_community = community
        for community in communities_to_remove:
            self.communities.pop(community)
        if selected_community is not None:
            self.communities[selected_community] = candidate_community.union(self.communities[selected_community])
            return
        self.community_count += 1
        community_name = "comm" + str(self.community_count)
        self.communities[community_name] = candidate_community

    def fitness(self, candidate_community):
        sum_adjacent_vertices = 0
        for vertex in candidate_community:
            sum_adjacent_vertices += len(set(self.graph.get_adjacency_list(vertex)).intersection(set(candidate_community)))
        if sum_adjacent_vertices == 0:
            return -1
        community_order = len(candidate_community)
        return sum_adjacent_vertices / (community_order * (community_order - 1))

    def run_apal(self, t):
        for vertex in self.graph.vertices:
            adjacent_vertices = self.graph.get_adjacency_list(vertex)
            for adjacent_vertex in adjacent_vertices:
                set1 = set(adjacent_vertices).difference({adjacent_vertex})
                set2 = set(self.graph.get_adjacency_list(adjacent_vertex)).difference({vertex})
                community_set = set1.intersection(set2)
                if len(community_set) != 0:
                    community_set.add(vertex)
                    community_set.add(adjacent_vertex)
                    self.evaluate(community_set, t)
        return [list(x) for x in self.communities.values()]


if __name__ == '__main__':
    from OGG import *
    from CompareClusters import CompareClusters as CC
    from sys import argv
    if argv[1] == "OGG":
        # Test APAL with OGG
        list_results = list()
        nbr_range = int(argv[3])
        for alpha in [0.2, 0.4, 0.6, 0.8]:
            liste_alpha_res = list()
            for t in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
                average = 0
                for _ in range(nbr_range):
                    # OGG algorithm, generate a graph
                    ogg = OGG()
                    ogg.number_of_clusters = 10
                    ogg.average_cluster_size = 15
                    ogg.overlapping = 0.3
                    if argv[2] == "alpha":
                        ogg.interconnectivity = 0.2
                        ogg.intraconnectivity = alpha
                    elif argv[2] == "omega":
                        ogg.interconnectivity = alpha
                        ogg.intraconnectivity = 0.8
                    else:
                        print("Invalid argument")
                        exit(1)
                    ogg.generate_graph()
                    # APAL algorithm
                    apal = APAL()
                    apal.graph = ogg.graph
                    apal_clusters = apal.run_apal(t)
                    cc = CC(ogg.graph.vertices, ogg.clusters, apal_clusters)
                    average += cc.nvi_overlapping()
                liste_alpha_res.append(average/nbr_range)
            list_results.append(liste_alpha_res)
            liste_alpha_res = list()
        import matplotlib.pyplot as plt

        # Plot for alpha values
        plt.plot(
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            list_results[0],
            "b-o",
            label=f"{argv[2]}=0.2")
        plt.plot(
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            list_results[1],
            "g-o",
            label=f"{argv[2]}=0.4")
        plt.plot(
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            list_results[2],
            "y-o",
            label=f"{argv[2]}=0.6")
        plt.plot(
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            list_results[3],
            "r-o",
            label=f"{argv[2]}=0.8")
        plt.xlabel("Threshold")
        plt.ylabel("NVI")
        if argv[2] == "alpha":
            plt.title("NVI for APAL with OGG and different alpha values")
        elif argv[2] == "omega":
            plt.title("NVI for APAL with OGG and different omega values")
        plt.legend()
        plt.savefig(f"APAL_{argv[2]}_{argv[1]}.png")
        plt.show()

    elif argv[1] == "data":
        import json
        import networkx as nx
        import random
        import matplotlib.pyplot as plt
        # Test APAL with data
        # Load data
        g = Graph()
        data = json.load(open("graph_union_data.json"))
        for key in data["nodes"]:
            g.add_vertex(key["id"])
        for edge in data["links"]:
            g.add_edge(edge["source"], edge["target"])
        # APAL algorithm
        apal = APAL()
        apal.graph = g
        apal_clusters = apal.run_apal(float(argv[2]))
        print(apal_clusters)
        if len(argv) < 4:
            argv.append("pas image")
        if argv[3] == "image":
            # Generate layout (manual layout for better control)
            G = nx.Graph()
            for vertex in g.vertices:
                G.add_node(vertex)
                for edge in g.get_adjacency_list(vertex):
                    G.add_edge(vertex, edge)
            try:
                pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)  # Seed for reproducibility

            except nx.NetworkXError:
                print("Error: Unable to generate layout.")
                exit()

            # Visualize the graph
            # we need to change g graph to G graph which is a networkx graph
            plt.figure(figsize=(50, 40))  # Adjust the figure size
            # Change the color of specific nodes
            nx.draw(G, pos, with_labels=False, node_size=10,
                    alpha=0.2, node_color="black")

            def color_generator():
                while True:
                    yield "#" + ''.join([
                        random.choice('0123456789ABCDEF') for j in range(6)])

            # Usage example
            color_iter = color_generator()
            for cluster in apal_clusters:
                color = next(color_iter)
                # Change the color of specific nodes
                nx.draw_networkx_nodes(
                    G, pos, nodelist=cluster, alpha=0.5,
                    node_color=color, node_size=40
                    )
                # Change the color of specific edges
                for edge in G.edges:
                    if edge[0] in cluster and edge[1] in cluster:
                        nx.draw_networkx_edges(
                            G, pos, edgelist=[edge],
                            edge_color=color, width=3,
                            )
                # Add labels to nodes in the cluster
                nx.draw_networkx_labels(
                    G, pos, labels={node: node for node in cluster},
                    font_color=color, font_size=16
                    )
            # Save the graph as an image
            plt.savefig(f'graph_union_image_t{argv[2]}.png')
