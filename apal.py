class Graph:
    def __init__(self):
        """
        On stocke les noeuds sous forme de dictionnaires, les noeuds sont les
        clés et les valeurs sont les listes des noeuds voisins.

        On stocke les arêtes sous forme de liste de tuples.

        A chaque ajout d'arrête, on met à jour les listes des voisins des
        noeuds concernés.

        On peut aussi ajouter des noeuds sans arêtes, dans ce cas on ajoute
        juste une clé dans le dictionnaire des noeuds.
        """
        self.neighbours = {}
        self.edges = []  # on stocke les arêtes sous forme de liste de tuples (pas forcément utile)

    def add_edge(self, start: int, end: int):
        self.edges.append((start, end))
        if start not in self.neighbours:
            self.neighbours[start] = set({end})
        else:
            self.neighbours[start] = {end} | self.neighbours[start]
        if end not in self.neighbours:
            self.neighbours[end] = set({start})
        else:
            self.neighbours[end] = {start} | self.neighbours[end]

    def add_vertex(self, vertex: int):
        self.neighbours[vertex] = set({})

    def __str__(self):
        return f"Graph: {self.neighbours}"

    def __repr__(self):
        return f"Graph: {self.neighbours}"


graph = Graph()
graph.add_vertex(1)
graph.add_vertex(2)
graph.add_vertex(3)
graph.add_vertex(4)
graph.add_vertex(5)
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(2, 3)
graph.add_edge(2, 4)
graph.add_edge(4, 5)
graph.add_edge(3, 5)


def intraconnectivity(set_nodes, graph):
    """
    """
    print(f"set_nodes: {set_nodes}")
    k = 0
    for node in set_nodes:
        print(f"node: {node}")
        k += len(set_nodes & graph.neighbours[node])
    return k / (len(set_nodes) * (len(set_nodes) - 1))


def evaluate_communities(set_communities, possible_community, treshold):
    """
    """
    print(f"set_communities: {set_communities}")
    print(f"possible_community: {possible_community}")
    jaccard_M = 0
    communities_M = set()
    for community in set_communities:
        jaccard = len(possible_community & community) / len(possible_community | community)
        alpha = intraconnectivity(possible_community | community, graph)
        if possible_community >= community:
            return set_communities
        elif community > possible_community:
            set_communities = set_communities.pop(community)
        elif jaccard > jaccard_M and jaccard > treshold and alpha > treshold:
            jaccard_M = jaccard
            communities_M = community | possible_community
    if communities_M:
        possible_community = communities_M
    print(set_communities, type(set_communities))
    print(possible_community, type(possible_community))
    set_communities.append(possible_community)
    return set_communities


def APAL(graph, treshold=0.5):
    """
    Décrit une fonction APAL qui permet de distinguer des communautés
    dans un graphe.

    Parameters:
        graph (Graph): Le graphe sur lequel l'algorithme sera appliqué.

    Returns:
        List[Graph]: Une liste de listes représentant les communautés
        détectées dans le graphe.
    """
    set_communities = []
    for node in graph.neighbours:
        for neighbour in graph.neighbours[node]:
            common_neighbours = graph.neighbours[node] & graph.neighbours[neighbour]
            if len(common_neighbours) > 0:
                common_neighbours = common_neighbours | {node, neighbour}
                if intraconnectivity(common_neighbours, graph) > treshold:
                    set_communities = evaluate_communities(
                            set_communities, common_neighbours, treshold
                            )
    return set_communities


APAL(graph)
