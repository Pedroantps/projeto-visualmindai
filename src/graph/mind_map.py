import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import textwrap

def build_graph(hierarchy_dict: dict) -> nx.DiGraph:
    G = nx.DiGraph()
    def add_nodes_edges(node, parent=None, level=0):
        node_name = node["name"]
        G.add_node(node_name, level=level)
        if parent:
            G.add_edge(parent, node_name)
        if "children" in node:
            for child in node["children"]:
                add_nodes_edges(child, node_name, level + 1)
    add_nodes_edges(hierarchy_dict)
    return G

def get_horizontal_tree_positions(G):
    pos = {}
    root_nodes = [n for n, d in G.nodes(data=True) if d.get('level') == 0]
    if not root_nodes: return pos
    root = root_nodes[0]
    
    pos[root] = np.array([0.0, 0.0])
    branches = list(G.successors(root))
    
    mid = (len(branches) + 1) // 2
    right_branches = branches[:mid]
    left_branches = branches[mid:]

    # AUMENTO AGRESSIVO DE ESPAÇOS
    # X_DISTANCE: Empurra as colunas (Níveis 1, 2 e 3) muito mais para longe umas das outras
    X_DISTANCE = 28.0  
    # BASE_Y_DISTANCE: Aumenta a distância vertical padrão entre as caixas
    BASE_Y_DISTANCE = 6.0  

    def layout_side(branch_list, direction):
        current_leaf_y = 0.0
        side_nodes = []

        def dfs(node, depth):
            nonlocal current_leaf_y
            children = list(G.successors(node))
            side_nodes.append(node)

            if not children:
                # Alargamos a quebra de linha para 40 caracteres (deixa a caixa mais achatada)
                lines = len(textwrap.wrap(node, width=40))
                # Empurra a caixa de baixo ainda mais longe se essa tiver muitas linhas
                dynamic_y_gap = BASE_Y_DISTANCE + (lines * 2.5)

                my_y = current_leaf_y
                current_leaf_y -= dynamic_y_gap
                pos[node] = np.array([direction * depth * X_DISTANCE, my_y])
                return my_y

            child_ys = []
            for child in children:
                child_ys.append(dfs(child, depth + 1))

            my_y = sum(child_ys) / len(child_ys)
            pos[node] = np.array([direction * depth * X_DISTANCE, my_y])
            return my_y

        for branch in branch_list:
            dfs(branch, 1)

        if side_nodes:
            y_coords = [pos[n][1] for n in side_nodes]
            center_y = (max(y_coords) + min(y_coords)) / 2.0
            for n in side_nodes:
                pos[n][1] -= center_y

    layout_side(right_branches, 1)
    layout_side(left_branches, -1)
    return pos

def draw_mind_map(hierarchy_dict: dict, container_frame) -> plt.Figure:
    G = build_graph(hierarchy_dict)

    for widget in container_frame.winfo_children(): widget.destroy()

    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor('#242424')
    ax.set_facecolor('#242424')

    pos = get_horizontal_tree_positions(G)

    x_values = [coords[0] for coords in pos.values()]
    y_values = [coords[1] for coords in pos.values()]
    if x_values and y_values:
        # Câmera mais distante para enquadrar o mapa que agora é super largo
        ax.set_xlim(min(x_values) - 15, max(x_values) + 15)
        ax.set_ylim(min(y_values) - 8, max(y_values) + 8)

    for u, v in G.edges():
        ax.annotate("", xy=pos[v], xycoords='data', xytext=pos[u], textcoords='data',
                    arrowprops=dict(arrowstyle="->,head_length=0.4,head_width=0.2", 
                                    color="#666666", linewidth=1.5, connectionstyle="arc3,rad=-0.02"))

    for node, data in G.nodes(data=True):
        level = data.get('level', 0)
        x, y = pos[node]
        
        wrapped_list = textwrap.wrap(node, width=40)
        wrapped_text = "\n".join(wrapped_list)
        lines_count = len(wrapped_list)
        
        # DIMINUIÇÃO GERAL DO TAMANHO DAS CAIXAS (padding e fonte menores)
        if level == 0:
            bbox_props = dict(boxstyle="round,pad=0.8", fc="#ff9800", ec="#e65100", lw=2.5)
            font_size, font_weight = 12, 'bold'
        elif level == 1:
            bbox_props = dict(boxstyle="round,pad=0.6", fc="#8bc34a", ec="#558b2f", lw=2)
            font_size, font_weight = 10, 'bold'
        elif level == 2:
            bbox_props = dict(boxstyle="round,pad=0.4", fc="#03a9f4", ec="#0277bd", lw=1.5)
            font_size = 8 if lines_count <= 2 else 7
            font_weight = 'bold'
        else:
            bbox_props = dict(boxstyle="round,pad=0.3", fc="#ab47bc", ec="#7b1fa2", lw=1)
            font_size = 7 if lines_count <= 2 else 6
            font_weight = 'normal'

        ax.text(x, y, wrapped_text, ha='center', va='center', bbox=bbox_props, color='white', 
                fontsize=font_size, fontweight=font_weight, zorder=5)

    ax.axis('off')
    plt.tight_layout(pad=1)

    canvas = FigureCanvasTkAgg(fig, master=container_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return fig