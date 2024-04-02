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
        self.edges = []  # on stocke les arêtes sous forme de liste de tuples
                                # (pas forcément utile)

    def add_edge(self, start: int, end: int):
        self.edges.append((start, end))
        if start not in self.neighbours:
            self.neighbours[start] = {}
        else:
            self.neighbours[start].append(end)
        if end not in self.neighbours:
            self.neighbours[end] = {}
        else:
            self.neighbours[end].append(start)

    def add_vertex(self, vertex: int):
        self.neighbours[vertex] = {}

    def __str__(self):
        return f"Graph: {self.neighbours}"

    def __repr__(self):
        return f"Graph: {self.neighbours}"


graph = Graph()
graph.add_vertex(1)
graph.add_vertex(2)
graph.add_vertex(3)
graph.add_edge(1, 2)
graph.add_edge(2, 3)


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
    set_communities = {}
    for node in graph.neighbours:
        for neighbour in graph.neighbours[node]:
            common_neighbours = graph.neighbours[node] & graph.neighbours[neighbour]
            if len(common_neighbours) > 0:
                common_neighbours = common_neighbours | {node, neighbour}
                if interconnectivity(common_neighbours) > treshold:
                    set_communities = evaluate_communities(set_communities, common_neighbours, treshold)
    return set_communities


APAL(graph)
