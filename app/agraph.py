from knowledge_graph_service import fetch_knowledge_graph
from streamlit_agraph import agraph, Node, Edge, Config
import textwrap

def get_agraph(graph_id: str):
    g = fetch_knowledge_graph(graph_id)
    nodes = []
    edges = []

    for entity_id, entity in g['entities'].items():
        title = ', '.join(entity['entity_names'])
        if properties := entity.get('properties'):
            title += '\n' + '\n'.join(f'{k}: {v}' for k, v in properties.items())

        nodes.append(
                Node(
                    id=entity['entity_id'], 
                    label=_wrap_text(entity['entity_names'][0]), 
                    title=title,
                    size=10,
                    shape='box',
                    shadow=True
                ))
    for rel in g['relationships']:
        edges.append(
                Edge(
                    source=rel['source_entity_id'], 
                    label=rel['relationship'], 
                    target=rel['target_entity_id'],
                    smooth=True,
                    shadow=True
                ))

    config = Config(
            height=500,
            directed=True, 
            physics=True, 
            hierarchical=False,
            # **kwargs
    )

    return agraph(nodes=nodes, edges=edges, config=config)


def _wrap_text(text, width=32):
  """
  Adds word wrap to a given string at a specified width.

  Args:
    text: The input string to be wrapped.
    width: The maximum width of each line. Defaults to 70 characters.

  Returns:
    A new string with word wrap applied.
  """
  wrapped_text = textwrap.fill(text, width=width)
  return wrapped_text
