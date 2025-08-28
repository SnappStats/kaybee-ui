from knowledge_graph_service import fetch_knowledge_graph
from streamlit_agraph import agraph, Node, Edge, Config

def get_agraph(graph_id: str):
    kg = fetch_knowledge_graph(graph_id)
    nodes = []
    edges = []

    for k, v in kg['entities'].items():
        nodes.append(Node(id=v['entity_id'], 
                          label=v['entity_names'][0], 
                          title=', '.join(v['entity_names']), 
                          size=10,
                          shape='box'))
    for e in kg['relationships']:
        edges.append(Edge(source=e['source_entity_id'], 
                          label=e['relationship'], 
                          target=e['target_entity_id']))

    config = Config(width=750,
                    height=450,
                    directed=True, 
                    physics=True, 
                    hierarchical=False,
                    # **kwargs
                    )

    return agraph(nodes=nodes, edges=edges, config=config)


