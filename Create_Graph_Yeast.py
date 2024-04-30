import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json

# Read the Excel file
file_path = "RRS.xlsx"
df = pd.read_excel(file_path)

# Drop rows with all NaN values (empty lines)
df = df.dropna(how="all")

# Initialize a graph
G = nx.Graph()

# Iterate over each row to add edges to the graph
for index, row in df.iterrows():
    protein_a = row.iloc[0]
    protein_b = row.iloc[1]

    # Skip rows with missing data or self-interacting proteins
    if pd.isnull(protein_a) or pd.isnull(protein_b) or protein_a == protein_b:
        continue

    G.add_edge(protein_a, protein_b)

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
plt.savefig('graph_RRS_image.png')  # Save the graph as an image
plt.show()

# Save the graph data as JSON
graph_data = nx.node_link_data(G)
with open("graph_RRS_data.json", "w") as json_file:
    json.dump(graph_data, json_file, indent=4)
