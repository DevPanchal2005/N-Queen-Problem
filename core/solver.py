
import copy
from .metrics import Metrics
from .tree_builder import TreeBuilder
from .state_logger import StateLogger
from .safety import is_safe

import time

class NQueenSolver:
    def __init__(self, n):
        self.n = n
        self.board = [-1] * n  # 1D array: index=row, value=col
        self.solutions = []
        
        # Initialize helpers
        self.metrics = Metrics()
        self.tree_builder = TreeBuilder()
        self.state_logger = StateLogger()
        
    def solve(self):
        """
        Main entry point to solve the N-Queens problem.
        Returns a dictionary containing all visualization data.
        """
        start_time = time.perf_counter()
        
        # Create root node for the tree
        root_id = self.tree_builder.create_node_id()
        self.tree_builder.add_node(root_id, "Start", status="root", row=-1, col=-1)
        
        # Start backtracking
        self.solve_backtracking(0, root_id)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        return {
            "n": self.n,
            "solutions": self.solutions,
            "steps": self.state_logger.logs,
            "tree": {
                "nodes": self.tree_builder.nodes,
                "edges": self.tree_builder.edges
            },
            "metrics": self.metrics.to_dict(),
            "execution_time": execution_time
        }

    def solve_backtracking(self, row, parent_node_id):
        self.metrics.increment_calls()
        self.metrics.update_max_depth(row)

        if row == self.n:
            # All queens placed successfully
            self.solutions.append(copy.copy(self.board))
            
            # Metrics snapshot
            metrics_snap = self.metrics.to_dict()
            metrics_snap['solutions'] = len(self.solutions)
            
            self.state_logger.log_state(self.board, row, -1, "solution", "Solution Found!", metrics=metrics_snap)
            # Mark parent as part of solution path (optional optimization: post-process)
            return

        for col in range(self.n):
            # 1. Visualization: Trying to place
            metrics_snap = self.metrics.to_dict()
            metrics_snap['solutions'] = len(self.solutions)
            self.state_logger.log_state(self.board, row, col, "try", f"Trying R{row}, C{col}", metrics=metrics_snap)
            
            # Tree Node creation
            node_id = self.tree_builder.create_node_id()
            label = f"({row}, {col})"
            self.tree_builder.add_node(node_id, label, parent_node_id, status="visit", row=row, col=col)
            
            if is_safe(self.board, row, col, self.n):
                # Place Queen
                self.board[row] = col
                
                metrics_snap = self.metrics.to_dict()
                metrics_snap['solutions'] = len(self.solutions)
                self.state_logger.log_state(self.board, row, col, "place", f"Placed R{row}, C{col}", metrics=metrics_snap)
                self.tree_builder.update_node_status(node_id, "valid")
                
                # Recurse
                self.solve_backtracking(row + 1, node_id)
                
                # Backtrack: Remove Queen
                self.board[row] = -1
                self.metrics.increment_backtracks()
                
                metrics_snap = self.metrics.to_dict()
                metrics_snap['solutions'] = len(self.solutions)
                self.state_logger.log_state(self.board, row, col, "remove", f"Backtracking from R{row}, C{col}", metrics=metrics_snap)
                # We don't mark 'invalid' here because it might have contributed to a solution or just finished sub-tree
            else:
                # Not safe
                self.tree_builder.update_node_status(node_id, "invalid")
                # Optional: Log the failure explicitly if we want detailed fail steps
                # self.state_logger.log_state(self.board, row, col, "invalid", f"Unsafe R{row}, C{col}")
