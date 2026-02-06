
class TreeBuilder:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.node_counter = 0

    def create_node_id(self):
        self.node_counter += 1
        return self.node_counter

    def add_node(self, node_id, label, parent_id=None, status="visit", row=None, col=None):
        """
        Stats: 'visit' (default), 'valid', 'invalid', 'solution'
        """
        node = {
            "id": node_id, 
            "label": label, 
            "status": status,
            "row": row,
            "col": col
        }
        self.nodes.append(node)
        
        if parent_id is not None:
            self.edges.append({"from": parent_id, "to": node_id})
    
    def update_node_status(self, node_id, status):
        for node in self.nodes:
            if node["id"] == node_id:
                node["status"] = status
                break
