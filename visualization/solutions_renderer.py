
import streamlit as st
from .board_renderer import render_board

def render_solutions(solutions, n):
    """
    Renders all solutions in a grid.
    """
    if not solutions:
        st.info("No solutions found.")
        return

    cols = st.columns(4) # 4 columns grid
    for idx, sol_board in enumerate(solutions):
        with cols[idx % 4]:
            st.caption(f"Solution {idx + 1}")
            # Construct a minimal state object for renderer
            # solution board is just [col1, col2...]
            state = {"board": sol_board} 
            render_board(state, n, key_suffix=f"_sol_{idx}")
            st.space("small")
