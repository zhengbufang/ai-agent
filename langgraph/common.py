from langgraph.graph.state import CompiledStateGraph

def image_graph(graph:CompiledStateGraph,image_name:str):
    if graph is None or image_name is None:
        return
    graph_png = graph.get_graph(xray=1).draw_mermaid_png()
    with open(image_name, "wb") as f:
        f.write(graph_png)