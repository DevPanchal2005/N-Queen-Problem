
class Metrics:
    def __init__(self):
        self.calls = 0
        self.backtracks = 0
        self.max_depth = 0

    def increment_calls(self):
        self.calls += 1

    def increment_backtracks(self):
        self.backtracks += 1
    
    def update_max_depth(self, depth):
        if depth > self.max_depth:
            self.max_depth = depth
    
    def to_dict(self):
        return {
            "calls": self.calls,
            "backtracks": self.backtracks,
            "max_depth": self.max_depth
        }
