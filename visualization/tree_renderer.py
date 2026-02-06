import streamlit as st
import graphviz
import tempfile

def render_tree(tree_data, n=8):
    """
    Renders the recursion tree using Graphviz.
    tree_data: { 'nodes': [...], 'edges': [...] }
    """
    # 1. Show Stats / Preview
    known_solutions = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    expected = known_solutions.get(n, "Unknown")
    
    has_data = tree_data and tree_data.get('nodes')
    status_text = "Generated" if has_data else "Waiting to start..."
    
    st.markdown(f"""
    ### Recursion Tree Info
    - **Depth**: N = {n}
    - **Max Branching Factor**: {n}
    - **Estimated Search Space**: {n}^{n} = {n**n:,}
    - **Expected Solutions**: {expected}
    - **Tree Status**: {status_text}
    """)

    if not has_data:
        return

    # 2. Render Graph
    graph = graphviz.Digraph()
    graph.attr(rankdir='TB', nodesep='0.25', ranksep='0.6')
    
    # 1. Add Nodes
    for node in tree_data['nodes']:
        # Color coding
        color = "black"
        style = "solid"
        fillcolor = "white"
        
        status = node.get('status', 'visit')
        if status == 'valid':
            color = "green"
            fillcolor = "#e6ffe6"
            style = "filled"
        elif status == 'invalid':
            color = "red"
            fillcolor = "#ffe6e6"
            style = "filled"
        elif status == 'solution':
            color = "blue"
            fillcolor = "#e6e6ff"
            style = "filled"
        
        label = node.get('label', str(node['id']))
        graph.node(str(node['id']), label=label, color=color, style=style, fillcolor=fillcolor)
    
    # 2. Add Edges
    for edge in tree_data['edges']:
        # Edge format might be tuple or dict depending on tree_builder
        # tree_builder.py uses {"from": p, "to": c}
        u = str(edge['from'])
        v = str(edge['to'])
        graph.edge(u, v)

    st.graphviz_chart(graph)