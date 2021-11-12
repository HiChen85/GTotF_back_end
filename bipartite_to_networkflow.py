import networkx as nx
import json

from EK import EK


def get_data(scenario:str):
    with open('scenarios.json', 'r', encoding="UTF-8") as f:
        data = json.loads(f.read())
    return data[scenario]


s1 = get_data("scenario1")
s2 = get_data("scenario2")
s3 = get_data("scenario3")
s4 = get_data("scenario4")
s5 = get_data("scenario5")
s6 = get_data("scenario6")
s7 = get_data("scenario7")

def generate_bipartite_graph(scenario:dict):
    g = nx.DiGraph(name="bipartite_graph")
    farmers = scenario['farmer']
    animals = scenario['animals']
    
    g.add_nodes_from(farmers.keys(), bipartite=1)
    g.add_nodes_from(animals.keys(), bipartite=0)
    
    for animal, eats in animals.items():
        for e in eats:
            for farmer, has in farmers.items():
                if e in has:
                    g.add_edge(animal, farmer, capacity=1, flow=0, residual=1)

    return g


def bipartite_to_networkflow(g:nx.DiGraph):
    # add source node for the graph
    bipartite_0 = [n for n in g.nodes if g.nodes[n]['bipartite']==0]
    bipartite_1 = [n for n in g.nodes if g.nodes[n]['bipartite']==1]

    for i in bipartite_0:
        g.add_edge('s', i, capacity=1, flow=0, residual=1)
    for i in bipartite_1:
        g.add_edge(i, 't', capacity=1, flow=0, residual=1)

    return g


if __name__ == '__main__':
    g = generate_bipartite_graph(s7)
    g = bipartite_to_networkflow(g)
    print(g.nodes)
    print(g.edges)
    print(EK(g, 's', 't'))