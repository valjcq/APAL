import json
#import pickle
import networkx as nx
import matplotlib.pyplot as plt

# Load JSON data
try:
    with open('ppi-G.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: JSON file not found.")
    exit()
except json.JSONDecodeError:
    print("Error: Invalid JSON format.")
    exit()

# Create an empty undirected graph
G = nx.Graph()

# Keep track of added node IDs
added_nodes = set()

## Count total number of nodes in the data
total_nodes = len(data['nodes'])
print("Total number of nodes in the data:", total_nodes)

# Add nodes with attributes
for node_data in data['nodes'][:5000]:
    node_id = node_data['id']
    if node_id not in added_nodes:
        G.add_node(node_id, **node_data)  # Add node with its attributes
        added_nodes.add(node_id)  # Add node ID to the set of added nodes
        #print(f"Added node {node_id}: {node_data.get('name', '')}")

# Count total number of links in the data
total_links = len(data['links'])
print("Total number of links in the data:", total_links)

# Add links with attributes
for link_data in data['links'][:5000]:
    try:
        source_id = link_data['source']
        target_id = link_data['target']
        if source_id in added_nodes and target_id in added_nodes:
            if source_id != target_id:
                G.add_edge(source_id, target_id, **link_data)  # Add edge with its attributes
                #print(f"Added edge: {source_id} -> {target_id}")
            else:
                print(f"Skipped edge: One or both nodes not in the added nodes, or self-loop.")
    except KeyError:
        print(f"Error adding edge: Missing keys in link data: {link_data}")

# Print the number of nodes and edges
print("Number of nodes added to the graph:", G.number_of_nodes())
print("Number of edges added to the graph:", G.number_of_edges())

# Generate layout (manual layout for better control)
try:
    pos = nx.spring_layout(G, k=0.5,iterations = 50, seed=42)  # Seed for reproducibility
except nx.NetworkXError:
    print("Error: Unable to generate layout.")
    exit()

# Visualize the graph
plt.figure(figsize=(50, 40))  # Adjust the figure size
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1, alpha=0.5)  # Adjust node_size for smaller nodes
plt.savefig('graph_image.png')  # Save the graph as an image
plt.show()

# Convert the NetworkX graph to a dictionary
graph_data = {
    "nodes": [],
    "links": []
}

for node_id, node_attrs in G.nodes(data=True):
    node_data = {"id": node_id}
    node_data.update(node_attrs)
    graph_data["nodes"].append(node_data)

for source, target, edge_attrs in G.edges(data=True):
    link_data = {"source": source, "target": target}
    link_data.update(edge_attrs)
    graph_data["links"].append(link_data)

# Save the graph data to a JSON file
with open('PPI_Graph_5000.json', 'w') as file:
    json.dump(graph_data, file, indent=4)




#Convert the graph to a dictionary of dictionaries format
#graph_data = nx.to_dict_of_dicts(G)

#Write the graph data to a JSON file
#with open('PPI_Graph_5000.json', 'w') as outfile:
    #json.dump(graph_data, outfile)
